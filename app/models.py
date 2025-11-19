# Shared base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

# ============================
# UserService: User Model
# ============================
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default='reader')

    # Relationships
    announcements = relationship("Announcement", back_populates="creator")
    lost_items = relationship("LostFoundItem", back_populates="creator")


# ============================
# AnnouncementService: Announcement Model
# ============================
class Announcement(Base):
    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="announcements")


# ============================
# LostFoundService: LostFoundItem Model
# ============================
class LostFoundItem(Base):
    __tablename__ = 'LostFound'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    is_found = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="lost_items")  
