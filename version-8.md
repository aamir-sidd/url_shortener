# Version 8: URL Validation and Flash Messages

In this version, we introduced domain structure validation for incoming URLs and user feedback alerts using Flask's flash messaging framework.

## Project Structure
No structural changes were made in this version.
```text
url_shortener/
│
├── app.py            # Main application (updated with secret key and validation helper)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
├── static/           # Static assets directory
│   └── style.css     # Clean stylesheet (updated with flash notification styles)
├── templates/        # Jinja2 HTML templates directory
│   ├── base.html     # Layout (updated with dynamic flash message display loops)
│   ├── home.html     # Homepage form
│   └── result.html   # Confirmation page
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 8

### 1. Flash Session Integration
To support Flask's session-based notification system (`flash`), we assigned a secret key configuration to the application inside `app.py`:
```python
app.secret_key = "url_shortener_dev_secret_key"
```

### 2. URL Format Regex Validation
We defined an `is_valid_url` helper function utilizing a strict regular expression to check if the input URL maps to a valid hostname structure, IP address, or `localhost`:
```python
def is_valid_url(url):
    regex = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None
```

### 3. Redirect Handling and Alerts
* **Validation Failure:** If validation fails, we trigger a flash error message and redirect the user back to the homepage (`/`):
  ```python
  if not is_valid_url(long_url):
      flash("Invalid URL! Please enter a valid web address.", "error")
      return redirect(url_for("home"))
  ```
* **Validation Success:** Upon successful entry, we trigger a flash success message and show the result page:
  ```python
  flash("URL created successfully!", "success")
  return redirect(url_for("result", short_code=short_code))
  ```

---

## 🎨 UI Updates

### 1. base.html Flash Box
We configured the flash template display loop inside the `<main>` block of [base.html](file:///d:/onedrivee/Cars%203/Desktop/url_shortener_iitm/templates/base.html):
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <div class="flashes">
            {% for category, message in messages %}
                <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
        </div>
    {% endif %}
{% endwith %}
```

### 2. Monochrome Styles
We styled notifications in [style.css](file:///d:/onedrivee/Cars%203/Desktop/url_shortener_iitm/static/style.css) adhering to our monochrome visual theme:
* **Success Messages:** Rendered inside a light gray box with a solid black border.
* **Error Messages:** Rendered inside a light gray box with a dashed black border to stand out without using colors.
