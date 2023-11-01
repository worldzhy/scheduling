from typing import Any
from flask import jsonify

def handle_api_error(e: Any):
    error_message = str(e)
    if error_message:
        return jsonify({'message': f'An error occurred [new]: {error_message}'}), 500
    else:
        return jsonify({'message': 'An unknown error occurred.'}), 500