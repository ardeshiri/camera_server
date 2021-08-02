import cv2
import flask
import base64
import json

cap = cv2.VideoCapture(0)
width = 320
height = 180
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
app = flask.Flask(__name__)

@app.route("/frontcam")
def return_frame():
    ret, frame = cap.read()
    if not ret:
        print("error")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_text = base64.b64encode(gray)
    sending_data = {
        'frame_string':frame_text.decode("utf-8"),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'channels': 1
    }
    return json.dumps(sending_data)


@app.route("/exit")
def exit_all():
    cap.release()
    exit(0)

app.run(host="0.0.0.0", port=5000)
