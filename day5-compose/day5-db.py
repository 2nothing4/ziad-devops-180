import psycopg2
import time

# Wait for database to be ready
time.sleep(2)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="db",
    database="devops",
    user="ziad",
    password="secret123"
)

# Create table
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Insert data
cur.execute("INSERT INTO logs (message) VALUES (%s)", ("Day 5: Docker Compose is real",))
conn.commit()

# Read data back
cur.execute("SELECT * FROM logs")
rows = cur.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Message: {row[1]}, Time: {row[2]}")

cur.close()
conn.close()
