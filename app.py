from flask import Flask, request, redirect, render_template
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
    return render_template("home.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form["long_url"].strip()

    # URL Validation / Normalization
    if not (long_url.startswith("http://") or long_url.startswith("https://")):
        long_url = "https://" + long_url

    # Generate a unique short code to prevent collisions
    while True:
        short_code = generate_code()
        existing = URL.query.filter_by(short_code=short_code).first()
        if not existing:
            break

    # Create object
    new_url = URL(
        short_code=short_code,
        long_url=long_url
    )

    db.session.add(new_url)
    db.session.commit()

    return redirect(f"/result/{short_code}")

@app.route("/result/<short_code>")
def result(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return "URL not found"

    return render_template("result.html", url=url)

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