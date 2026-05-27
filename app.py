from flask import Flask, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("urls.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE,
                long_url TEXT
        )
    """)
    conn.close()

init_db()

def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def home():
    return """
    <form action="/shorten" method="POST">
        <input name="long_url" placeholder="Enter URL">
        <button type="submit">Shorten</button>
    </form>
    """

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form["long_url"]

    short_code = generate_code()

    conn = sqlite3.connect("urls.db")
    conn.execute(
        "INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
        (short_code, long_url)    
        )
    conn.commit()
    conn.close()

    return f"""
    Short URL: 
    <a href="/{short_code}">
        http://localhost:5000/{short_code}
    </a>
    """

@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.execute(
        "SELECT long_url FROM urls WHERE short_code = ?",
        (short_code,)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])

    return "URL not found"

if __name__ == "__main__":
    app.run(debug=True)