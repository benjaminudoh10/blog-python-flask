import json
from datetime import datetime

from . import db, BaseModel
from .user import User


class Comment(BaseModel):
    '''
    This model describes an article.
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get(cls, id):
        comment = cls.query.get(id)
        return cls.to_json(comment)

    @classmethod
    def get_comments(cls, article_id, page=1):
        comments = cls.query.filter_by(deleted_at=None) \
            .order_by(cls.updated_at.desc()) \
            .offset((page - 1) * 10).limit(10).all()
        return cls.to_json(comment)

    @classmethod
    def insert(cls, comment):
        comment = cls(**comment)
        db.session.add(comment)
        db.session.commit()
        return cls.to_json(comment)

    @classmethod
    def update(cls, id, data):
        comment = cls.query.get(id)
        comment.comment = data['comment']
        comment.updated_at = datetime.now()
        db.session.add(comment)
        db.session.commit()
        return cls.to_json(comment)
    
    @classmethod
    def delete(cls, id):
        comment = cls.query.get(id)
        comment.deleted_at = datetime.now()
        db.session.add(comment)
        db.session.commit()

    @classmethod
    def to_json(cls, data):
        if isinstance(data, cls):
            return {
                'id': data.id,
                'comment': data.comment,
                'user': User.to_json(data.user),
                'created_at': datetime.strftime(data.created_at, '%a %d, %Y'),
                'updated_at': data.updated_at.isoformat(),
            }
        elif isinstance(data, list):
            return list(map(cls.to_json, data))
