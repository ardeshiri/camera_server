import time
import cv2
import flask
import base64
import json
from waitress import serve

class CamException(Exception):
    pass


class CamServer:
    def __init__(self, cam: int):
        self.cap = cv2.VideoCapture(cam)

    def set_wh(self, stt: dict):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, stt["width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, stt["height"])

    def send_frame(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                raise CamException()
            frame = cv2.resize(frame, [int(flask.request.args.get("width")), int(flask.request.args.get("height"))])
            if int(flask.request.args.get("channels")) == 1:
                sending_data = {
                    'frame_string': base64.b64encode(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)).decode("utf-8"),
                    "request_time": flask.request.args.get("request_time")
                }
            else:
                sending_data = {
                    'frame_string': base64.b64encode(frame).decode("utf-8"),
                    "request_time": flask.request.args.get("request_time")
                }
            return json.dumps(sending_data)
        except CamException:
            self.cap.release()

    def exit(self):
        self.cap.release()
        exit(0)


settings = {
    "width": 320,
    "height": 180
}
c = CamServer(0)
# c.set_wh(settings)
app = flask.Flask(__name__)
app.add_url_rule("/frontcam", "frontcam", c.send_frame)
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)