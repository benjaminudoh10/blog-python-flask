import json
from datetime import datetime

from ..parser import BlogContentParser
from . import db, BaseModel
from .comment import Comment


class Article(BaseModel):
    '''
    This model describes an article.
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    first_paragraph = db.Column(db.String)
    content = db.Column(db.Text, nullable=False)
    draft = db.Column(db.Boolean, nullable=True, default=True)
    comments = db.relationship('Comment', backref='article', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get(cls, id, convert_to_html=True):
        article = cls.query.get(id)
        return cls.to_json(article, convert_to_html)

    @classmethod
    def get_articles(cls, draft=False, page=1):
        articles = cls.query.filter_by(draft=draft, deleted_at=None) \
            .order_by(cls.updated_at.desc()) \
            .offset((page - 1) * 10).limit(10).all()
        return cls.to_json(articles)
    
    @classmethod
    def get_user_posts(cls, user_id, draft=False):
        articles = cls.query.filter_by(user_id=user_id, draft=draft, deleted_at=None) \
            .order_by(cls.updated_at.desc()).all()
        return cls.to_json(articles)

    @classmethod
    def insert(cls, article):
        article = cls(**article)
        db.session.add(article)
        db.session.commit()
        return cls.to_json(article)

    @classmethod
    def update(cls, id, data):
        article = cls.query.get(id)
        article.content = json.dumps(data['content'])
        article.draft = data['draft']
        article.first_paragraph = data['first_paragraph']
        article.title = data['title']
        article.updated_at = datetime.now()
        db.session.add(article)
        db.session.commit()
        return cls.to_json(article)
    
    @classmethod
    def delete(cls, id):
        article = cls.query.get(id)
        article.deleted_at = datetime.now()
        db.session.add(article)
        db.session.commit()

    @classmethod
    def to_json(cls, data, convert_to_html=True):
        if isinstance(data, cls):
            content = json.loads(data.content)
            return {
                'id': data.id,
                'title': data.title,
                'first_paragraph': data.first_paragraph or '',
                'content': convert_to_html and  BlogContentParser(content).html() or content,
                'comments': [Comment.to_json(comment) for comment in data.comments],
                'created_at': datetime.strftime(data.created_at, '%a %d, %Y'),
                'updated_at': data.updated_at.isoformat(),
            }
        elif isinstance(data, list):
            return list(map(cls.to_json, data))
