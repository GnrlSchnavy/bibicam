from flask import Flask, render_template, Response
import os

machine = os.uname().machine


def onPi():
    return machine == "armv7l"


if onPi():
    from campera import PiCamera
    pi_camera = PiCamera(flip=False)  # flip pi camera if upside down.
else:
    import cv2
    pi_camera = cv2.VideoCapture(0)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')  # you can customze index.html here


def gen(camera):
    while True:
        if onPi():
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            success, frame = camera.read()  # read the camera frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
