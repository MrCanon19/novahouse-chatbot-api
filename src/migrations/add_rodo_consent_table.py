"""
Migration: Add RODO Consent Table
Dodaje tabelę do śledzenia zgód RODO użytkowników chatbota
"""

import os
import sys

# Dodaj ścieżkę główną projektu do sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.chatbot import db, RodoConsent
from datetime import datetime


def upgrade():
    """Utwórz tabelę rodo_consents"""
    print("Creating rodo_consents table...")
    
    # Tabela zostanie utworzona automatycznie przez SQLAlchemy
    # na podstawie modelu RodoConsent
    db.create_all()
    
    print("✅ Table rodo_consents created successfully")


def downgrade():
    """Usuń tabelę rodo_consents"""
    print("Dropping rodo_consents table...")
    
    RodoConsent.__table__.drop(db.engine)
    
    print("✅ Table rodo_consents dropped successfully")


if __name__ == '__main__':
    from src.main import app
    
    with app.app_context():
        print("Running RODO consent table migration...")
        upgrade()
        print("Migration completed!")