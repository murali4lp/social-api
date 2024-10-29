from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = 'posts_orm'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users_orm.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")

    # added for issue with json serialization
    def as_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(Base):
    __tablename__ = 'users_orm'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('now()'), nullable=False)

class Vote(Base):
    __tablename__ = "votes_orm"
    user_id = Column(Integer, ForeignKey(
        "users_orm.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts_orm.id", ondelete="CASCADE"), primary_key=True)