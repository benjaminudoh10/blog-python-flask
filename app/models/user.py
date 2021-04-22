import json
from datetime import datetime

from flask_login import UserMixin

from . import db, BaseModel


class User(BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sub = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_pic = db.Column(db.String)
    articles = db.relationship('Article', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_sub(cls, sub):
        return cls.query.filter_by(sub=sub).first()

    @classmethod
    def get_or_create(cls, user_json):
        user = cls.get_by_sub(user_json['sub'])
        if not user:
            cls.insert(user_json)
            user = cls.get_by_sub(user_json['sub'])

        return user

    @classmethod
    def insert(cls, user):
        user = cls(**user)
        db.session.add(user)
        db.session.commit()
        return cls

    @classmethod
    def to_json(cls, data):
        if isinstance(data, cls):
            return {
                'id': data.id,
                'sub': data.sub,
                'name': data.name,
                'email': data.email,
                'profile_pic': data.profile_pic,
                'created_at': datetime.strftime(data.created_at, '%a %d, %Y'),
                'updated_at': data.updated_at.isoformat(),
            }
        elif isinstance(data, list):
            return list(map(cls.to_json, data))
