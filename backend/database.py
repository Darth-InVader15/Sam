import sqlite3
import json
from datetime import datetime
from typing import List, Dict

DB_PATH = "sam_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            user_input TEXT NOT NULL,
            llm_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_interaction(mode: str, user_input: str, llm_response: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (mode, user_input, llm_response) VALUES (?, ?, ?)",
        (mode, user_input, llm_response)
    )
    conn.commit()
    conn.close()

def get_recent_history(mode: str, limit: int = 5) -> List[Dict[str, str]]:
    """
    Retrieves recent history for a specific mode.
    Returns a list of dicts: [{"role": "user", "content": ...}, {"role": "assistant", "content": ...}]
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_input, llm_response FROM conversations WHERE mode = ? ORDER BY id DESC LIMIT ?",
        (mode, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    # Rows are returned newest first, we want oldest first for the context window
    for row in reversed(rows):
        history.append({"role": "user", "content": row[0]})
        history.append({"role": "assistant", "content": row[1]})
        
    return history

# Initialize DB on module load (simple approach)
init_db()
