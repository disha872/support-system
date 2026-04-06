import streamlit as st
import requests
import pandas as pd

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Support System", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.stButton button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("💬 Smart Customer Support System")

BASE_URL = "https://support-system-zla6.onrender.com"

# ---------------- MENU ----------------
if not st.session_state.logged_in:
    menu = ["Login", "Register"]
else:
    if st.session_state.role == "admin":
        menu = ["Admin", "Analytics"]
    else:
        menu = ["Chat", "Tickets", "My Tickets"]

choice = st.sidebar.selectbox("Menu", menu)

# ---------------- LOGOUT ----------------
if st.session_state.logged_in:
    st.sidebar.write(f"👤 {st.session_state.username} ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()

# ---------------- LOGIN ----------------
if choice == "Login":
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{BASE_URL}/login",
            json={"username": username, "password": password}
        )

        data = res.json()

        if "message" in data:
            st.success("Login successful ✅")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = data.get("role", "user")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

# ---------------- REGISTER ----------------
elif choice == "Register":
    st.subheader("📝 Register")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        res = requests.post(
            f"{BASE_URL}/register",
            json={"username": username, "password": password}
        )
        st.write(res.json())

# ---------------- CHAT ----------------
elif choice == "Chat":
    st.subheader("💬 Chat Support")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Type your message")

    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            res = requests.post(
                f"{BASE_URL}/chat",
                json={"message": user_input}
            )

            bot_reply = res.json().get("response", "Error")

            st.session_state.messages.append(("user", user_input))
            st.session_state.messages.append(("bot", bot_reply))

    for sender, msg in st.session_state.messages:
        if sender == "user":
            st.markdown(
                f"<div style='text-align:left; color:black; background:#DCF8C6; padding:10px; border-radius:10px; margin:5px;'>{msg}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='text-align:left; color:black; background:#F1F0F0; padding:10px; border-radius:10px; margin:5px;'>{msg}</div>",
                unsafe_allow_html=True
            )

# ---------------- TICKETS ----------------
elif choice == "Tickets":
    st.subheader("🎫 Raise a Ticket")

    issue = st.text_area("Describe your issue")

    if st.button("Submit Ticket") and issue:
        res = requests.post(
            f"{BASE_URL}/ticket",
            json={
                "issue": issue,
                "user": st.session_state.username
            }
        )
        st.success(res.json().get("message", "Done"))

# ---------------- USER TICKETS ----------------
elif choice == "My Tickets":
    st.subheader("📄 My Tickets")

    res = requests.get(f"{BASE_URL}/mytickets/{st.session_state.username}")
    data = res.json()

    for t in data["tickets"]:
        st.markdown(f"**Issue:** {t['issue']}")
        st.markdown(f"**Status:** {t['status']}")
        st.markdown(f"**Reply:** {t['reply'] or 'No reply yet'}")
        st.write("------")

# ---------------- ADMIN ----------------
elif choice == "Admin":
    st.subheader("👨‍💼 Admin Dashboard")

    res = requests.get(f"{BASE_URL}/tickets")
    data = res.json()

    for t in data["tickets"]:
        st.markdown(f"**User:** {t.get('user','N/A')}")
        st.markdown(f"**Issue:** {t['issue']}")
        st.markdown(f"**Status:** {t['status']}")

        reply = st.text_input(f"Reply for {t['id']}", key=f"reply_{t['id']}")

        if st.button(f"Send Reply {t['id']}", key=f"btn_{t['id']}"):
            requests.post(
                f"{BASE_URL}/reply/{t['id']}",
                json={"reply": reply}
            )
            st.success("Replied!")
            st.rerun()

        st.write("------")

# ---------------- ANALYTICS ----------------
elif choice == "Analytics":
    st.subheader("📊 Ticket Analytics")

    res = requests.get(f"{BASE_URL}/analytics")
    data = res.json()

    df = pd.DataFrame(list(data.items()), columns=["Status", "Count"])
    st.bar_chart(df.set_index("Status"))