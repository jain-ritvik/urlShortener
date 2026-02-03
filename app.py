from flask import Flask, render_template, redirect, url_for, request
import random
import string

app = Flask(__name__)

url_map = {}

@app.route('/', methods=["GET", "POST"])
def home():
    short_url = None
    if request.method == "POST":
        url = request.form["url"]
        print("url :", url)
        if not url.startswith("http://") and not url.startswith('https://'):
            return "Invalid URL"
        # return f"You entered: {url}"
    
        newurl= generate_short_code()
        url_map[newurl] = url
        short_url = request.host_url  + newurl
    return render_template('index.html', short_url=short_url)

@app.route('/<newurl>')
def redirect_url(newurl):
    original_url = url_map.get(newurl)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

if __name__ == "__main__":
    app.run(debug=True)