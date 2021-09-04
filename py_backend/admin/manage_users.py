import config
from py_backend.mail_automation.mail import SendMail
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
from py_backend.signup.signup_user import Registration


class Users:

    def __init__(self):
        load_dotenv("py_backend/env/email_credentials.env")
        self.sender_email = os.getenv("EMAIL")
        self.sender_password = os.getenv("PASSWORD")

    def insert_user(self, admin_email, record):
        admin_details = config.mongo_db.my_db['users'].find({"_id": admin_email, "role": 'admin'})[0]
        data = {
            "email": record['email'],
            "password": generate_password_hash("password"),
            "firstname": record['firstname'],
            "lastname": record['lastname'],
            "role": record['role'],
            "company": admin_details['company'],
            "branch": admin_details['branch']
        }
        from_ = "From: HSSERISK - IRAI <{}>\n".format(self.sender_email)
        to = "To: {} <{}>\n".format(record['firstname'] + " " + record['lastname'], record['email'])
        subject = "Subject: Registration in HSSERISK - IRAI successful\n\n"
        msg = "Welcome to HSSERISK - Incident Reporting and Investigation. You have been registered by" \
              "{}, {}. \nEmail - {}\nPassword - {}\n\nDo not share it with anyone.  ".format(record['company'],
                                                                                             record['branch'],
                                                                                             record['email'],
                                                                                             'password')
        message = from_ + to + subject + msg
        return Registration(data, message).insert_to_db()

    def update_user(self, email, record):
        condition = {"_id": email}
        new_val = {"$set": record}
        return config.mongo_db.update("users", condition, new_val)





