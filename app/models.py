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

    def __repr__(self):
        return '<Topic {}>'.format(self.title)


class TopicGroup(db.Model):
    '''
    This model describes the topic groups each topic can belong to.
    '''
    __tablename__ = 'topic_group'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    topics = db.relationship(Topic, backref='group', lazy=True)

    def __repr__(self):
        return '<TopicGroup {}>'.format(self.title)
