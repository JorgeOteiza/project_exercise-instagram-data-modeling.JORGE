import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean # type: ignore
from sqlalchemy.orm import relationship, declarative_base # type: ignore
from sqlalchemy import create_engine # type: ignore
from eralchemy2 import render_er # type: ignore

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    likes = relationship('Like', back_populates='user')
    followers = relationship('Follow', back_populates='follower', foreign_keys='Follow.follower_id')
    following = relationship('Follow', back_populates='followed', foreign_keys='Follow.followed_id')
    profile = relationship('Profile', uselist=False, back_populates='user')

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    biography = Column(Text)
    twitter = Column(String(250))
    facebook = Column(String(250))
    instagram = Column(String(250))
    avatar = Column(String(250))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='profile')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image_url = Column(String, nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime)
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    created_at = Column(DateTime)
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

class Follow(Base):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime)
    follower = relationship('User', back_populates='followers', foreign_keys=[follower_id])
    followed = relationship('User', back_populates='following', foreign_keys=[followed_id])

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
