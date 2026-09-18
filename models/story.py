from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    jobs = relationship("StoryJob", back_populates="story", cascade="all, delete-orphan")

    nodes = relationship("StoryNode", back_populates="story", cascade="all, delete-orphan")
    
class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("story_nodes.id"), nullable=True)
    content = Column(String, nullable=False)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON, nullable=True)

    story = relationship("Story", back_populates="nodes")