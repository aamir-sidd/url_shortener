from flask import Flask, request, redirect, render_template, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string
import re
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "url_shortener_dev_secret_key"

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

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # Explicit constructor to satisfy the IDE's type checker
    def __init__(self, short_code, long_url, expires_at=None):
        self.short_code = short_code
        self.long_url = long_url
        self.expires_at = expires_at

# Create tables
with app.app_context():
    db.create_all()

def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    regex = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/')
def home():
    urls = URL.query.all()
    return render_template("home.html", urls=urls)

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form["long_url"].strip()

    # URL Normalization
    if not (long_url.startswith("http://") or long_url.startswith("https://")):
        long_url = "https://" + long_url

    # URL Validation
    if not is_valid_url(long_url):
        flash("Invalid URL! Please enter a valid web address.", "error")
        return redirect(url_for("home"))

    # Calculate Expiration Time
    expires_in = request.form.get("expires_in", "never")
    expires_at = None
    if expires_in == "1m":
        expires_at = datetime.utcnow() + timedelta(minutes=1)
    elif expires_in == "1h":
        expires_at = datetime.utcnow() + timedelta(hours=1)
    elif expires_in == "1d":
        expires_at = datetime.utcnow() + timedelta(days=1)
    elif expires_in == "7d":
        expires_at = datetime.utcnow() + timedelta(days=7)

    # Generate a unique short code to prevent collisions
    while True:
        short_code = generate_code()
        existing = URL.query.filter_by(short_code=short_code).first()
        if not existing:
            break

    # Create object
    new_url = URL(
        short_code=short_code,
        long_url=long_url,
        expires_at=expires_at
    )

    db.session.add(new_url)
    db.session.commit()

    flash("URL created successfully!", "success")
    return redirect(url_for("result", short_code=short_code))

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
        # Check Expiration
        if url.expires_at and datetime.utcnow() > url.expires_at:
            return "This short link has expired.", 410
        return redirect(url.long_url)

    return "URL not found"

@app.route("/delete/<short_code>")
def delete_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        db.session.delete(url)
        db.session.commit()
        flash("URL deleted successfully!", "success")
    else:
        flash("URL not found!", "error")
    return redirect(url_for("home"))

# ==========================================
# REST API Endpoints
# ==========================================

@app.route("/api/shorten", methods=["POST"])
def api_shorten():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    long_url = data.get("long_url")

    if not long_url:
        return jsonify({"error": "Missing long_url parameter"}), 400

    long_url = long_url.strip()

    # Normalization
    if not (long_url.startswith("http://") or long_url.startswith("https://")):
        long_url = "https://" + long_url

    # Validation
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Calculate Expiration Time
    expires_in_minutes = data.get("expires_in_minutes")
    expires_at = None
    if expires_in_minutes is not None:
        try:
            expires_at = datetime.utcnow() + timedelta(minutes=int(expires_in_minutes))
        except (ValueError, TypeError):
            return jsonify({"error": "expires_in_minutes must be an integer"}), 400

    # Generate a unique short code to prevent collisions
    while True:
        short_code = generate_code()
        existing = URL.query.filter_by(short_code=short_code).first()
        if not existing:
            break

    # Create object
    new_url = URL(
        short_code=short_code,
        long_url=long_url,
        expires_at=expires_at
    )
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://127.0.0.1:5000/{short_code}",
        "long_url": long_url,
        "expires_at": expires_at.isoformat() if expires_at else None
    }), 201

@app.route("/api/url/<short_code>", methods=["GET", "DELETE"])
def api_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({"error": "URL not found"}), 404

    if request.method == "GET":
        # Check Expiration
        if url.expires_at and datetime.utcnow() > url.expires_at:
            return jsonify({"error": "URL has expired"}), 410

        return jsonify({
            "short_code": url.short_code,
            "short_url": f"http://127.0.0.1:5000/{url.short_code}",
            "long_url": url.long_url,
            "expires_at": url.expires_at.isoformat() if url.expires_at else None
        }), 200

    elif request.method == "DELETE":
        db.session.delete(url)
        db.session.commit()
        return jsonify({"message": "URL deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)