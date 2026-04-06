import mysql.connector

# ---------------- CONNECTION ----------------
import os

conn = mysql.connector.connect(
    host=os.getenv("mysql.railway.internal"),
    user=os.getenv("root"),
    password=os.getenv("cTfdEyejDDTNGwlNTMVRWePciMGDrpET"),
    database=os.getenv("railway")
)

cursor = conn.cursor()


# ---------------- CHAT ----------------
def save_chat(message, response):
    try:
        query = "INSERT INTO chats (message, response) VALUES (%s, %s)"
        cursor.execute(query, (message, response))
        conn.commit()
    except Exception as e:
        print("Chat Save Error:", e)


# ---------------- TICKETS ----------------
def create_ticket(issue, user):
    try:
        query = "INSERT INTO tickets (issue, user) VALUES (%s, %s)"
        cursor.execute(query, (issue, user))
        conn.commit()
    except Exception as e:
        print("Ticket Error:", e)


def get_all_tickets():
    query = "SELECT id, issue, user, status, created_at FROM tickets"
    cursor.execute(query)
    return cursor.fetchall()


def resolve_ticket(ticket_id):
    query = "UPDATE tickets SET status='Resolved' WHERE id=%s"
    cursor.execute(query, (ticket_id,))
    conn.commit()


def reply_ticket(ticket_id, reply):
    query = "UPDATE tickets SET reply=%s, status='Resolved' WHERE id=%s"
    cursor.execute(query, (reply, ticket_id))
    conn.commit()


def get_user_tickets(username):
    query = "SELECT id, issue, reply, status FROM tickets WHERE user=%s"
    cursor.execute(query, (username,))
    return cursor.fetchall()


# ---------------- USERS ----------------
def create_user(username, password):
    try:
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')"
        cursor.execute(query, (username, password))
        conn.commit()
    except Exception as e:
        print("User Create Error:", e)


def get_user(username, password):
    query = "SELECT id, username, password, role FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    return cursor.fetchone()


# ---------------- CHAT HISTORY ----------------
def get_chats():
    query = "SELECT message, response FROM chats ORDER BY id DESC LIMIT 10"
    cursor.execute(query)
    return cursor.fetchall()


# ---------------- ANALYTICS ----------------
def get_ticket_stats():
    query = "SELECT status, COUNT(*) FROM tickets GROUP BY status"
    cursor.execute(query)
    return cursor.fetchall()