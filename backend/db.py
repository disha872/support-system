import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "support.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# TABLES
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue TEXT,
    user TEXT,
    reply TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()

# USERS
def create_user(username, password):
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, 'user')",
        (username, password)
    )
    conn.commit()

def get_user(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    return cursor.fetchone()

# TICKETS
def create_ticket(issue, user):
    cursor.execute(
        "INSERT INTO tickets (issue, user, status) VALUES (?, ?, 'Pending')",
        (issue, user)
    )
    conn.commit()

def get_all_tickets():
    cursor.execute("SELECT * FROM tickets")
    return cursor.fetchall()

def reply_ticket(ticket_id, reply):
    cursor.execute(
        "UPDATE tickets SET reply=?, status='Resolved' WHERE id=?",
        (reply, ticket_id)
    )
    conn.commit()

def get_user_tickets(username):
    cursor.execute(
        "SELECT * FROM tickets WHERE user=?",
        (username,)
    )
    return cursor.fetchall()