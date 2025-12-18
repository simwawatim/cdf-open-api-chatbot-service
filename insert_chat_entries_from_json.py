import sqlite3
import json
from pathlib import Path

# ---------------- Paths ----------------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"  # Path to your Django SQLite database
JSON_PATH = BASE_DIR / "cdf_entries.json"

# ---------------- Connect to SQLite ----------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---------------- Load JSON file ----------------
with open(JSON_PATH, "r", encoding="utf-8") as f:
    chat_data = json.load(f)

# ---------------- Insert data ----------------
for entry in chat_data:
    question = entry.get("question")
    answer = entry.get("answer")

    if question and answer:
        # Check if question already exists
        cursor.execute("SELECT id FROM chat_chatentry WHERE question = ?", (question,))
        exists = cursor.fetchone()
        if exists:
            print(f"Already exists: {question}")
        else:
            cursor.execute(
                "INSERT INTO chat_chatentry (question, answer) VALUES (?, ?)",
                (question, answer)
            )
            print(f"Inserted: {question}")

# ---------------- Commit and close ----------------
conn.commit()
conn.close()
print("All entries processed!")
