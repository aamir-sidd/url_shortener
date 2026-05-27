from flask import Flask, request, redirect

app = Flask(__name__)

urls = {}

@app.route('/')
def home():
    return """
    <form action="/shorten" method="POST">
        <input name="long_url" placeholder="Enter URL">
        <button type="submit">Shorten</button>
    </form>
    """

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form["long_url"]

    short_code = str(len(urls) + 1)

    urls[short_code] = long_url

    return f"""
    Short URL: 
    <a href="/{short_code}">
        http://localhost:5000/{short_code}
    </a>
    """

@app.route("/<short_code>")
def redirect_url(short_code):
    long_url = urls.get(short_code)

    if long_url:
        return redirect(long_url)

    return "URL not found"

if __name__ == "__main__":
    app.run(debug=True)