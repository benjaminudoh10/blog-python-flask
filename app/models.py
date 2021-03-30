import json
from datetime import datetime

from flask_login import UserMixin

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
    def get_articles(cls, draft=False, page=1):
        articles = cls.query.filter_by(draft=draft) \
            .order_by(cls.updated_at.desc()) \
            .offset((page - 1) * 10).limit(10).all()
        return cls.to_json(articles)
    
    @classmethod
    def get_user_posts(cls):
        return []

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
                'first_paragraph': data.first_paragraph or '',
                'content': convert_to_html and  BlogContentParser(content).html() or content,
                'created_at': datetime.strftime(data.created_at, '%a %d, %Y'),
                'updated_at': data.updated_at.isoformat(),
            }
        elif isinstance(data, list):
            return list(map(cls.to_json, data))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sub = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_pic = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

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
            content = json.loads(data)
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
