from flask import request
from flask_restful import Resource
from py_backend.employee.report_incident import Incident
import config
from py_backend.jwt_token.token import Token


class AddIncident(Resource):

    def post(self):
        try:
            token = request.form['token']
            title = request.form['title']
            info = request.form['info']
            images = request.files['images']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                email = decoded_token['decoded_token']['email']
                return Incident(email).add_new_incident(title, info, images)
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


class DisplayIncident(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                email = decoded_token['decoded_token']['email']
                return Incident(email).display_incidents()
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}