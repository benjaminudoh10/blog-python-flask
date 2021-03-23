from datetime import datetime
from . import db


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
        return cls.query.limit(number)

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
        return cls.query.all()

    def __repr__(self):
        return '{}'.format(self.title)
