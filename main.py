from flask import Flask, render_template, request
from file_routes import file_browser
from system_routes import system_routes

app = Flask(__name__)
app.register_blueprint(file_browser)
app.register_blueprint(system_routes)

@app.before_request
def log_request_info():
    # Log IP address of the caller
    print(f"Connection from: {request.remote_addr} -> {request.method} {request.path}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
