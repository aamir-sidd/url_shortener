# Version 9: Global History List & Deletes (CRUD)

In this version, we completed the database CRUD (Create, Read, Update, Delete) capability of our application. Users can now view a historical record of all shortened URLs directly on the homepage and delete any link from the database.

## Project Structure
No structural changes were made in this version.
```text
url_shortener/
│
├── app.py            # Main application (updated home and delete routes)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
├── static/           # Static assets directory
│   └── style.css     # Clean stylesheet (updated with history table styles)
├── templates/        # Jinja2 HTML templates directory
│   ├── base.html     # Layout (displays flash alerts)
│   ├── home.html     # Homepage form (updated with history table and delete links)
│   └── result.html   # Confirmation page
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 9

### 1. Database Queries & Deletes (app.py)
* **Read (Listing all links):** We updated the home route to load all records from the SQLite database using the SQLAlchemy model:
  ```python
  @app.route('/')
  def home():
      urls = URL.query.all()
      return render_template("home.html", urls=urls)
  ```
* **Delete (Removing a link):** We added a `/delete/<short_code>` route. It retrieves the URL, deletes it from the database, commits the changes, and notifies the user with a flash message:
  ```python
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
  ```

---

## 🎨 UI Updates

### 1. home.html History Table
We added a table underneath the URL shortener form inside [home.html](file:///d:/onedrivee/Cars%203/Desktop/url_shortener_iitm/templates/home.html). It loops over the queried `urls` list:
```html
{% if urls %}
    <div class="history-section">
        <h2>History</h2>
        <table class="history-table">
            <thead>
                <tr>
                    <th>Original URL</th>
                    <th>Short Link</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for url in urls %}
                    <tr>
                        <td class="long-url-cell" title="{{ url.long_url }}">{{ url.long_url }}</td>
                        <td><a href="/{{ url.short_code }}" target="_blank">http://127.0.0.1:5000/{{ url.short_code }}</a></td>
                        <td><a href="/delete/{{ url.short_code }}" class="delete-btn">Delete</a></td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endif %}
```

### 2. Table & Truncation Styles (style.css)
* **Text Overflow Handling (`.long-url-cell`):** Long input URLs are automatically truncated with an ellipsis (`...`) so they don't break the layout. Hovering over a cell displays the full URL as a browser tooltip via the `title` attribute.
* **Monochrome Delete Button:** Styled the "Delete" link with a thin gray border. On hover, the button flips colors (black background, white text) in keeping with our flat design guidelines.
