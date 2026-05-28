# Version 11: Link Expiration Dates

In this version, we introduced temporal constraints to shortened URLs. Users can specify a self-destruction timeline (expiry) for their links, automatically rendering them inactive once their duration lapses.

## Project Structure
No structural changes were made in this version.
```text
url_shortener/
│
├── app.py            # Main application (updated URL model schema and expiry checking)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git, automatically recreated on startup)
├── static/           # Static assets directory
│   └── style.css     # Clean stylesheet
├── templates/        # Jinja2 HTML templates directory
│   ├── base.html     # Layout
│   ├── home.html     # Homepage form (updated with expiry options select & history expiry column)
│   └── result.html   # Confirmation page (updated to show expiry date)
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 11

### 1. Database Schema Extensions (app.py)
We updated the `URL` model to track timestamps using Python's `datetime` module:
* `created_at`: Records the URL creation timestamp in UTC.
* `expires_at`: Stores the expiration target timestamp in UTC. If empty (`None`), the link remains active indefinitely.

```python
class URL(db.Model):
    # ... other columns ...
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
```

### 2. Redirection Validation
When a shortened code is accessed, the server checks the current timestamp against `expires_at`. If expired, it blocks redirection and returns a `410 Gone` HTTP status code:
```python
if url:
    if url.expires_at and datetime.utcnow() > url.expires_at:
        return "This short link has expired.", 410
    return redirect(url.long_url)
```

### 3. Options in Web Form and REST API
* **Web UI Form (`home.html`):** Adds a `<select name="expires_in">` dropdown with choices ranging from 1 Minute (testing), 1 Hour, 1 Day, 7 Days, to Never.
* **REST API (`/api/shorten`):** Accepts an optional `"expires_in_minutes"` parameter inside the JSON payload to calculate `expires_at` dynamically.

---

## 🔬 API & Response Examples

### 1. API Shorten Request (with Expiry)
* **Request (POST `/api/shorten`):**
  ```json
  {
    "long_url": "https://example.com",
    "expires_in_minutes": 5
  }
  ```
* **Response (201 Created):**
  ```json
  {
    "short_code": "xC19aD",
    "short_url": "http://127.0.0.1:5000/xC19aD",
    "long_url": "https://example.com",
    "expires_at": "2026-05-28T04:20:00"
  }
  ```

### 2. API GET Request (Expired Link)
* **Request (GET `/api/url/xC19aD`):**
* **Response (410 Gone):**
  ```json
  {
    "error": "URL has expired"
  }
  ```
