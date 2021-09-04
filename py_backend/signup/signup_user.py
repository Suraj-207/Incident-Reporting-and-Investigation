from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv
import config
from py_backend.mail_automation.mail import SendMail


class Registration:

    def __init__(self, record, message=None):
        try:
            load_dotenv("py_backend/env/email_credentials.env")
            self.sender_email = os.getenv("EMAIL")
            self.sender_password = os.getenv("PASSWORD")
            self.user_data = {
                "_id": record['email'].lower(),
                "firstname": record['firstname'],
                "lastname": record['lastname'],
                "password": generate_password_hash(record['password']),
                "role": record['role'],
                "company": record['company'],
                "branch": record['branch']
            }
            from_ = "From: HSSERISK - IRAI <{}>\n".format(self.sender_email)
            to = "To: {} <{}>\n".format(record['firstname'] + " " + record['lastname'], record['email'])
            subject = "Subject: Registration in HSSERISK - IRAI successful\n\n"
            msg = "Welcome to HSSERISK - Incident Reporting and Investigation. We are pleased to welcome " \
                  "{}, {} to our community. ".format(record['company'], record['branch'])
            self.message = from_ + to + subject + msg
            if message is not None:
                self.message = message
        except Exception as e:
            config.logger.log("ERROR", str(e))

    def insert_to_db(self):
        try:
            check_existence = config.mongo_db.my_db['users'].find({"_id": self.user_data['_id']})
            if len(list(check_existence)) == 0:
                check_email = SendMail(self.sender_email, self.sender_password, self.user_data['_id'],
                                       self.message).send()
                if check_email:
                    res = config.mongo_db.insert_one("users", self.user_data)
                    return res
                else:
                    return {"status": False, "message": "Invalid email"}
            else:
                return {"status": False, "message": "User already exists"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}
