from datetime import datetime
from flask import Blueprint, jsonify, request
from services.data import DataService

bp = Blueprint("data", __name__)


@bp.route("/data", methods=["GET"])
def get_data():
    query_params = request.args.to_dict()

    # extract and parse filters from query params
    filters = {}
    after_date = query_params.get("after")
    before_date = query_params.get("before")
    between_date = query_params.get("between")
    title = query_params.get("title")
    url = query_params.get("url")

    if after_date:
        filters["after_date"] = datetime.strptime(after_date, "%Y-%m-%d").date()
    if before_date:
        filters["before_date"] = datetime.strptime(before_date, "%Y-%m-%d").date()
    if between_date:
        between_dates = between_date.split(":")
        filters["between_dates"] = [
            datetime.strptime(d, "%Y-%m-%d") for d in between_dates
        ]
    if title:
        filters["title"] = title
    if url:
        filters["url"] = url

    return jsonify(DataService.get_all(filters))


@bp.route("/data/<int:id>", methods=["GET"])
def get_data_by_id(id):
    return jsonify(DataService.get_by_id(id))


@bp.route("/data", methods=["POST"])
def create_data():
    url = request.json.get("url")
    title = request.json.get("title")
    if not url or not title:
        return jsonify({"error": "url and title are required fields"}), 400
    data = DataService.create(request.json)
    return jsonify(data)
