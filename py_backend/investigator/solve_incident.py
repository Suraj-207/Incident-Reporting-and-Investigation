import config


class Incident:

    def __init__(self, email):
        self.email = email

    def display_all_incidents(self):
        try:
            return list(config.mongo_db.my_db['incident'].find({
                "investigator_email": self.email
            }))
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def display_incident(self, _id):
        try:
            return config.mongo_db.my_db['incident'].find({
                "_id": _id
            })[0]
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


