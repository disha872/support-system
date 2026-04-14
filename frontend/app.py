import streamlit as st
import requests

API = "https://support-system-zla6.onrender.com/"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

menu = ["Login", "Register"]

if st.session_state.logged_in:
    if st.session_state.role == "admin":
        menu = ["Admin"]
    else:
        menu = ["Chat", "My Tickets"]
choice = st.sidebar.selectbox("Menu", menu)
if st.session_state.logged_in:
    st.sidebar.write(f"👤 {st.session_state.username} ({st.session_state.role})")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()


# LOGIN
if choice == "Login":
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
            st.rerun()

# REGISTER
elif choice == "Register":
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        requests.post(f"{API}/register", json={"username": u, "password": p})
        st.success("Registered")

# CHAT
elif choice == "Chat":
    msg = st.text_input("Ask your problem")

    if st.button("Send"):
        res = requests.post(f"{API}/chat", json={
            "message": msg,
            "user": st.session_state.username
        }).json()

        st.write("Bot:", res["response"])

        if "ticket" in res:
            st.warning("Ticket created!")

# USER TICKETS
elif choice == "My Tickets":
    res = requests.get(f"{API}/mytickets/{st.session_state.username}").json()

    for t in res["tickets"]:
        st.write(t)

# ADMIN
elif choice == "Admin":
    res = requests.get(f"{API}/tickets").json()

    for t in res["tickets"]:
        st.write(t)
        reply = st.text_input(f"Reply {t[0]}", key=t[0])

        if st.button(f"Send {t[0]}"):
            requests.post(f"{API}/reply/{t[0]}", json={"reply": reply})
            st.success("Replied")