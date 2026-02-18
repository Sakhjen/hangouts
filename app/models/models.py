"""SQLAlchemy модели для приложения вписок."""

from typing import List, Optional
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey, Enum, ARRAY, Numeric, func, BigInteger
from sqlalchemy import UniqueConstraint 
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import ARRAY as PGArray
from app.db.base import BaseModel

# Enums (без изменений)
class HangoutStatus(PyEnum):
    PLANNED = "planned"
    STARTED = "started"
    FINISHED = "finished"
    CANCELLED = "cancelled"

class ResponseStatus(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"

class ReportType(PyEnum):
    NO_SHOW = "no_show"
    WRONG_ADDRESS = "wrong_address"
    MISMATCH = "mismatch"
    SPAM = "spam"

# Модели (исправленные)
class User(BaseModel):
    __tablename__ = "users"
    
    phone = Column(String(20), unique=True, index=True, nullable=False)
    verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
    avatar_url = Column(Text, nullable=True)
    photos = Column(PGArray(Text), default=list, nullable=False)
    bio = Column(Text, nullable=True)
    city = Column(String(100), index=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    hangouts = relationship("Hangout", back_populates="creator", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="user", cascade="all, delete-orphan")
    sent_messages = relationship("ChatMessage", foreign_keys="ChatMessage.sender_id")
    ratings_given = relationship("Rating", foreign_keys="Rating.rater_id")
    reports = relationship("Report", foreign_keys="Report.reporter_id")

class Hangout(BaseModel):
    __tablename__ = "hangouts"
    
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    tags = Column(PGArray(String), default=list, nullable=False)
    max_guests = Column(Integer, default=10, nullable=False)
    photos = Column(PGArray(Text), default=list, nullable=False)
    address = Column(Text, nullable=True)
    lat = Column(Numeric(9, 6), nullable=True)
    lng = Column(Numeric(9, 6), nullable=True)
    datetime_start = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    datetime_end = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(Enum(HangoutStatus), default=HangoutStatus.PLANNED, nullable=False, index=True)
    applications_closed = Column(Boolean, default=False, nullable=False)
    
    # Связи
    creator = relationship("User", back_populates="hangouts")
    responses = relationship("Response", back_populates="hangout", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", cascade="all, delete-orphan")

class Response(BaseModel):
    __tablename__ = "responses"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    hangout_id = Column(Integer, ForeignKey("hangouts.id"), nullable=False, index=True)
    status = Column(Enum(ResponseStatus), default=ResponseStatus.PENDING, nullable=False)
    confirmed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "hangout_id", name="unique_user_hangout"),
    )
    
    # Связи
    user = relationship("User", back_populates="responses")
    hangout = relationship("Hangout", back_populates="responses")

class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"
    
    hangout_id = Column(Integer, ForeignKey("hangouts.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    
    # Связи
    hangout = relationship("Hangout", back_populates="messages")
    sender = relationship("User")

class Rating(BaseModel):
    __tablename__ = "ratings"
    
    rater_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    ratee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hangout_id = Column(Integer, ForeignKey("hangouts.id"), nullable=True)
    score = Column(Integer, nullable=False)
    feedback = Column(Text)
    
    # Unique constraints
    __table_args__ = (
        UniqueConstraint("rater_id", "ratee_id", name="unique_rater_ratee"),
        UniqueConstraint("rater_id", "hangout_id", name="unique_rater_hangout"),
    )
    
    # Связи
    rater = relationship("User", foreign_keys=[rater_id])
    ratee = relationship("User", foreign_keys=[ratee_id])

class Report(BaseModel):
    __tablename__ = "reports"
    
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hangout_id = Column(Integer, ForeignKey("hangouts.id"), nullable=True)
    type_ = Column(Enum(ReportType), nullable=False, index=True)  # type is reserved word
    description = Column(Text)
    resolved = Column(Boolean, default=False, nullable=False)
    
    # Связи
    reporter = relationship("User", foreign_keys=[reporter_id])
    target_user = relationship("User", foreign_keys=[target_user_id])
