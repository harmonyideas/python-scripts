import os
import uuid
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
from tasks import read_csv_task
from main import create_app

app = create_app()
app.clients = {}

# Configure CORS in case upload form is hosted elsewhere externally
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Set SocketIO to connect to message queue (optional)
socketio = SocketIO(app, message_queue=app.config["MESSAGE_QUEUE"])


# Define a helper function to check if a file is allowed
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


# Define defautl route
@app.route("/", methods=["GET", "POST"])
@cross_origin()
def home():
    """
    Here, the server responds to the default route with a message
    """
    if request.method == "GET":
        return render_template("index.html")
    return redirect(url_for("index"))


# Define a route to handle file uploads
@app.route("/upload", methods=["POST", "GET", "OPTIONS"])
@cross_origin()
def upload():
    """
    Handle file uploads and submit them to Celery tasks

    Returns:
        JSON object with a list of task IDs
    """

    if request.method != "POST":
        return redirect(url_for("index"))

    # Get the uploaded files
    uploaded_files = request.files.getlist("file")

    # Get the URL of the event endpoint
    url = url_for("event", _external=True)

    # Get the user ID
    userid = request.form.get("userid")

    # Iterate over the uploaded files and submit them to Celery tasks
    taskid = []
    for index, file in enumerate(uploaded_files):
        if allowed_file(file.filename):
            filename = request.form.get(f"file_uploads[{index}].name")
            filejobid = request.form.get(f"file_uploads[{index}].jobid")
            progressid = request.form.get(f"file_uploads[{index}].progressid")
            path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
            file.save(path)

            # Submit the file to a Celery task
            file_task = read_csv_task.apply_async(
                args=[filejobid, progressid, userid, url, path]
            )

            # Add the task ID to the list of task IDs to return to the client
            taskid.append(str(file_task.task_id))

    # Return the list of task IDs to the client
    return jsonify({"taskid": taskid}), 202


# Define a route to handle event messages
@app.route("/event/", methods=["POST"])
def event():
    """
    Handle event messages from Celery tasks

    Returns:
        String "ok" if the message was handled successfully, or "error" otherwise
    """

    # Get the user ID from the message
    userid = request.json["userid"]

    # Get the data from the message
    data = request.json

    # Get the namespace for the user
    ns = app.clients.get(userid)
    # Emit the event to the client
    if ns and data:
        socketio.emit("celerystatus", data, namespace=ns)
        return "ok"
    return "error", 404


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
