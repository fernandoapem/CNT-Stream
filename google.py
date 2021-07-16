import os
from flask import Flask, redirect, url_for, render_template, Response
from flask_dance.contrib.google import make_google_blueprint, google
import cv2

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
google_bp = make_google_blueprint(scope=["profile", "email"])
app.register_blueprint(google_bp, url_prefix="/login")

############
# Camera Stuff
#############
camera = cv2.VideoCapture('http://ed50265e2ecc.ngrok.io') # <--------- Insert NGROK link in here
def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route("/")
def index():
    if not google.authorized:
        return render_template("main.html")
    return "hi"

@app.route("/login")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return "Success"


#####
# Stream routes
#####

@app.route("/stream")
def stream():
    return render_template('stream.html')

@app.route("/stream/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')