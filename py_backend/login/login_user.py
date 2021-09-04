from werkzeug.security import check_password_hash
import config
from py_backend.jwt_token.token import Token


class Validation:

    def __init__(self, email, password, role):
        try:
            self.email = email
            self.password = password
            self.role = role
        except Exception as e:
            config.logger.log("ERROR", str(e))

    def check(self):
        """

        :return: whether valid or not along with a new jwt.
        """
        try:
            if self.email is not None and self.password is not None:
                self.email = self.email.lower()
                result = config.mongo_db.my_db['users'].find({"_id": self.email, "role": self.role})[0]
                if result is None:
                    config.logger.log("CRITICAL", "Invalid Credentials")
                    return {"role": False, "message": "Invalid Credentials", "token": None}
                else:
                    if check_password_hash(result['password'], self.password):
                        token = Token().generate_token(self.email, self.role)
                        config.logger.log("INFO", "Login successful...")
                        return {"role": self.role, "message": "Login successful", "token": token}
                    else:
                        config.logger.log("WARNING", "Wrong password...")
                        return {"role": False, "message": "Wrong password", "token": None}
            else:
                return {"role": False, "message": "Please enter an email and password to log in", "token": None}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"role": False, "message": "Internal Server Error", "token": None}
