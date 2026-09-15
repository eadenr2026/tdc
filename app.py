import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from models import init_db, find_user, club_clips, create_clip, DATABASE
from models import create_user, find_all_clips
from werkzeug.security import generate_password_hash, check_password_hash
import re
app = Flask(__name__)

app.secret_key = "temporary-dev-key-change-me"

init_db()
club_clips()

def extract_twitch_slug(url):
    match = re.search(r'(?:clips\.twitch\.tv\/|twitch\.tv.\/\w+\/clip\/)([\w-]+)', url)
    if match:
        return match.group(1)
    return url.strip()

# Route to TDC Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route to TDC Registration Page
@app.route("/register", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)

        create_user(username, password_hash)

        return render_template("index.html")
    else:
        return render_template("register.html")

# Route to TDC login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = find_user(username)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

# URL profile logout
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))

# Route to Profile Page
@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")



# Submit clips
@app.route("/submit", methods=["GET", "POST"])
def upload_clip():
    if "user_id" not in session:
        return redirect(url_for("login"))
    elif request.method == "POST":
        url = request.form["create_clip"]
        user_id = session["user_id"]
        create_clip(user_id, url)
        return render_template("index.html")
    else:
        return render_template("submit.html")

@app.route("/clipboard", methods=["GET"])
def tha_clipboard():
    clips = find_all_clips()
    return render_template("clipboard.html", clips=clips)

# have to find out why clips default to jinja else loop


# Run App in Debug Mode
if __name__ == "__main__":
    app.run(debug=True)