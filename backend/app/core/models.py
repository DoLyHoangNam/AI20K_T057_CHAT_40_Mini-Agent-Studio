import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False) # 'HR', 'Accounting', 'Production', 'Marketing'
    role = Column(String(20), default="EMPLOYEE")   # 'ADMIN', 'MANAGER', 'EMPLOYEE'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    agents = relationship("Agent", back_populates="creator")
    chat_logs = relationship("ChatLog", back_populates="user")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    instruction = Column(Text, nullable=False) # System Prompt
    department_access = Column(String(100), default="ALL") # 'ALL' hoặc phòng ban cụ thể ví dụ 'Accounting'
    workflow_config = Column(Text, default="{}") # Sơ đồ JSON của các nodes
    is_published = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="agents")
    documents = relationship("Document", back_populates="agent")
    chat_logs = relationship("ChatLog", back_populates="agent")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size_kb = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    agent = relationship("Agent", back_populates="documents")


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    role = Column(String(20)) # 'user' hoặc 'assistant'
    message = Column(Text, nullable=False)
    citations = Column(Text)  # Nguồn trích dẫn (Trang X tài liệu Y)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_logs")
    agent = relationship("Agent", back_populates="chat_logs")
