# Version 5: Collision Handling (Robustness)

In this version, we implemented a robust collision avoidance mechanism. This ensures the application never crashes due to database unique constraint violations if the random code generator produces a code that is already in use.

## Project Structure
No structural changes were made in this version.
```text
url_shortener/
│
├── app.py            # Main application (updated with collision checking loop)
├── instance/         # Flask instance directory (ignored by git)
│   └── urls.db       # Database file (ignored by git)
└── .gitignore        # Ignores venv, compiled files, and instance/
```

---

## 🛠️ Key Improvements in Version 5

### 1. Unique Short Code Guarantee (Loop Checking)
Previously, the code generator was called only once. If it generated a code that already existed in the database, the server would crash with a database `IntegrityError` (Unique constraint failed).

We implemented a `while True` loop that repeatedly generates a short code, queries the database, and checks if it exists. The loop only breaks when it finds a code that is completely unused.

```python
# Generate a unique short code to prevent collisions
while True:
    short_code = generate_code()
    existing = URL.query.filter_by(short_code=short_code).first()
    if not existing:
        break
```

### 2. Multi-submission Behavior
As per the project specification:
* The system **always generates a new short code** for every URL entered, even if that same long URL has been shortened before.
* This allows users to track/create separate short links for the same destination URL while ensuring none of the generated short codes collide.
