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
        username = session["username"]

        if "twitch.tv" in url and "/clip/" in url:
            create_clip(user_id, username, url)
            return render_template("index.html")
        else:
            return render_template("submit.html")
    else:
        return render_template("submit.html")

@app.route("/clipboard", methods=["GET"])
def tha_clipboard():

    clips = find_all_clips()
    clips_with_embeds = []

    for clip in clips:
        clip_dict = dict(clip)
        ttv_clip_url = clip_dict["url"]

        ttv_id1 = ttv_clip_url.rpartition("/")[2]
        ttv_id2 = ttv_clip_url.rstrip("/").rpartition("/")[2]

        clip_dict["embed_url"] = f"https://clips.twitch.tv/embed?clip={ttv_id1}&parent=127.0.0.1"

        clips_with_embeds.append(clip_dict)



    return render_template("clipboard.html", clips=clips_with_embeds)

# Run App in Debug Mode
if __name__ == "__main__":
    app.run(debug=True)