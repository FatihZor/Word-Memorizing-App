from app import db, bcrypt
from time import time
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(50), nullable=False)
    definitions = db.relationship('WordDefinition', back_populates="word", lazy='dynamic')
    library_items = db.relationship('Library', back_populates="word", lazy='dynamic')

    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return '<Word %s>' % self.word

    @classmethod
    def get(cls, word):
        """
        :rtype: object
        :type word: string
        """
        try:
            return Word.query.filter_by(word=word).one()
        except NoResultFound:
            return None

    @classmethod
    def get_all(cls):
        """
        :rtype: object
        """
        try:
            return Word.query.all()
        except NoResultFound:
            return None

    @classmethod
    def get_definitions(cls, word_id):
        """
        :rtype: object
        :type word_id: int
        """
        try:
            return WordDefinition.query.filter_by(word_id=word_id).all()
        except NoResultFound:
            return None

class WordDefinition(db.Model):
    __tablename__ = 'word_definitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    definition = db.Column(db.String(255), nullable=False)
    part_of_speech = db.Column(db.String(50), nullable=False)

    word = db.relationship('Word', back_populates="definitions")

    def __init__(self, word_id, definition, part_of_speech):
        self.word_id = word_id
        self.definition = definition
        self.part_of_speech = part_of_speech
    
    def __repr__(self):
        return '<WordDefinition %s>' %  self.definition

    @classmethod
    def get(cls, word_id):
        """
        :rtype: object
        :type word_id: string
        """
        try:
            return WordDefinition.query.filter_by(word_id=word_id).one()
        except NoResultFound:
            return None

class Library(db.Model):
    __tablename__ = 'libraries'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'word_id'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False )
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    word = db.relationship('Word', back_populates="library_items")

    def __init__(self, user_id, word_id):
        self.user_id = user_id
        self.word_id = word_id
    
    def __repr__(self):
        return '<Library %s>' %  self.id

    @classmethod
    def get(cls, user_id, word_id):
        """
        :rtype: object
        :type user_id: int
        :type word_id: int
        """
        try:
            return Library.query.filter_by(user_id=user_id, word_id=word_id).one()
        except NoResultFound:
            return None

    @classmethod
    def get_all(cls, user_id):
        """
        :rtype: object
        :type user_id: int
        """
        try:
            return Library.query.filter_by(user_id=user_id).all()
        except NoResultFound:
            return None

    @classmethod
    def word_exists(cls, user_id, word_id):
        """
        :rtype: boolean
        :type user_id: int
        :type word_id: int
        """
        try:
            library = Library.query.filter_by(user_id=user_id, word_id=word_id).first()
            if library:
                return True
            return False
        except NoResultFound:
            return False
            
    @classmethod
    def get_count(cls, user_id):
        """
        :rtype: int
        :type user_id: int
        """
        try:
            return Library.query.filter_by(user_id=user_id).count()
        except NoResultFound:
            return 0

class Point(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False )
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, word_id, point, reason):
        self.user_id = user_id
        self.word_id = word_id
        self.point = point
        self.reason = reason
    
    def __repr__(self):
        return '<Point %s>' %  self.id

    @classmethod
    def get(cls, user_id, word_id):
        """
        :rtype: object
        :type user_id: int
        :type word_id: int
        """
        try:
            return Point.query.filter_by(user_id=user_id, word_id=word_id).one()
        except NoResultFound:
            return None

    @classmethod
    def get_all(cls, user_id):
        """
        :rtype: object
        :type user_id: int
        """
        try:
            return Point.query.filter_by(user_id=user_id).all()
        except NoResultFound:
            return None

    @classmethod
    def get_count(cls, user_id):
        """
        :rtype: int
        :type user_id: int
        """
        try:
            return Point.query.filter_by(user_id=user_id).count()
        except NoResultFound:
            return 0

    @classmethod
    def get_points(cls, user_id, word_id):
        """
        :rtype: int
        :type user_id: int
        :type word_id: int
        """
        try:
            point = Point.query.filter_by(user_id=user_id, word_id=word_id).all()
            total_point = 0
            for point in point:
                total_point += point.point
            return total_point
        except NoResultFound:
            return 0

    @classmethod
    def get_points_for_word(cls, word_id):
        """
        :rtype: int
        :type word_id: int
        """
        try:
            points = Point.query.filter_by(word_id=word_id).all()
            total_point = 0
            for point in point:
                total_point += point.point
            return total_point
        except NoResultFound:
            return 0
