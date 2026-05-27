# Version 7: Minimal Monochrome Styling Integration

In this version, we introduced a clean, minimal black-and-white visual theme to structure the application. We chose a simple layout avoiding heavy cards, shadows, or popup effects, keeping a flat print-like aesthetic.

## Project Structure
We introduced a new `static/` directory to store static assets like stylesheets.
```text
url_shortener/
│
├── app.py            # Main application
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
├── static/           # Static assets directory
│   └── style.css     # Clean, flat monochrome CSS stylesheet
├── templates/        # Jinja2 HTML templates directory
│   ├── base.html     # Layout (linked with stylesheet, removed raw <hr> tags)
│   ├── home.html     # Homepage form
│   └── result.html   # Confirmation page
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 7

### 1. Minimal Flat Design Style
We created `static/style.css` following a strict black, white, and gray color palette:
* **Layout Structure:** Uses a simple layout with a thin-bordered header (navbar), centered content space, and a flat footer.
* **No Shadows or Popups:** Kept the UI flat, clean, and fast with no card shadows, box-shadows, or transitions except for a clean hover indicator.
* **Buttons & Inputs:** Inputs have simple borders that turn dark on focus. The button has a flat black background and shifts to dark gray on hover.

### 2. Template Integration
We linked the stylesheet in [base.html](file:///d:/onedrivee/Cars%203/Desktop/url_shortener_iitm/templates/base.html) and removed the legacy `<hr>` tags since the border dividers are now cleanly handled by CSS styling.
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```
