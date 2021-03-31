from . import db
# fix cyclic import issue with next line
# from .topic import Topic


class TopicGroup(db.Model):
    '''
    This model describes the topic groups each topic can belong to.
    '''
    __tablename__ = 'topic_group'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    topics = db.relationship('Topic', backref='group', lazy=True)

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
