from flask import Blueprint, jsonify, Response, render_template
import ctypes
import mss
import io
from PIL import Image
import time

system_routes = Blueprint('system_routes', __name__)

@system_routes.route('/sleep', methods=['POST'])
def sleep_pc():
    try:
        # Put Windows PC to sleep
        ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
        return jsonify({'status': 'success', 'message': 'PC is going to sleep'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@system_routes.route('/health')
def health_check():
    # If the server responds, it's alive.
    return jsonify({'status': 'online', 'message': 'System is running'})

def gen_frames():
    with mss.mss() as sct:
        # Monitor 1 is usually the 'all in one' monitor
        monitor = sct.monitors[1]
        while True:
            # Capture the screen
            sct_img = sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Save to buffer as JPEG
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=50)
            frame = buffer.getvalue()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            # Limit frame rate
            time.sleep(0.1)

@system_routes.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@system_routes.route('/screen')
def view_screen():
    return render_template('screen_share.html')
