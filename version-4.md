# Version 4: URL Validation & Normalization

In this version, we added URL cleaning and validation logic to prevent a common redirection bug where inputs without `http://` or `https://` schemes were treated as relative paths on our local server.

## Project Structure
No structural changes were made in this version.
```text
url_shortener/
│
├── app.py            # Main application (updated with URL normalization)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 4

### 1. URL Normalization
When a user submits a URL, the backend now trims accidental whitespace and checks if the URL starts with a valid protocol scheme (`http://` or `https://`). If it does not, the system defaults to prepending `https://`.

```python
long_url = request.form["long_url"].strip()

# URL Validation / Normalization
if not (long_url.startswith("http://") or long_url.startswith("https://")):
    long_url = "https://" + long_url
```

---

## 🔬 How It Works (Examples)

Here is how different user inputs are processed and stored in the database:

| User Input | Processed URL (Stored in DB) | Redirection Behavior |
| :--- | :--- | :--- |
| `https://github.com` | `https://github.com` | Redirects to external site (GitHub) |
| `http://example.com` | `http://example.com` | Redirects to external site (Example) |
| `google.com` | `https://google.com` | Automatically prepends scheme, redirects to external site (Google) |
| `  yahoo.com  ` | `https://yahoo.com` | Strips whitespace, prepends scheme, redirects to external site (Yahoo) |
