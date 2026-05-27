How this version1 works-
In this version we simply ask user to enter the URL and we generate a short code for the URL and store it in a dictionary and then we redirect the user to the short URL.


What Happens Internally
User enters:
https://google.com


The /shorten route runs:

short_code = str(len(urls) + 1)

If dictionary empty:

short_code = "1"

Then:

urls["1"] = "https://google.com"


User visits:
/1

This route runs:

@app.route("/<short_code>")

Flask captures:

short_code = "1"

Then:

long_url = urls.get("1")

Then:

return redirect(long_url)

Browser gets redirected.


