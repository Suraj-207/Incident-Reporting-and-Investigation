import config
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
from py_backend.signup.signup_user import Registration
import random


class Users:

    def __init__(self, admin_email):
        try:
            load_dotenv("py_backend/env/email_credentials.env")
            self.sender_email = os.getenv("EMAIL")
            self.sender_password = os.getenv("PASSWORD")
            self.admin_details = config.mongo_db.my_db['users'].find({"_id": admin_email, "role": 'admin'})[0]
        except Exception as e:
            config.logger.log("ERROR", str(e))

    def insert_user(self, record):
        try:
            default_password = str(random.randint(9999999, 100000000))
            data = {
                "email": record['email'],
                "password": generate_password_hash(default_password),
                "firstname": record['firstname'],
                "lastname": record['lastname'],
                "role": record['role'],
                "company": self.admin_details['company'],
                "branch": self.admin_details['branch']
            }
            from_ = "From: HSSERISK - IRAI <{}>\n".format(self.sender_email)
            to = "To: {} <{}>\n".format(record['firstname'] + " " + record['lastname'], record['email'])
            subject = "Subject: Registration in HSSERISK - IRAI successful\n\n"
            msg = "Welcome to HSSERISK - Incident Reporting and Investigation. You have been registered by" \
                  " {}, {}. \nEmail - {}\nPassword - {}\nRoles - {}\n\nDo not share it with anyone.  ".format(
                                                                                                    data['company'],
                                                                                                    data['branch'],
                                                                                                    record['email'],
                                                                                                    default_password,
                                                                                                    str(record['role']))
            message = from_ + to + subject + msg
            return Registration(data, message).insert_to_db()
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def update_user(self, email, record):
        try:
            condition = {
                "_id": email
            }
            new_val = {"$set": record}
            return config.mongo_db.update("users", condition, new_val)
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def delete_user(self, email):
        try:
            condition = {
                "_id": email
            }
            return config.mongo_db.delete("users", condition)
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def display_all_users(self):
        try:
            return list(config.mongo_db.my_db['users'].find({
                "company": self.admin_details['company'],
                "branch": self.admin_details['branch']
            }))
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def display_user(self, email):
        try:
            return config.mongo_db.my_db['users'].find({
                "_id": email
            })[0]
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}
