# Version 6: Jinja2 Templates Integration

In this version, we decoupled the presentation layer (HTML) from the application logic (Python). We created a template structure using Jinja2 inheritance, allowing for a clean, extendable foundation.

## Project Structure
We introduced a new `templates/` directory to hold our HTML layouts.
```text
url_shortener/
│
├── app.py            # Main application (now rendering templates)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
├── templates/        # Jinja2 HTML templates directory
│   ├── base.html     # Base structural layout
│   ├── home.html     # Homepage shortening form
│   └── result.html   # Shortening confirmation page
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 6

### 1. Template Inheritance (`base.html`)
To prevent repeating the HTML head tags, layout structures, header, and footer on every single page, we created a master template called `base.html`. This acts as the structural shell for the entire app. Other templates insert their content dynamically into Jinja2 blocks: `{% block title %}` and `{% block content %}`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}URL Shortener{% endblock %}</title>
</head>
<body>
    <header><h1><a href="/">URL Shortener</a></h1></header>
    <hr>
    <main>
        {% block content %}{% endblock %}
    </main>
    <hr>
    <footer><p>&copy; 2026 URL Shortener project</p></footer>
</body>
</html>
```

### 2. Rendering Templates with Flask
In `app.py`, we replaced all inline HTML string returns with the Flask `render_template` utility.

* **Homepage (`/`):**
  ```python
  @app.route('/')
  def home():
      return render_template("home.html")
  ```

* **Result Page (`/result/<short_code>`):**
  Passes the database object `url` directly to the template context so its attributes (`long_url` and `short_code`) can be rendered dynamically.
  ```python
  @app.route("/result/<short_code>")
  def result(short_code):
      url = URL.query.filter_by(short_code=short_code).first()
      if not url:
          return "URL not found"
      return render_template("result.html", url=url)
  ```
