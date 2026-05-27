# Version 10: JSON REST API Layer

In this version, we introduced a headless REST API layer to allow external programs, automation scripts, browser extensions, or mobile applications to manage shortened URLs programmatically.

## Project Structure
No structural changes were made in this version.
```text
url_shortener/
│
├── app.py            # Main application (updated with REST API endpoints)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
├── static/           # Static assets directory
│   └── style.css     # Clean stylesheet
├── templates/        # Jinja2 HTML templates directory
│   ├── base.html     # Layout
│   ├── home.html     # Homepage form
│   └── result.html   # Confirmation page
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 10

### 1. Flask `jsonify` Integration
We imported `jsonify` from Flask to format native Python dictionaries into JSON responses with correct HTTP response headers (`Content-Type: application/json`).

### 2. The REST Endpoints (app.py)

* **Create Short Link (POST `/api/shorten`):**
  Accepts a JSON payload containing `long_url`. Validates, normalizes, and generates a unique short code.
  * **Status Codes:** `201 Created` on success, `400 Bad Request` on invalid formatting or missing parameters.
  * **Payload Example:**
    ```json
    { "long_url": "google.com" }
    ```
  * **Response Example:**
    ```json
    {
      "short_code": "xC19aD",
      "short_url": "http://127.0.0.1:5000/xC19aD",
      "long_url": "https://google.com"
    }
    ```

* **Query Metadata (GET `/api/url/<short_code>`):**
  Retrieves information about a shortened code.
  * **Status Codes:** `200 OK` on success, `404 Not Found` if the code does not exist.
  * **Response Example:**
    ```json
    {
      "short_code": "xC19aD",
      "short_url": "http://127.0.0.1:5000/xC19aD",
      "long_url": "https://google.com"
    }
    ```

* **Delete Short Link (DELETE `/api/url/<short_code>`):**
  Deletes the mapping from the database.
  * **Status Codes:** `200 OK` on success, `404 Not Found` if the code does not exist.
  * **Response Example:**
    ```json
    {
      "message": "URL deleted successfully"
    }
    ```
