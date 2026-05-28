# Version 12: Background Cleanup Worker (with APScheduler)

In this version, we introduced automatic background clean-up. We configured a scheduling worker that runs in the background of our application to prune expired links from the database.

## Project Structure
No structural changes were made in this version.
```text
url_shortener/
│
├── app.py            # Main application (updated with background scheduler setup)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
├── static/           # Static assets directory
│   └── style.css     # Clean stylesheet
├── templates/        # Jinja2 HTML templates directory
│   ├── base.html     # Layout
│   ├── home.html     # Homepage form (updated with 2-minute and 5-minute expiry options)
│   └── result.html   # Confirmation page
├── requirements.txt  # Updated to track apscheduler and Flask-SQLAlchemy dependencies
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 12

### 1. Dependency Integration (requirements.txt)
We added `apscheduler` and `Flask-SQLAlchemy` dependencies to keep our dependencies tracked:
```text
Flask
Flask-SQLAlchemy
apscheduler
```

### 2. In-Process Background Scheduler (app.py)
We integrated `BackgroundScheduler` from the `apscheduler` library. Because it runs in-process on a separate background thread, it does not require running extra terminal worker processes or third-party databases (like Celery/Redis requires).

* **The Clean-up Task:**
  Queries for all URLs where `expires_at` is in the past, deletes them from the SQLite database, and prints a success message to the terminal console:
  ```python
  def delete_expired_links():
      with app.app_context():
          now = datetime.utcnow()
          expired_count = URL.query.filter(URL.expires_at < now).delete()
          db.session.commit()
          if expired_count > 0:
              print(f"[Cleanup Worker] Deleted {expired_count} expired links at {now}.")
  ```

* **Scheduler Startup:**
  Launches the scheduler on app startup. For testing convenience, it is scheduled to run the clean-up task **every 30 seconds**:
  ```python
  scheduler = BackgroundScheduler()
  scheduler.add_job(func=delete_expired_links, trigger="interval", seconds=30)
  scheduler.start()
  ```

### 3. More Minute-Based Expiration Durations
To test the clean-up task, we added options for **2 Minutes** and **5 Minutes** to the home form. The `/shorten` route computes these offsets dynamically:
```python
elif expires_in == "2m":
    expires_at = datetime.utcnow() + timedelta(minutes=2)
elif expires_in == "5m":
    expires_at = datetime.utcnow() + timedelta(minutes=5)
```
