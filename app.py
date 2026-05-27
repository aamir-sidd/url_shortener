from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"

db = SQLAlchemy(app)

# Database model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    short_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    long_url = db.Column(
        db.Text,
        nullable=False
    )

    # Explicit constructor to satisfy the IDE's type checker
    def __init__(self, short_code, long_url):
        self.short_code = short_code
        self.long_url = long_url

# Create tables
with app.app_context():
    db.create_all()

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

    # Create object
    new_url = URL(
        short_code=short_code,
        long_url=long_url
    )

    db.session.add(new_url)
    db.session.commit()

    return f"""
    Short URL: 
    <a href="/{short_code}">
        http://localhost:5000/{short_code}
    </a>
    """

@app.route("/<short_code>")
def redirect_url(short_code):
    # Query database
    url = URL.query.filter_by(
        short_code=short_code
    ).first()

    if url:
        return redirect(url.long_url)

    return "URL not found"

if __name__ == "__main__":
    app.run(debug=True)