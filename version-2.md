How this version2 works-
In this version, we introduced a SQLite database (`urls.db`) so that shortened links survive server restarts. We also replaced sequential short codes (`1`, `2`, `3`) with randomized 6-character unique codes (`PUPwbk`, `Zrdiln`, etc.) to prevent users from easily guessing or enumerating other links.

Project Structure:
url_shortener/
│
├── app.py
├── urls.db   ← auto-created on first run
└── .gitignore


What Happens Internally

1. Initialization:
When the app starts, it checks for the database and creates the table if it doesn't exist:
```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT
    )
""")
```

2. Generating Short URL:
User enters:
https://google.com

The /shorten route runs:
* Generates a 6-character code using random letters and digits:
  short_code = generate_code()  # e.g., "Zrdiln"
* Inserts the mapping into SQLite:
  INSERT INTO urls (short_code, long_url) VALUES ("Zrdiln", "https://google.com")

Flask returns the clickable short URL:
http://localhost:5000/Zrdiln


3. Redirection:
User visits:
/Zrdiln

This route runs:
@app.route("/<short_code>")

Flask captures:
short_code = "Zrdiln"

Then:
* Queries the database:
  SELECT long_url FROM urls WHERE short_code = "Zrdiln"
* Fetches the database result:
  result = ("https://google.com",)
* Redirects the browser:
  return redirect(result[0])
