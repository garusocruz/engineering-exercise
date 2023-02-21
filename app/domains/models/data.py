import re
from datetime import datetime
from flask import current_app
from sqlalchemy import or_, and_
from main import server

with server.app_context():
    db = current_app.config.get("DB")


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "date_added": self.date_added,
        }

    @classmethod
    def get_all(cls, filters: dict = {}):
        # build the filter expressions using SQLAlchemy
        filter_expressions = []

        if filters:
            if "after_date" in filters:
                filter_expressions.append(Data.date_added >= filters["after_date"])
            if "before_date" in filters:
                filter_expressions.append(Data.date_added <= filters["before_date"])
            if "title" in filters:
                filter_expressions.append(
                    or_(
                        Data.title.like(f'%{filters["title"]}%'),
                        Data.title.ilike(f'%{filters["title"]}%'),
                    )
                )
            if "url" in filters:
                filter_expressions.append(
                    or_(
                        Data.url.like(f'%{filters["url"]}%'),
                        Data.url.ilike(f'%{filters["url"]}%'),
                    )
                )
            if "between_dates" in filters:
                filter_expressions.append(
                    Data.date_added.between(
                        filters["between_dates"][0], filters["between_dates"][1]
                    )
                )

        if filter_expressions:
            response = [
                d.to_dict() for d in Data.query.filter(and_(*filter_expressions)).all()
            ]
        else:
            response = [d.to_dict() for d in cls.query.all()]

        return response

    @classmethod
    def get_by_id(cls, id):
        data = cls.query.filter_by(id=id).first()
        return data.to_dict() if data else None

    @classmethod
    def create(cls, url, title, date_added):
        data = cls(url=url, title=title, date_added=date_added)
        db.session.add(data)
        db.session.commit()

        return data.to_dict()
