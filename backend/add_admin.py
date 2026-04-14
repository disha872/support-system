import sqlite3

conn = sqlite3.connect("support.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin", "admin123", "admin")
)

conn.commit()
print("Admin added ✅")