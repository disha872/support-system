from fastapi import FastAPI
from pydantic import BaseModel
from backend.chatbot import get_response
from backend.db import (
    save_chat,
    create_ticket,
    get_all_tickets,
    resolve_ticket,
    create_user,
    get_user,
    get_chats,
    get_ticket_stats,
    reply_ticket,
    get_user_tickets
)

app = FastAPI()

# ---------------- MODELS ----------------
class Query(BaseModel):
    message: str

class Ticket(BaseModel):
    issue: str
    user: str   # ✅ FIXED

class User(BaseModel):
    username: str
    password: str

class Reply(BaseModel):
    reply: str

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "API Working"}

# ---------------- CHAT ----------------
@app.post("/chat")
def chat(query: Query):
    try:
        if not query.message:
            return {"error": "Message cannot be empty"}

        response = get_response(query.message)
        save_chat(query.message, response)

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}

# ---------------- CREATE TICKET ----------------
@app.post("/ticket")
def create_new_ticket(ticket: Ticket):
    try:
        create_ticket(ticket.issue, ticket.user)
        return {"message": "Ticket created"}
    except Exception as e:
        return {"error": str(e)}

# ---------------- GET ALL TICKETS ----------------
@app.get("/tickets")
def fetch_tickets():
    try:
        data = get_all_tickets()

        tickets = []
        for row in data:
            tickets.append({
                "id": row[0],
                "issue": row[1],
                "user": row[2],        # ✅ FIXED
                "status": row[3],
                "created_at": str(row[4])
            })

        return {"tickets": tickets}

    except Exception as e:
        return {"error": str(e)}

# ---------------- RESOLVE ----------------
@app.post("/resolve/{ticket_id}")
def resolve(ticket_id: int):
    try:
        resolve_ticket(ticket_id)
        return {"message": "Ticket resolved"}
    except Exception as e:
        return {"error": str(e)}

# ---------------- REGISTER ----------------
@app.post("/register")
def register(user: User):
    try:
        if not user.username or not user.password:
            return {"error": "Username & Password required"}

        create_user(user.username, user.password)
        return {"message": "User registered"}

    except Exception as e:
        return {"error": str(e)}

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: User):
    try:
        data = get_user(user.username, user.password)

        if data:
            return {
                "message": "Login successful",
                "role": data[3]   # ✅ IMPORTANT (admin/user)
            }
        else:
            return {"error": "Invalid credentials"}

    except Exception as e:
        return {"error": str(e)}

# ---------------- CHAT HISTORY ----------------
@app.get("/history")
def chat_history():
    try:
        data = get_chats()

        history = []
        for row in data:
            history.append({
                "message": row[0],
                "response": row[1]
            })

        return {"history": history}

    except Exception as e:
        return {"error": str(e)}

# ---------------- ANALYTICS ----------------
@app.get("/analytics")
def analytics():
    try:
        data = get_ticket_stats()

        stats = {}
        for row in data:
            stats[row[0]] = row[1]

        return stats

    except Exception as e:
        return {"error": str(e)}

# ---------------- ADMIN REPLY ----------------
@app.post("/reply/{ticket_id}")
def reply(ticket_id: int, data: Reply):
    try:
        reply_ticket(ticket_id, data.reply)
        return {"message": "Replied successfully"}
    except Exception as e:
        return {"error": str(e)}

# ---------------- USER TICKETS ----------------
@app.get("/mytickets/{username}")
def my_tickets(username: str):
    try:
        data = get_user_tickets(username)

        tickets = []
        for row in data:
            tickets.append({
                "id": row[0],
                "issue": row[1],
                "reply": row[2],
                "status": row[3]
            })

        return {"tickets": tickets}

    except Exception as e:
        return {"error": str(e)}