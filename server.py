from dotenv import load_dotenv
load_dotenv()

from src.app.Helper import handle_api_error
from src.app.Controller import Controller
from flask import Flask, jsonify, request

app = Flask(__name__)
controller = Controller()

# TO DO: Make the route accept specific params
@app.route('/schedule', methods=['POST'])
def post_schedule():
    try:
        return jsonify(controller.post_schedule()), 200
    except Exception as e:
        return handle_api_error(e)

@app.route('/v1/forecast', methods=['POST'])
def post_v1_forecast():
    try:
        return jsonify(controller.post_v1_forecast(request)), 200
    except Exception as e:
        return handle_api_error(e)
    
@app.route('/v2/forecast', methods=['POST'])
def post_v2_forecast():
    try:
        return jsonify(controller.post_v2_forecast(request)), 200
    except Exception as e:
        return handle_api_error(e)

@app.route('/studio', methods=['GET'])
def get_studio():
    try:
        return jsonify(controller.get_studio()), 200
    except Exception as e:
        return handle_api_error(e)
    
@app.route('/location', methods=['GET'])
def get_location():
    try:
        return jsonify(controller.get_location(request)), 200
    except Exception as e:
        return handle_api_error(e)

@app.route('/program', methods=['GET'])
def get_program():
    try:
        return jsonify(controller.get_program()), 200
    except Exception as e:
        return handle_api_error(e)
    
@app.route('/month', methods=['GET'])
def get_month():
    try:
        return jsonify(controller.get_month()), 200
    except Exception as e:
        return handle_api_error(e)

@app.route('/weekday', methods=['GET'])
def get_weekday():
    try:
        return jsonify(controller.get_weekday()), 200
    except Exception as e:
        return handle_api_error(e)

@app.route('/coach_tier', methods=['GET'])
def get_coach_tier():
    try:
        return jsonify(controller.get_coach_tier()), 200
    except Exception as e:
        return handle_api_error(e)

@app.route('/timeslot', methods=['GET'])
def get_timeslot():
    try:
        return jsonify(controller.get_timeslot_list()), 200
    except Exception as e:
        return handle_api_error(e)

if __name__ == '__main__':
    print('API Ready')
    from waitress import serve
    port = 8080
    serve(app, port = port)
