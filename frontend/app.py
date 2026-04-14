import streamlit as st
import requests

API = "https://support-system-zla6.onrender.com"

st.set_page_config(page_title="Support System", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Menu")

menu = ["Login", "Register"]

if st.session_state.logged_in:
    if st.session_state.role == "admin":
        menu = ["Admin"]
    else:
        menu = ["Home", "Chat", "My Tickets"]

choice = st.sidebar.selectbox("Navigate", menu)

# User info
if st.session_state.logged_in:
    st.sidebar.success(f"👤 {st.session_state.username} ({st.session_state.role})")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

# About section
st.sidebar.markdown("## ℹ️ About App")
st.sidebar.info("""
Smart Customer Support System

👤 Users:
- Chat with bot
- Raise tickets
- Track issues

🧑‍💼 Admin:
- View tickets
- Reply & resolve
""")

# ---------------- LOGIN ----------------
if choice == "Login":
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API}/login", json={"username": u, "password": p}).json()

        if "error" in res:
            st.error(res["error"])
        else:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.session_state.role = res["role"]
            st.success("Login successful ✅")
            st.rerun()

# ---------------- REGISTER ----------------
elif choice == "Register":
    st.title("📝 Register")

    u = st.text_input("Create Username")
    p = st.text_input("Create Password", type="password")

    if st.button("Register"):
        requests.post(f"{API}/register", json={"username": u, "password": p})
        st.success("Registered successfully ✅")

# ---------------- HOME ----------------
elif choice == "Home":
    st.title("👋 Welcome to Smart Customer Support System")

    st.markdown("""
    ### 💡 What you can do:

    ✅ Ask your problems in chat  
    ✅ Get instant answers  
    ✅ If not satisfied → raise ticket  
    ✅ Track your tickets  

    ---
    """)

# ---------------- CHAT ----------------
if st.button("Send"):
    if msg.strip() == "":
        st.warning("Please enter a message")
    else:
        res = requests.post(f"{API}/chat", json={"message": msg}).json()

        if "response" in res:
            st.success(f"🤖 {res['response']}")

            if "don't understand" in res["response"]:
                st.warning("Not satisfied? Create a ticket 👇")

                if st.button("📩 Create Ticket"):
                    requests.post(f"{API}/ticket", json={
                        "issue": msg,
                        "user": st.session_state.username
                    })
                    st.success("Ticket created ✅")

        else:
            st.error(res.get("error", "Server error"))
# ---------------- USER TICKETS ----------------
elif choice == "My Tickets":
    st.title("🎫 My Tickets")

    res = requests.get(f"{API}/mytickets/{st.session_state.username}").json()

    if not res["tickets"]:
        st.info("No tickets found")
    else:
        for t in res["tickets"]:
            with st.container():
                st.markdown(f"""
                **🆔 ID:** {t['id']}  
                **❗ Issue:** {t['issue']}  
                **💬 Reply:** {t['reply']}  
                **📌 Status:** {t['status']}  
                """)
                st.divider()

# ---------------- ADMIN ----------------
elif choice == "Admin":
    st.title("🧑‍💼 Admin Dashboard")

    st.markdown("### 📋 All Tickets")

    res = requests.get(f"{API}/tickets").json()

    if not res["tickets"]:
        st.info("No tickets available")
    else:
        for t in res["tickets"]:
            with st.container():
                st.markdown(f"""
                **🆔 ID:** {t['id']}  
                **👤 User:** {t['user']}  
                **❗ Issue:** {t['issue']}  
                **📌 Status:** {t['status']}  
                """)

                reply = st.text_input(f"Reply to Ticket {t['id']}", key=f"reply_{t['id']}")

                if st.button(f"Send Reply {t['id']}"):
                    requests.post(f"{API}/reply/{t['id']}", json={"reply": reply})
                    st.success("Replied successfully ✅")
                    st.rerun()

                st.divider()