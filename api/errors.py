from flask import jsonify
from http_status import HttpStatus

def error_response(status_code, message=None):
    payload = {'error': status_code}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(HttpStatus.bad_request_400.value, message)
