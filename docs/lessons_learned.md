# TDC Lessons Learned

A living list of things I learned the hard way while building this project. Reread before starting a session. Add a line whenever something bites me.

## Debugging

**Ask which layer first.** The app has layers: browser, Flask (app.py), models (models.py), sqlite3, the database file. When something breaks, figure out which layer before diving in. Wrong or missing data points to the data layer even when the symptom shows up in a route. I once spent an evening staring at the login route when the bug was a bad SELECT in the model.

**Read the error message literally.** The traceback usually names the exact problem. "Did not return a valid response" meant a path with no return, not the bug I assumed I had. Read what it actually says before guessing based on what I most recently changed.

**A bug that throws no error is the sneakiest.** `create_user` once ran clean but saved nothing because it was missing `connection.commit()`. No crash, no message, just silently did nothing. When something "works" but the result is missing, suspect a missing commit or a step that never ran.

**Reads don't commit, writes do.** SELECT queries just read, so no commit needed. INSERT, UPDATE, DELETE change data, so they need `connection.commit()` before `close()` or the change never lands on disk.

## Flask patterns

**render_template shows a page, redirect sends to a URL.** Use render_template when someone needs to see HTML. Use redirect after an action to move them onward. redirect takes a URL from `url_for("function_name")`, never a filename like "login.html". This one bit me more than once.

**GET shows, POST redirects.** A visit is a GET, so render the page. A form submission or completed action is a POST, so redirect.

**Every route path needs a return.** If any branch reaches the end without returning something, Flask errors. Check that both the if and the else hand back a response.

**Check the session before using it.** Use `if "user_id" not in session:` to test whether the key exists. Reading `session["user_id"]` directly crashes when it is missing. Put login guards at the very top of the route, before touching the session, so they run before anything can crash and protect both GET and POST at once.

## Database and schema

**IF NOT EXISTS ignores schema changes.** A CREATE TABLE with IF NOT EXISTS only builds the table if it does not already exist. So editing the columns or constraints in my code does nothing to a table that is already on disk. It just gets skipped on the next run. To apply a schema change while the data is throwaway, delete the table (or the whole tdc.db file) and let the app rebuild it fresh. This is the same constraint that makes the table safe to recreate on every startup and the reason schema edits silently do nothing.

**Migrations exist for changing tables without losing data.** Deleting the database to change a table only works because my data is throwaway right now. Once real people use the site, I can never just delete it. Changing a table's structure while keeping its data is what migrations are for. Not needed yet, but that is why they exist.

**UNIQUE can span more than one column.** A single column can be UNIQUE, like username. But uniqueness can also apply to a combination, written as its own line like `UNIQUE (user_id, clip_id)`. That means the pair must be unique even though each column repeats freely on its own. This is what stops one user voting on the same clip twice.

**Trust the database, not the viewer.** The PyCharm viewer's column panel shows column names and types but not table-level constraints like UNIQUE or foreign keys. Not seeing UNIQUE in the panel does not mean it is missing. To check for real, view the table's DDL or run `SELECT sql FROM sqlite_master WHERE name = 'table_name';` to see the exact CREATE TABLE text. The behavioral test is the real proof: try to violate the constraint and confirm it throws an IntegrityError.

## Security

**Frontend is not a security boundary.** Hiding a tab or button in HTML controls what a user can click, not what they can visit by typing the URL. Enforce access rules in the backend route. Hide in the template for UX, guard in the route for security. Need both.

**Never trust the client for identity.** Get the user_id from the session, not from the form. The form can be forged. The session was set by the server at login.

**Always use parameterized queries.** Use `?` placeholders with a tuple of values, never build SQL by inserting user input into the string. This is the defense against SQL injection.

## Workflow and mindset

**Tutorials optimize for showing features, not for my project.** A tutorial had me add Flask-Session (server side sessions) when built in cookie sessions were plenty. Adopt what fits, skip what doesn't, and know why I am adding any dependency.

**The same small mistakes recur until muscle memory forms.** The redirect-vs-filename mistake, mashed-together terminal commands, forgetting a return. Repeating them is not failure, it is the reps that build the instinct. The instinct forms from correcting the mistake, not from avoiding it.

**Commit changes to the branch they belong to.** Unrelated improvements should not ride along on a feature branch. Glance at the branch indicator before starting to type. If an idea belongs elsewhere, branch for it.

**Features have an order, and finding it is part of the work.** I could not test voting because there was no page showing clips to vote on. Voting (#3) depends on the clip board page (#4). Some features have hidden dependencies, so figure out the build order before diving in rather than getting stuck halfway.

**Coming back after a break feels like starting over but is not.** The skills are there, the recall is just slow and speeds back up within a session. Reread one route out loud in plain English to reload the mental map. Match hard reasoning to high energy days, give tired days something small.
