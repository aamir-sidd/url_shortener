# Version 3: Flask-SQLAlchemy Integration & Post-Redirect-Get (PRG) Pattern

In this version, we transitioned from raw SQLite query execution (`sqlite3`) to a modern Python **ORM (Object-Relational Mapper)** using `Flask-SQLAlchemy`. We also refactored the redirect workflow to prevent duplicate form submissions upon page refresh.

## Project Structure
```text
url_shortener/
│
├── app.py            # Main application using Flask & Flask-SQLAlchemy
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
└── .gitignore        # Updated to ignore venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 3

### 1. Object-Relational Mapping (ORM)
Instead of writing raw SQL commands, we define our database tables as Python classes inheriting from `db.Model`.
```python
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    long_url = db.Column(db.Text, nullable=False)

    # Satisfies IDE type-checkers (e.g. Pylance/Pyright)
    def __init__(self, short_code, long_url):
        self.short_code = short_code
        self.long_url = long_url
```

### 2. Solving Duplicate Submissions with PRG
* **The Issue in Version 2:** When a user submitted a URL, they were shown the result directly on the `/shorten` route (which was a `POST` request). If they refreshed the page, the browser re-submitted the `POST` request, generating a brand new short code and inserting the same long URL into the database again.
* **The Solution (Post-Redirect-Get):**
  1. The user sends a `POST` request to `/shorten`.
  2. The server processes the request and saves the URL database object.
  3. Instead of rendering HTML directly, the server redirects (`302`) to a `GET` route: `/result/<short_code>`.
  4. The browser performs a clean `GET` request to `/result/<short_code>` and renders the page. 
  5. Refreshes on the result page now simply query the database without creating duplicate entries.

```text
[User Form Submit] (POST /shorten)
         ↓
 [Create db entry]
         ↓
 [HTTP Redirect] (302 Redirect to /result/<code>)
         ↓
[Render Result UI] (GET /result/<code>)
```

---

## 🔬 How It Works Internally

### 1. Shortening a URL
* User enters `https://google.com` on the homepage `/`.
* Form submits to `POST /shorten`.
* The server calls `generate_code()` to generate a unique key (e.g. `6JV8rC`).
* The server instantiates a `URL` object and saves it:
  ```python
  new_url = URL(short_code=short_code, long_url=long_url)
  db.session.add(new_url)
  db.session.commit()
  ```
* The server redirects the user to `/result/6JV8rC`.

### 2. Showing the Result
* The route `@app.route("/result/<short_code>")` fetches the URL:
  ```python
  url = URL.query.filter_by(short_code=short_code).first()
  ```
* It returns the success message with a link to the shortened URL.

### 3. Redirection
* Visiting `http://127.0.0.1:5000/6JV8rC` triggers `@app.route("/<short_code>")`.
* The server queries the database:
  ```python
  url = URL.query.filter_by(short_code=short_code).first()
  ```
* Redirects the browser: `redirect(url.long_url)`.