import CameraServer
import flask
from waitress import serve

settings = {
    "width": 320,
    "height": 180
}
c = CameraServer.CamServer(0)
# c.set_wh(settings)
app = flask.Flask(__name__)
app.add_url_rule("/frontcam", "frontcam", c.send_frame)
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
