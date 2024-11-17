import sqlite3
from pathlib import Path

DB_FILE = "local.db"

def initialize_db():
    """Initializes the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdf_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            url TEXT,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_pdf_downloaded(pdf_name):
    """Check if the PDF is already in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pdf_metadata WHERE name = ?", (pdf_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_pdf_record(pdf_name, url):
    """Add a new PDF record to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pdf_metadata (name, url) VALUES (?, ?)", (pdf_name, url))
    conn.commit()
    conn.close()

def count_pdfs():
    """Count the number of PDFs in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pdf_metadata")
    count = cursor.fetchone()[0]
    conn.close()
    return count
