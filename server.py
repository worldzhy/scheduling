from src.app.Helper import handle_api_error
from src.app.Controller import Controller
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
controller = Controller()

# TO DO: Make the route accept specific params
@app.route('/schedule', methods=['POST'])
def post_schedule():
    try:
        return jsonify(controller.schedule()), 200
    except Exception as e:
        return handle_api_error(e)

@app.route('/forecast', methods=['POST'])
def post_forecast():
    try:
        return jsonify(controller.forecast(request)), 200
    except Exception as e:
        return handle_api_error(e)

if __name__ == '__main__':
    print('API Ready')
    from waitress import serve
    port = 8080
    serve(app, port = port)