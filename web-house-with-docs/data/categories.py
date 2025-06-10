from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase

posts_to_category = Table(
    'posts_to_category',
    SqlAlchemyBase.metadata,
    Column('news', Integer,
                      ForeignKey('posts.id')),
    Column('category', Integer,
                      ForeignKey('categories.id'))
)

class Categories(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)