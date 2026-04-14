from fastapi import FastAPI
from pydantic import BaseModel
from db import *
from chatbot import get_response,save_chat

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

class Query(BaseModel):
    message: str
    user: str

class Ticket(BaseModel):
    issue: str
    user: str

class Reply(BaseModel):
    reply: str

@app.get("/")
def home():
    return {"message": "API Running"}

# REGISTER
@app.post("/register")
def register(user: User):
    create_user(user.username, user.password)
    return {"message": "Registered"}

# LOGIN
@app.post("/login")
def login(user: User):
    data = get_user(user.username, user.password)
    if data:
        return {"message": "Login success", "role": data[3]}
    return {"error": "Invalid credentials"}

# CHAT + AUTO TICKET
@app.post("/chat")
def chat(query: Query):
    try:
        if not query.message:
            return {"error": "Message cannot be empty"}

        response = get_response(query.message)

        try:
            save_chat(query.message, response)
        except:
            pass  # DB fail hone pe bhi app crash nahi hoga

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}

# ADMIN
@app.get("/tickets")
def tickets():
    return {"tickets": get_all_tickets()}

@app.post("/reply/{ticket_id}")
def reply(ticket_id: int, r: Reply):
    reply_ticket(ticket_id, r.reply)
    return {"message": "Replied"}

# USER TICKETS
@app.get("/mytickets/{username}")
def my(username: str):
    return {"tickets": get_user_tickets(username)}