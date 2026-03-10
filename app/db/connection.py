import sqlite3
from flask import g
from pathlib import Path

# Build the absolute path to the database file
DB_PATH = Path(__file__).resolve().parent.parent.parent / "travel_board.db"

def get_db():
    # Prevents opening duplicate connections in the same context
    if "db" not in g:
        # open the data base connection (if not exists the file, it will be created)
        g.db = sqlite3.connect(DB_PATH)
        # access column by name
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    # remove the connection safely
    db = g.pop("db", None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL,
            category TEXT NOT NULL,
            planned_date TEXT,
            estimated_budget REAL,
            status TEXT NOT NULL,
            notes TEXT,
            is_favorite INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );
    """)

    db.commit()
    
def init_app(app):
    # register the automatic close connection at the end of context
    app.teardown_appcontext(close_db)