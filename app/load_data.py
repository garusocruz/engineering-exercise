import json
import dateutil.parser
from datetime import datetime
from flask import current_app
from services.data import DataService
from main import server


with server.app_context():
    db = current_app.config.get("DB")

    def import_data():
        with open("data.json", "r") as f:
            data = json.load(f)

        for item in data["items"]:
            data_json = {
                "url": item["url"],
                "title": item["title"],
                "date_added": dateutil.parser.parse(item["date_added"]),
            }

            print(f"Created: {DataService.create(data_json)}")

    if __name__ == "__main__":
        import_data()
