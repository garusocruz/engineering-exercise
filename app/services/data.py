from datetime import datetime
from domains.models.data import Data


class DataService:
    @classmethod
    def get_all(cls, filters: dict = {}):
        return {"items": Data.get_all(filters)}

    @classmethod
    def get_by_id(cls, id):
        data = Data.get_by_id(id)
        if not data:
            return {"message": "Data not found"}, 404
        return data

    @classmethod
    def create(cls, data):
        url = data.get("url")
        title = data.get("title")
        date_added = (
            data.get("date_added") if data.get("date_added") else datetime.now()
        )
        if not url or not title or not date_added:
            return {"message": "Missing required field(s)"}, 400

        return Data.create(url, title, date_added)
