from flask import Flask, render_template, redirect, url_for, request
import random
import string
from datetime import datetime, timezone
import sqlite3
from flask import session

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("urls.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        original_url TEXT,
        clicks INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

app.secret_key = "dev_secret_key"

@app.route('/', methods=["GET", "POST"])
def home():
    short_url = session.pop('short_url', None)

    if request.method == "POST":
        url = request.form["url"]

        if not url.startswith("http://") and not url.startswith('https://'):
            return render_template("index.html", error="Invalid URL")

        newurl = generate_unique_code()

        conn = sqlite3.connect("urls.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO urls (code, original_url, created_at) VALUES (?, ?, ?)",
            (newurl, url, datetime.now(timezone.utc).isoformat())
        )

        conn.commit()
        conn.close()

        session['short_url'] = request.host_url + newurl
        return redirect(url_for('home'))

    return render_template('index.html', short_url=short_url)

def generate_unique_code():
    while True:
        code = generate_short_code()
        conn = sqlite3.connect("urls.db")
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM urls WHERE code=?", (code,))
        exists = cur.fetchone()

        conn.close()

        if not exists:
            return code
@app.route('/history')
def history():
    conn = sqlite3.connect("urls.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT code, original_url, clicks, created_at
        FROM urls
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return render_template("history.html", rows=rows)

@app.route('/<newurl>')
def redirect_url(newurl):
    conn = sqlite3.connect("urls.db")
    cur = conn.cursor()

    cur.execute("SELECT original_url, clicks FROM urls WHERE code=?", (newurl,))
    row = cur.fetchone()

    if row:
        original_url, clicks = row

        cur.execute(
            "UPDATE urls SET clicks=? WHERE code=?",
            (clicks + 1, newurl)
        )
        conn.commit()
        conn.close()

        return redirect(original_url)

    conn.close()
    return "URL not found", 404

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

if __name__ == "__main__":
    app.run(debug=True)