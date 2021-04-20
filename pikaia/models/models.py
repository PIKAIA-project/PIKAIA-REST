import datetime

from pikaia import db


# class for user table
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(db.String(length=50), nullable=False, unique=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=80))
    admin = db.Column(db.Boolean)


# we need a public key for each chat conversation
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    user_sentence = db.Column(db.String(200))
    chatbot_sentence = db.Column(db.String(200))
    user_emotion = db.Column(db.String(10))
    user_id = db.Column(db.Integer)
    date_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)


class Emotion(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(db.String(length=50), nullable=False, unique=True)
    user_input = db.Column(db.String(200))
    user_emotion = db.Column(db.String(10))
    user_id = db.Column(db.Integer())


class Songs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    song_name = db.Column(db.String(50))
    song_link = db.Column(db.String(1000))
    song_author = db.Column(db.String(15))
    song_cover = db.Column(db.String(1000))


class Ratings(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    song_id = db.Column(db.Integer(), db.ForeignKey('songs.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    ratings = db.Column(db.Integer())


class Binaural(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    binaural_name = db.Column(db.String(50))
    binaural_link = db.Column(db.String(1000))
    binaural_author = db.Column(db.String(15))
    binaural_cover = db.Column(db.String(15))
    binaural_type = db.Column(db.String(50))
