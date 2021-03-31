from . import db
from .topic_group import TopicGroup


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

