import os
import datetime
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_caching import Cache
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session



app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = b"123a123b456a"
app.config["SESSION_USE_SIGNER"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=5)

# Set up database
# Initialize app
app.wsgi_app = ProxyFix(app.wsgi_app)
cache = Cache(app)
Session(app)

@app.route("/")
def count_users():
    if session.get("count_users") is None:
        count = "0"
    else:
        count = session["count_users"]
    return count

@app.route("/<user>")
def user_in(user):
    session.modified = True
    if not session.get("users"):
        session["users"] = [user]
    elif user not in session["users"]:
        session["users"].append(user)
    elif user in session["users"]:
        return "Try again this name is already exist in session"

    if session.get("count_users") is None:
        session["count_users"] = "1"
    else:
        session["count_users"] = str(int(session["count_users"]) + 1)
    return f"Hello {user}"

@app.route("/del/<user>")
def del_user(user):
    if user in session.get("users"):
        session["count_users"] = str((session.get("count_users")) - 1)
        session["users"].pop(user)
    else:
        return f"Unknown {user} name"
    return redirect(url_for(count_users))

@app.route("/users_list")
def users_list():
    if session.get("users"):
        users_string = "\n".join([user for user in session["users"]])
    else:
        users_string = "Users list is empty"

    return users_string


if __name__ == "__main__":
    app.run(debug=True)
