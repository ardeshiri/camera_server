import time
import cv2
import flask
import base64
import json
import threading


class CamException(Exception):
    pass


class Cam:
    def __init__(self, cam: int):
        self.cap = cv2.VideoCapture(cam)
        self.lock = threading.Lock()
        self.current_frame = None

    def set_wh(self, stt: dict):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, stt["width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, stt["height"])

    def get_frame(self):
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    raise CamException()
                with self.lock:
                    self.current_frame = frame
                time.sleep(0.07)
        except CamException:
            self.cap.release()

    def send_frame(self):
        with self.lock:
            tmp_frame = self.current_frame
        tmp_frame = cv2.resize(tmp_frame, [int(flask.request.args.get("width")), int(flask.request.args.get("height"))])
        if int(flask.request.args.get("channels")) == 1:
            sending_data = {
                'frame_string': base64.b64encode(cv2.cvtColor(tmp_frame, cv2.COLOR_BGR2GRAY)).decode("utf-8"),
                "request_time": flask.request.args.get("request_time")
            }
        else:
            sending_data = {
                'frame_string': base64.b64encode(tmp_frame).decode("utf-8"),
                "request_time": flask.request.args.get("request_time")
            }
        return json.dumps(sending_data)

    def exit(self):
        self.cap.release()
        exit(0)


settings = {
    "width": 320,
    "height": 180
}
app = flask.Flask(__name__)
c = Cam(0)
c.set_wh(settings)
thr = threading.Thread(target=c.get_frame)
thr.start()
app.add_url_rule("/frontcam", "frontcam", c.send_frame)
app.run()