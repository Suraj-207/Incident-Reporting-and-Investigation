from flask import request
from flask_restful import Resource
import config
from py_backend.jwt_token.token import Token
from py_backend.investigator.solve_incident import Incident


class DisplayAllIncidents(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                email = decoded_token['decoded_token']['email']
                return Incident(email).display_all_incidents()
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


class DisplayIncidentById(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            _id = request.get_json()['_id']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                email = decoded_token['decoded_token']['email']
                return Incident(email).display_incident(_id)
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


class EditIncident(Resource):

    def post(self):
        try:
            token = request.form['token']
            _id = request.form['_id']
            report = request.form['report']
            evidence = request.files['evidence']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                email = decoded_token['decoded_token']['email']
                return Incident(email).edit_incident(_id, report, evidence)
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}
