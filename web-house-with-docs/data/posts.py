from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    body = Column(String, nullable=False)
    user = relationship('Users', backref='posts')
    categories = relationship('Categories', secondary='posts_to_category', backref='posts')
