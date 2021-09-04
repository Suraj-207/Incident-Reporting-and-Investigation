from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
import config
import os
from py_backend.logger.log_db import Logger
from py_backend.mongo_db.crud import Operations
from py_backend.signup.signup_api import Signup
from py_backend.login.login_api import Login
from py_backend.jwt_token.token_validation_api import IsValidToken
from py_backend.admin.manage_users_api import InsertUser, DeleteUser, UpdateUser, DisplayUser, DisplayAllUsers
from py_backend.employee.report_incident_api import AddIncident, DisplayIncident


app = Flask(__name__, template_folder='./py_backend/', static_url_path='', static_folder='./frontend/build')
CORS(app)
config.logger = Logger()
config.mongo_db = Operations("IncidentReportingAndInvestigation", config.logger)
api = Api(app)


@app.route('/', defaults={'path': ''})
def home_page(path):
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(Signup, '/api/signup')
api.add_resource(Login, '/api/login')
api.add_resource(IsValidToken, '/api/check-token')
api.add_resource(InsertUser, '/api/insert-user')
api.add_resource(UpdateUser, '/api/update-user')
api.add_resource(DeleteUser, '/api/delete-user')
api.add_resource(DisplayUser, '/api/display-user')
api.add_resource(DisplayAllUsers, '/api/display-all-users')
api.add_resource(AddIncident, '/api/add-incident')
api.add_resource(DisplayIncident, '/api/display-incident')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)