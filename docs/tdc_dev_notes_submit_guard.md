# TDC Dev Notes — Submit Route Login Guard

Session focus: adding a login guard to the clip submission route, plus a refresher on the core Flask concepts.

## What I built this session

Added a guard to the `/submit` route so a logged out visitor who reaches the URL gets redirected to login instead of hitting the page or crashing. The nav already hid the Submit tab from logged out users, but hiding a link only controls what someone can click, not what they can visit by typing the URL. The real protection has to live in the route on the backend.

Shipped it through the normal git loop on its own branch (`feature/submit-guard`), committed, pushed, PR, merged, synced main.

The finished guard, as the first lines of the route:

```python
@app.route("/submit", methods=["GET", "POST"])
def upload_clip():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        url = request.form["create_clip"]
        user_id = session["user_id"]
        create_clip(user_id, url)
        return render_template("index.html")
    else:
        return render_template("submit.html")
```

## Concepts to remember

**Frontend is not a security boundary.** Hiding a tab or button in HTML is convenience, not a lock. The browser is fully under the user's control, so they can navigate anywhere or edit the page. The only place a rule is actually enforced is the backend route, which runs on the server. Hide things in the template for UX, enforce them in the route for security. You need both.

**Guard goes at the very top of the route.** Check whether the user is logged in before touching anything in the session. If the check comes after you read `session["user_id"]`, it already crashed before the check ran. Putting the guard first also protects both GET and POST at once, since it runs before the method split.

**Checking the session safely.** Use `if "user_id" not in session:` to ask whether the key exists. Reading `session["user_id"]` directly crashes with a KeyError when the key is missing. This is a memorized idiom, not something to reason out.

**render_template vs redirect.** `render_template("page.html")` shows a page, used when someone needs to see HTML. `redirect(url_for("route_function"))` sends the browser to another route, used after an action. `redirect` takes a URL built from a function name, never a filename like "login.html".

**GET shows, POST redirects.** Someone visiting a page is a GET, so render the template. Someone who submitted a form or completed an action is a POST, so redirect them onward.

**Every route path needs a return.** If a path through the function ends without returning something, Flask throws "did not return a valid response." Make sure both the if and the else give the browser something back.

## Where TDC stands (v1)

Stack: Python and Flask, SQLite via sqlite3, HTML and Bootstrap 5 with Jinja templates, sessions and Werkzeug hashing, git and GitHub with a feature branch and PR workflow.

Shipped and merged:
- Registration (hashed passwords, SQLite)
- Login (session in, redirect)
- Logout (session cleared) plus conditional nav and welcome message
- Clip submission (writes a clip tied to the logged in user)
- Login guard on the submit route

Still to build in v1:
- Voting on clips (#3, adds a votes table, the last piece with new structure)
- Visitor views the clip board (#4)
- Visitor views the leaderboard (#5)
- Visitor views a member profile (#9)

Deferred to v2: profile editing and password change (#7).

The account system is done, which was the hardest and most security sensitive part. Three of the four remaining features are reads, meaning they query and display data that is already stored rather than adding new machinery.

## Note to self

Coming back after a break feels like starting over but it is not. The skills are there, the recall is just slow at first and speeds back up within a session. When re-entry feels heavy, open the project and reread one route out loud in plain English. That reloads the mental map without forcing a big push. Match the hard reasoning work to the days with energy, and give the tired days something small.

Next real step: voting (#3).
