import unittest
import json
import dateutil.parser
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, patch

from flask import Flask
from werkzeug.datastructures import ImmutableMultiDict

from controllers.data import bp
from services.data import DataService

date_added: date = date(2021, 1, 1)


class DataRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(bp)
        self.client = self.app.test_client()

    @patch.object(DataService, "get_all", return_value=["data1", "data2"])
    def test_get_data_with_missing_filters(self, mock_get_all):
        with self.app.test_request_context("/data"):
            response = self.client.get("/data")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.get_json(),
                ["data1", "data2"],
            )
            mock_get_all.assert_called_with({})

    @patch.object(
        DataService,
        "get_all",
        return_value=[
            {
                "title": "how to train a dragon",
                "url": "http://test.com",
                "date_added": "Fri, 01 Jan 2021 00:00:00 GMT",
            }
        ],
    )
    def test_get_data_with_filters(self, mock_get_all):
        with self.app.test_request_context("/data"):
            response = self.client.get(
                f"/data?title=a&url=h&after={date_added}&before={date_added}&between={date_added}:{date_added + timedelta(seconds=1)}"
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.get_json()[0],
                {
                    "date_added": "Fri, 01 Jan 2021 00:00:00 GMT",
                    "title": "how to train a dragon",
                    "url": "http://test.com",
                },
            )

    @patch.object(
        DataService,
        "get_by_id",
        return_value={
            "title": "how to train a dragon",
            "url": "http://test.com",
            "date_added": "Fri, 01 Jan 2021 00:00:00 GMT",
        },
    )
    def test_get_data_by_id(self, mock_get_by_id):
        with self.app.test_request_context("/data/1"):
            response = self.client.get("/data/1")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.get_json(),
                {
                    "date_added": "Fri, 01 Jan 2021 00:00:00 GMT",
                    "title": "how to train a dragon",
                    "url": "http://test.com",
                },
            )

    @patch.object(
        DataService,
        "create",
        return_value={
            "id": 1,
            "url": "http://test.com",
            "title": "test",
            "date_added": date_added,
        },
    )
    def test_create_data(self, mock_create):
        data = {
            "url": "http://test.com",
            "title": "test",
            "date_added": date_added.isoformat(),
        }
        response = self.client.post(
            "/data", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "date_added": "Fri, 01 Jan 2021 00:00:00 GMT",
                "id": 1,
                "title": "test",
                "url": "http://test.com",
            },
        )

    @patch.object(
        DataService,
        "create",
        return_value={},
    )
    def test_create_data_missing_fields(self, mock_create):
        data = {}
        response = self.client.post(
            "/data", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "url and title are required fields"},
        )
