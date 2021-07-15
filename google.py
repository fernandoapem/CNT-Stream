import os
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = "66309064423-a1hi759ud0p2pgms0pm9cul2re55b73p.apps.googleusercontent.com"
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "MIHGs8MvVUdD488Ph1GAxi1Y"
google_bp = make_google_blueprint(scope=["profile", "email"])
app.register_blueprint(google_bp, url_prefix="/login")


@app.route("/")
def index():
    if not google.authorized:
        return render_template("main.html")
    return "hi"

@app.route("/signup")
def signup():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return render_template("stream.html")


