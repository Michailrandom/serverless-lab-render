from flask import Flask, request, jsonify
import psycopg2
import os
from urllib.parse import urlparse
app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    url = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=serverless_db_fti8_user,
        password=rH8x2UvWQkvO7ZzOWqN9jb90Jl1cvnFS,
        host=dpg-d3que7ur433s73e1hctg-a,
        port=5432
    )
else:
    conn = None
if conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
@app.route('/save', methods=['POST'])
def save_message():
    if not conn:
        return jsonify({"error": "DB not connected"}), 500
    data = request.get_json()
    message = data.get('message', '') if data else ''
    with conn.cursor() as cur:
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        conn.commit()
    return jsonify({"status": "saved", "message": message})
@app.route('/messages')
def get_messages():
    if not conn:
        return jsonify({"error": "DB not connected"}), 500
    with conn.cursor() as cur:
        cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC LIMIT 10")
        rows = cur.fetchall()
    messages = [{"id": r[0], "text": r[1], "time": r[2].isoformat()} for r in rows]
    return jsonify(messages)
