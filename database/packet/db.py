import sqlite3

DB_PATH = "database/db.sqlite"


def get_db_connection():
    """Create a new database connection and return it."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn


def init_db():
    """Create the database tables if they don't exist."""
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


def store_email_data(email_data):
    """Store incoming email data into the database."""
    # Find or create a conversation for the email
    conversation_id = find_existing_conversation(email_data["subject"])

    if not conversation_id:
        # If no conversation exists, create one
        conversation_id = create_conversation(email_data["subject"])

    # Insert the email into the corresponding conversation
    insert_email(conversation_id, email_data["from"], email_data["to"], email_data["body"], email_data["is_reply"])

    return {"message": "Email stored successfully!"}
