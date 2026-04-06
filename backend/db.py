import mysql.connector
import os

# ---------------- SAFE CONNECTION ----------------
conn = None
cursor = None

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "containers-xxx.railway.app"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "cTfdEyejDDTNGwlNTMVRWePciMGDrpET"),
        database=os.getenv("DB_NAME", "railway"),
        port=int(os.getenv("DB_PORT", 41295))
    )
    cursor = conn.cursor()
    print("DB Connected ✅")

except Exception as e:
    print("DB Connection Failed ❌:", e)
    conn = None
    cursor = None


# ---------------- CHAT ----------------
def save_chat(message, response):
    if cursor is None:
        return
    try:
        query = "INSERT INTO chats (message, response) VALUES (%s, %s)"
        cursor.execute(query, (message, response))
        conn.commit()
    except Exception as e:
        print("Chat Save Error:", e)


# ---------------- TICKETS ----------------
def create_ticket(issue, user):
    if cursor is None:
        return
    try:
        query = "INSERT INTO tickets (issue, user) VALUES (%s, %s)"
        cursor.execute(query, (issue, user))
        conn.commit()
    except Exception as e:
        print("Ticket Error:", e)


def get_all_tickets():
    if cursor is None:
        return []
    try:
        query = "SELECT id, issue, user, status, created_at FROM tickets"
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return []


def resolve_ticket(ticket_id):
    if cursor is None:
        return
    try:
        query = "UPDATE tickets SET status='Resolved' WHERE id=%s"
        cursor.execute(query, (ticket_id,))
        conn.commit()
    except Exception as e:
        print("Resolve Error:", e)


def reply_ticket(ticket_id, reply):
    if cursor is None:
        return
    try:
        query = "UPDATE tickets SET reply=%s, status='Resolved' WHERE id=%s"
        cursor.execute(query, (reply, ticket_id))
        conn.commit()
    except Exception as e:
        print("Reply Error:", e)


def get_user_tickets(username):
    if cursor is None:
        return []
    try:
        query = "SELECT id, issue, reply, status FROM tickets WHERE user=%s"
        cursor.execute(query, (username,))
        return cursor.fetchall()
    except:
        return []


# ---------------- USERS ----------------
def create_user(username, password):
    if cursor is None:
        return
    try:
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')"
        cursor.execute(query, (username, password))
        conn.commit()
    except Exception as e:
        print("User Create Error:", e)


def get_user(username, password):
    # Admin login
    if username == "admin" and password == "admin123":
        return (1, "admin", "admin123", "admin")

    # Dummy user login
    if username == "user" and password == "user123":
        return (2, "user", "user123", "user")

    return None


# ---------------- CHAT HISTORY ----------------
def get_chats():
    if cursor is None:
        return []
    try:
        query = "SELECT message, response FROM chats ORDER BY id DESC LIMIT 10"
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return []


# ---------------- ANALYTICS ----------------
def get_ticket_stats():
    if cursor is None:
        return []
    try:
        query = "SELECT status, COUNT(*) FROM tickets GROUP BY status"
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return []