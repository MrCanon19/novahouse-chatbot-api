import psycopg2
import json

# Konfiguracja bazy danych
DB_CONFIG = {
    'host': '35.205.83.191',
    'database': 'chatbot_db',
    'user': 'chatbot_user',
    'password': 'NovaHouse2024SecurePass',
    'port': 5432
}

def fix_json_in_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT id, training_phrases, response_templates FROM intents;")
        intents = cursor.fetchall()

        for intent_id, training_phrases, response_templates in intents:
            try:
                json.loads(training_phrases)
            except json.JSONDecodeError:
                fixed_training_phrases = json.dumps(eval(training_phrases))
                cursor.execute("UPDATE intents SET training_phrases = %s WHERE id = %s;", (fixed_training_phrases, intent_id))
                print(f"Fixed training_phrases for intent {intent_id}")

            try:
                json.loads(response_templates)
            except json.JSONDecodeError:
                fixed_response_templates = json.dumps(eval(response_templates))
                cursor.execute("UPDATE intents SET response_templates = %s WHERE id = %s;", (fixed_response_templates, intent_id))
                print(f"Fixed response_templates for intent {intent_id}")

        conn.commit()
        conn.close()
        print("Finished fixing JSON in the database.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fix_json_in_db()

