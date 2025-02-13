import sqlite3

DB_PATH = "database/db.sqlite"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create database tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        sender TEXT NOT NULL,
        recipient TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        body TEXT NOT NULL,
        is_reply BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id)
    );
    """)
    conn.commit()
    conn.close()


def create_conversation(subject):
    """Create a new conversation thread and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO conversations (subject) VALUES (?)", (subject,))
    conn.commit()
    conversation_id = cursor.lastrowid  # Get the newly created conversation ID

    conn.close()
    return conversation_id


def find_existing_conversation(subject):
    """Check if a conversation with the same subject exists."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM conversations WHERE subject = ?", (subject,))
    row = cursor.fetchone()

    conn.close()
    return row["id"] if row else None


def insert_email(conversation_id, sender, recipient, body, is_reply):
    """Insert an email into the database under the given conversation ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO emails (conversation_id, sender, recipient, body, is_reply)
    VALUES (?, ?, ?, ?, ?)
    """, (conversation_id, sender, recipient, body, is_reply))

    conn.commit()
    conn.close()


def get_conversation_emails(conversation_id):
    """Retrieve all emails in a conversation, sorted by timestamp."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT sender, recipient, body, timestamp, is_reply
    FROM emails WHERE conversation_id = ?
    ORDER BY timestamp
    """, (conversation_id,))

    emails = cursor.fetchall()
    conn.close()
    return emails

