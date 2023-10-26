""" Setup Flask routes to to process file uploads using celery  """
from __future__ import absolute_import
from gevent import monkey

monkey.patch_all()
import os
import uuid
import logging
import time
from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    render_template,
    url_for,
    session,
    current_app,
)
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from tasks import read_task
from main import create_app

app = create_app()
app.clients = {}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# configure cors in case upload form is hosted elsewhere externally)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# set SocketIO to connect to message queue (optional)
socketio = SocketIO(app, message_queue=app.config["MESSAGE_QUEUE"])


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def home():
    """
    Here, the server responds to the default route with a message
    """
    if request.method == "GET":
        return render_template("index.html")
    return redirect(url_for("index"))


@app.route("/upload", methods=["POST", "GET", "OPTIONS"])
@cross_origin()
def upload():
    """
    Uploads a file to the server and starts a Celery task to process it.

    Returns:
        A JSON response with the IDs of the started Celery tasks.
    """

    if request.method != "POST":
        return redirect(url_for("index"))

    uploaded_files = request.files.getlist("file")
    url = url_for("event", _external=True)
    userid = request.form.get("userid")

    task_ids = []
    for index, file in enumerate(uploaded_files):
        if allowed_file(file.filename):
            filename = request.form.get(f"file_uploads[{index}].name")
            filejobid = request.form.get(f"file_uploads[{index}].jobid")
            progressId = request.form.get(f"file_uploads[{index}].progressId")
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
            file.save(filepath)

            file_task = read_task.apply_async(
                args=[filejobid, progressId, userid, url, filepath]
            )
            task_ids.append(str(file_task.task_id))

    return jsonify({"task_ids": task_ids}), 202


@app.route("/clients", methods=["GET"])
def clients():
    """
    Here, the server responds with a list of connected clients
    """
    return jsonify(list({"clients": app.clients.keys()}))


@app.route("/event/", methods=["POST"])
def event():
    """
    Here, the server handles event messages for our file task
    """
    userid = request.json["userid"]
    data = request.json
    ns = app.clients.get(userid)
    # Emit the event to the client
    if ns and data:
        socketio.emit("celerystatus", data, namespace=ns)
        return jsonify({"status":"ok"}), 200
    return jsonify({"status":"error"}), 404


@socketio.on("status", namespace="/events")
def events_message(message):
    emit("status", {"status": message["status"]})


@socketio.on("disconnect request", namespace="/events")
def disconnect_request():
    emit("status", {"status": "Disconnected!"})
    disconnect()


@socketio.on("connect", namespace="/events")
def events_connect():
    userid = str(uuid.uuid4())
    session["userid"] = userid
    current_app.clients[userid] = request.namespace
    emit("userid", {"userid": userid})
    emit("status", {"status": "Connection established", "userid": userid})


@socketio.on("disconnect", namespace="/events")
def events_disconnect():
    del current_app.clients[session["userid"]]
    print(f"Client {session['userid']} disconnected")


if __name__ == "__main__":
    socketio.run(port=8982, debug=True, host="0.0.0.0")

