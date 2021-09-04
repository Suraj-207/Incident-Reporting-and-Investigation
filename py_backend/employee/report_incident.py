import config
from py_backend.image_handler.img_to_b64 import ImageConvert


class Incident:

    def __init__(self, email):
        self.email = email

    def add_new_incident(self, title, info, images):
        try:
            record = {
                "email": self.email,
                "title": title,
                "info": info,
                "images": ImageConvert().convert_to_b64(images),
                "approved": False,
                "completed": False,
                "investigator_email": None,
                "report": None,
                "evidence": []
            }
            return config.mongo_db.insert_one("incident", record)
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def display_incidents(self):
        try:
            return list(config.mongo_db.my_db['incident'].find({
                "email": self.email
            }))
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}


