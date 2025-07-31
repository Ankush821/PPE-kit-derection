from flask import Flask, render_template, request, Response, redirect, url_for, stream_with_context
import cv2
import os
from main import ppe_detection

app = Flask(__name__)

# Global variables
video_path = ""
detection_mode = "with_alert"  # default
alert_flag = {"status": False}  # Shared alert status for SSE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global video_path, detection_mode
    detection_mode = request.form.get('mode')
    input_source = request.form.get('input_source')  # Make sure HTML name is input_source

    if input_source == 'upload':
        video = request.files.get('video')
        if video and video.filename != '':
            video_path = os.path.join('static', 'uploads', video.filename)
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            video.save(video_path)
        else:
            video_path = 0  # fallback to webcam if no video uploaded
    else:
        video_path = 0  # webcam selected

    return redirect(url_for('video'))

def generate():
    global detection_mode, video_path, alert_flag
    for frame, alert in ppe_detection(video_path, detection_mode):
        alert_flag["status"] = alert  # update shared alert flag
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video():
    return render_template('result.html', mode=detection_mode)  # pass mode to template

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alert-stream')
def alert_stream():
    def event_stream():
        while True:
            yield f"data: {'alert' if alert_flag['status'] else 'noalert'}\n\n"
    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
