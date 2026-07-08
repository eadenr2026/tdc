from flask import Flask, render_template, request
from models import init_db
from models import create_user
from werkzeug.security import generate_password_hash

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(debug=True)