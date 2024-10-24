from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
import uuid

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User',back_populates='blogs')

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer,primary_key=True,index=True)
    uid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    street_name = Column(String)
    pwm = Column(String)
    volt = Column(String)
    ampe = Column(String)
    health = Column(String)
    log = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # Khóa ngoại liên kết với User

    owner = relationship('User', back_populates='nodes')  # Liên kết với User


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    # email = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    blogs = relationship('Blog', back_populates='creator')
    nodes = relationship('Node', back_populates='owner')



