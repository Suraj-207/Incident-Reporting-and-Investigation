import config
from py_backend.image_handler.img_to_b64 import ImageConvert


class Incident:

    def __init__(self, email):
        self.email = email

    def display_all_incidents(self):
        try:
            return list(config.mongo_db.my_db['incident'].find({
                "investigator_email": self.email,
                "approved": True
            }))
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def display_incident_by_id(self, _id):
        try:
            return config.mongo_db.my_db['incident'].find({
                "_id": _id
            })[0]
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def edit_incident(self, _id, report, evidence):
        try:
            new_val = {"_id": _id}
            condition = {"$set": {"report": report}, "$push": {"evidence": ImageConvert().convert_to_b64(evidence)}}
            return config.mongo_db.update("incident", new_val, condition)
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}
