from flask import Flask, render_template, request, redirect, url_for, session
from models import init_db, find_user
from models import create_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "temporary-dev-key-change-me"

init_db()

# Route to TDC Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route to TDC Registration Page
@app.route("/register", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        password_hash = generate_password_hash(password)

        create_user(username, password_hash)

        return render_template("index.html")
    else:
        return render_template("register.html")

# Route to TDC login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]

        user = find_user(username)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            print(f"login success. Welcome to Tha Club, {username}")
            return redirect(url_for("home"))
        else:
            return redirect("login.html")
    else:
        return render_template("login.html")

# Run Application
if __name__ == "__main__":
    app.run(debug=True)