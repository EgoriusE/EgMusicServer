# coding: utf-8
import base64
import os
from datetime import datetime, timedelta

from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, lm

Base = declarative_base()
metadata = Base.metadata


#
#

#
#
# class Playlist(db.Model):
#     __tablename__ = 'playlist'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     author = Column(String(255), nullable=False)
#     duration = Column(Time, nullable=False)
#     icon_path = Column(String(255))
#
#     song = relationship('Song', secondary='playlists_table')
#     user = relationship('User', secondary='like_playlist')
#
#
# class Prize(db.Model):
#     __tablename__ = 'prize'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)
#     year = Column(Integer, nullable=False)
#     description = Column(String(255))
#
#     song = relationship('Song', secondary='prizes_songs_table')
#


class HistoryArtistTable(db.Model):
    def __repr__(self):
        return '<HistoryArtistTable {}>'.format(self.name)

    artist = db.Column(db.ForeignKey('artist.name'), primary_key=True, nullable=False, index=True)
    group = db.Column(db.ForeignKey('group.name'), primary_key=True, nullable=False, index=True)
    start_date = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.Integer, nullable=False)


artists_table = db.Table('artists_table',
                         db.Column('creator', db.String, db.ForeignKey('artist.name')),
                         db.Column('song', db.Integer, db.ForeignKey('song.id')))


class Artist(db.Model):
    def __repr__(self):
        return '<Artist {}>'.format(self.name)

    name = db.Column(db.String(255), primary_key=True)
    desc = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    icon_path = db.Column(db.String(255), nullable=True)

    songs = db.relationship('Song', secondary=artists_table)
    history = relationship('HistoryArtistTable')

    @staticmethod
    def to_collection_dict():
        resources = Artist.query.paginate(1, 20, False)
        data = {
            'items': [item.to_dict() for item in resources.items]
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'desc', 'country', 'icon_path']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'name': self.name,
            'desc': self.desc,
            'country': self.country,
            'icon_path': self.icon_path
        }
        return data


groups_table = db.Table('groups_table',
                        db.Column('creator', db.String, db.ForeignKey('group.name')),
                        db.Column('song', db.Integer, db.ForeignKey('song.id')))


class Group(db.Model):
    def __repr__(self):
        return '<Group {}>'.format(self.name)

    name = db.Column(db.String(255), primary_key=True)
    desc = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    icon_path = db.Column(db.String(255), nullable=True)

    history = db.relationship('HistoryArtistTable')

    songs = tags = db.relationship('Song', secondary=groups_table)

    @staticmethod
    def to_collection_dict():
        resources = Group.query.paginate(1, 20, False)
        data = {
            'items': [item.to_dict() for item in resources.items]
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'desc', 'country', 'icon_path']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'name': self.name,
            'desc': self.desc,
            'country': self.country,
            'icon_path': self.icon_path
        }
        return data


class Album(db.Model):
    def __repr__(self):
        return '<Album {}>'.format(self.name)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    icon_path = db.Column(db.String(255), nullable=True)
    type = db.Column(db.Enum('album', 'compilation', 'concert', name='album_type'), nullable=False, index=True,
                     server_default=db.text("'album'::album_type"))

    # U = relationship('User', secondary='like_album')
    # prize = relationship('Prize', secondary='prizes_albums_table')

    @staticmethod
    def to_collection_dict():
        resources = Album.query.paginate(1, 20, False)
        data = {
            'items': [item.to_dict() for item in resources.items]
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'year', 'quantity', 'icon_path', 'type']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'quantity': self.quantity,
            'icon_path': self.icon_path,
            'type': self.type
        }
        return data


class Song(db.Model):
    def __repr__(self):
        return '<Song {}>'.format(self.name)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=True)
    album = db.Column(db.ForeignKey('album.id'), nullable=True)
    year = db.Column(db.Integer, index=True, nullable=False)

    album1 = relationship('Album')

    @staticmethod
    def to_collection_dict():
        resources = Song.query.paginate(1, 20, False)
        data = {
            'items': [item.to_dict() for item in resources.items]
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'path', 'album', 'year', 'id']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'path': self.path,
            'album': self.album
        }
        return data


@lm.user_loader
def load_user(email):
    return User.query.get(str(email))


class User(UserMixin, db.Model):
    email = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    icon_path = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def to_collection_dict():
        resources = User.query.paginate(1, 20, False)
        data = {
            'users': [item.to_dict() for item in resources.items]
        }
        return data

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def from_dict(self, data, new_user=False):
        for field in ['email', 'name', 'icon_path']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self, include_email=False):
        data = {
            'email': self.email,
            'name': self.name,
            'icon_path': self.icon_path
        }
        if include_email:
            data['email'] = self.email
        return data

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#
# t_like_playlist = Table(
#     'like_playlist', metadata,
#     Column('user', ForeignKey('user.email'), nullable=False),
#     Column('playlist', ForeignKey('playlist.id'), nullable=False)
# )
#
# t_prizes_albums_table = Table(
#     'prizes_albums_table', metadata,
#     Column('album', ForeignKey('album.id')),
#     Column('prize', ForeignKey('prize.id'), primary_key=True)
# )
#
#

#
#

#

#
# t_playlists_table = Table(
#     'playlists_table', metadata,
#     Column('playlist', ForeignKey('playlist.id'), nullable=False, index=True),
#     Column('song', ForeignKey('song.id'), nullable=False)
# )
#
# t_prizes_songs_table = Table(
#     'prizes_songs_table', metadata,
#     Column('song', ForeignKey('song.id')),
#     Column('prize', ForeignKey('prize.id'), primary_key=True)
# )
