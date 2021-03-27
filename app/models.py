import json
from datetime import datetime

from . import db
from .parser import BlogContentParser


class Topic(db.Model):
    '''
    This model describes the various topics users can subscribe to.
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    image = db.Column(db.String)
    group_id = db.Column(db.Integer, db.ForeignKey('topic_group.id'))

    @classmethod
    def get_topics(cls, number = 10):
        topics = cls.query.limit(number).all()
        return cls.to_json(topics)

    @classmethod
    def to_json(cls, data):
        if isinstance(data, cls):
            return {
                'id': data.id,
                'title': data.title,
                'description': data.description,
                'image': data.image,
                'group': TopicGroup.to_json(data.group, False)
            }
        elif isinstance(data, list):
            return list(map(cls.to_json, data))

    def __repr__(self):
        return '{}'.format(self.title)


class TopicGroup(db.Model):
    '''
    This model describes the topic groups each topic can belong to.
    '''
    __tablename__ = 'topic_group'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    topics = db.relationship(Topic, backref='group', lazy=True)

    @classmethod
    def get(cls):
        groups = cls.query.all()
        return cls.to_json(groups)

    @classmethod
    def to_json(cls, data, include_topics=True):
        if isinstance(data, cls):
            return {
                'id': data.id,
                'title': data.title,
                'topics': include_topics and Topic.to_json(data.topics) or None
            }
        elif isinstance(data, list):
            return list(map(cls.to_json, data))

    def __repr__(self):
        return '{}'.format(self.title)


class Article(db.Model):
    '''
    This model describes an article.
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    first_paragraph = db.Column(db.String)
    content = db.Column(db.Text, nullable=False)
    draft = db.Column(db.Boolean, nullable=True, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def get(cls, id, convert_to_html=True):
        article = cls.query.get(id)
        return cls.to_json(article, convert_to_html)

    @classmethod
    def get_all_articles(cls):
        articles = cls.query.all()
        return cls.to_json(articles)

    @classmethod
    def insert(cls, article):
        article = cls(**article)
        db.session.add(article)
        db.session.commit()
        return cls.to_json(article)

    @classmethod
    def update(cls, id, content):
        article = cls.query.get(id)
        article.content = content
        db.session.add(article)
        db.session.commit()
        return cls.to_json(article)

    @classmethod
    def to_json(cls, data, convert_to_html=True):
        if isinstance(data, cls):
            content = json.loads(data.content)
            return {
                'id': data.id,
                'title': data.title,
                'content': convert_to_html and  BlogContentParser(content).html() or content,
                'created_at': datetime.strftime(data.created_at, '%a %d, %Y'),
                'updated_at': data.updated_at.isoformat(),
            }
        elif isinstance(data, list):
            return list(map(cls.to_json, data))
