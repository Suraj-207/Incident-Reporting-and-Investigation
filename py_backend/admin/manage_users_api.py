from flask import request
from flask_restful import Resource
from py_backend.admin.manage_users import Users
import config
from py_backend.jwt_token.token import Token


class InsertUser(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            record = request.get_json()['record']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                admin_email = decoded_token['decoded_token']['email']
                return Users(admin_email).insert_user(record)
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


class UpdateUser(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            email = request.get_json()['email']
            record = request.get_json()['record']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                admin_email = decoded_token['decoded_token']['email']
                return Users(admin_email).update_user(email, record)
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


class DeleteUser(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            email = request.get_json()['email']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                admin_email = decoded_token['decoded_token']['email']
                return Users(admin_email).delete_user(email)
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


class DisplayAllUsers(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            email = request.get_json()['email']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                admin_email = decoded_token['decoded_token']['email']
                return Users(admin_email).display_user(email)
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


class DisplayUser(Resource):

    def post(self):
        try:
            token = request.get_json()['token']
            decoded_token = Token().validate_token(token)
            if decoded_token['valid']:
                admin_email = decoded_token['decoded_token']['email']
                return Users(admin_email).display_all_users()
            else:
                return {"status": False, "message": "Invalid Token"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}