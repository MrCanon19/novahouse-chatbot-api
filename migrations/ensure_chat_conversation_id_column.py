import argparse
import os
import sys
from typing import Any, Dict, List

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import SQLAlchemyError

TABLE_NAME = "chat_conversations"


def redact_url(db_url: str) -> str:
    try:
        url_obj = make_url(db_url)
        if url_obj.password is not None:
            url_obj = url_obj.set(password="***")
        return str(url_obj)
    except Exception:
        return "<redacted>"


def get_engine(db_url: str) -> Engine:
    if not db_url:
        raise RuntimeError(
            "Brak adresu bazy. Podaj go parametrem --db lub w zmiennej SQLALCHEMY_DATABASE_URI."
        )

    redacted = redact_url(db_url)
    print(f"[INFO] Łączę z bazą: {redacted}")

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return engine
    except SQLAlchemyError as exc:
        print(f"[ERROR] Nie udało się połączyć z bazą: {exc}", file=sys.stderr)
        raise


def inspect_schema(engine: Engine) -> Dict[str, Any]:
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    if TABLE_NAME not in tables:
        raise RuntimeError(
            f"Tabela {TABLE_NAME} nie istnieje w tej bazie. "
            f"Dostępne tabele: {', '.join(tables)}"
        )

    columns = inspector.get_columns(TABLE_NAME)
    pk = inspector.get_pk_constraint(TABLE_NAME) or {}
    uniques = inspector.get_unique_constraints(TABLE_NAME) or []
    indexes = inspector.get_indexes(TABLE_NAME) or []

    return {
        "columns": columns,
        "primary_key": pk,
        "uniques": uniques,
        "indexes": indexes,
    }


def print_schema_report(schema: Dict[str, Any]) -> None:
    print("\n=== Schemat tabeli chat_conversations ===\n")

    print("Kolumny:")
    for col in schema["columns"]:
        name = col.get("name")
        col_type = col.get("type")
        nullable = col.get("nullable")
        default = col.get("default")
        print(f"  - {name}: {col_type}, nullable={nullable}, default={default}")

    pk = schema.get("primary_key") or {}
    pk_name = pk.get("name")
    pk_cols = pk.get("constrained_columns") or []
    print("\nPrimary key:")
    print(f"  nazwa constraintu: {pk_name}")
    print(f"  kolumny: {', '.join(pk_cols) if pk_cols else '<brak>'}")

    print("\nUnikalne constrainty:")
    uniques: List[Dict[str, Any]] = schema.get("uniques") or []
    if not uniques:
        print("  <brak>")
    else:
        for uc in uniques:
            print(f"  - {uc.get('name')}: {', '.join(uc.get('column_names') or [])}")

    print("\nIndeksy:")
    indexes: List[Dict[str, Any]] = schema.get("indexes") or []
    if not indexes:
        print("  <brak>")
    else:
        for idx in indexes:
            cols = ", ".join(idx.get("column_names") or [])
            print(f"  - {idx.get('name')}: {cols}, unique={idx.get('unique')}")


def suggest_remediation(schema: Dict[str, Any]) -> None:
    print("\n=== Propozycja naprawy schematu pod model ORM ===\n")
    print("Założenia modelu:")
    print("  - kolumna id jako BIGSERIAL PRIMARY KEY")
    print("  - kolumna session_id z unikalnością\n")

    dialect = schema.get("dialect")
    if dialect != "postgresql":
        print(
            "Wykryty dialekt nie jest PostgreSQL. Skrypt nie generuje gotowego SQL "
            "dla innych baz. Użyj raportu powyżej jako punktu wyjścia.",
            file=sys.stderr,
        )
        return

    columns: List[Dict[str, Any]] = schema["columns"]
    pk = schema.get("primary_key") or {}
    pk_cols = pk.get("constrained_columns") or []
    pk_name = pk.get("name")

    col_names = {c["name"] for c in columns}
    has_id = "id" in col_names
    has_conversation_id = "conversation_id" in col_names

    print("Przykładowe komendy SQL dla PostgreSQL. Wykonuj je w psql.")

    if has_conversation_id and not has_id and pk_cols == ["conversation_id"]:
        print("\nScenariusz: PK na conversation_id, brak kolumny id.")
        print("Proponowany SQL:")
        print(
            f"""
-- 1. Usuń obecny primary key
ALTER TABLE {TABLE_NAME}
DROP CONSTRAINT {pk_name};

-- 2. Zmień nazwę conversation_id na id
ALTER TABLE {TABLE_NAME}
RENAME COLUMN conversation_id TO id;

-- 3. Ustaw id jako primary key
ALTER TABLE {TABLE_NAME}
ADD CONSTRAINT {TABLE_NAME}_pkey PRIMARY KEY (id);

-- 4. Zapewnij unikalność session_id
CREATE UNIQUE INDEX IF NOT EXISTS {TABLE_NAME}_session_id_key
ON {TABLE_NAME} (session_id);
""".strip()
        )
        return

    if not has_id:
        print("\nScenariusz: brak kolumny id.")
        print("Proponowany SQL:")
        print(
            f"""
ALTER TABLE {TABLE_NAME}
ADD COLUMN id BIGSERIAL;

ALTER TABLE {TABLE_NAME}
ADD CONSTRAINT {TABLE_NAME}_pkey PRIMARY KEY (id);

CREATE UNIQUE INDEX IF NOT EXISTS {TABLE_NAME}_session_id_key
ON {TABLE_NAME} (session_id);
""".strip()
        )
        return

    if has_id and (pk_cols != ["id"]):
        print("\nScenariusz: kolumna id istnieje, ale primary key jest ustawiony inaczej.")
        print("Proponowany SQL (dopasuj nazwę constraintu jeśli inna):")
        drop_clause = ""
        if pk_name:
            drop_clause = f"ALTER TABLE {TABLE_NAME}\n" f"DROP CONSTRAINT {pk_name};\n\n"

        print(
            f"""
{drop_clause}ALTER TABLE {TABLE_NAME}
ADD CONSTRAINT {TABLE_NAME}_pkey PRIMARY KEY (id);

CREATE UNIQUE INDEX IF NOT EXISTS {TABLE_NAME}_session_id_key
ON {TABLE_NAME} (session_id);
""".strip()
        )
        return

    print(
        "Schemat wygląda na zgodny z założeniami modelu "
        "(id jako PK, session_id unikalne). Jeśli ORM dalej zgłasza błędy, "
        "sprawdź konfigurację modelu i połączenia."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnostyka tabeli chat_conversations i sugerowane poprawki schematu."
    )
    parser.add_argument(
        "--db",
        "--database-url",
        dest="db_url",
        help=(
            "Pełny URL bazy w formacie SQLAlchemy, na przykład "
            "postgresql+psycopg2://user:pass@host:5432/dbname. "
            "Jeśli nie podasz, zostanie użyta zmienna SQLALCHEMY_DATABASE_URI."
        ),
    )

    args = parser.parse_args()
    db_url = args.db_url or os.environ.get("SQLALCHEMY_DATABASE_URI")

    try:
        engine = get_engine(db_url)
        dialect = engine.dialect.name

        schema = inspect_schema(engine)
        schema["dialect"] = dialect

        print_schema_report(schema)
        suggest_remediation(schema)

        print("\n[OK] Diagnostyka zakończona pomyślnie.")
        return 0

    except Exception as exc:
        print(f"[ERROR] Diagnostyka nie powiodła się: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
