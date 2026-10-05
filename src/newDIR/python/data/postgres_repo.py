"""PostgreSQL repository using SQLAlchemy ORM."""

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class AgentRecord(Base):
    """SQLAlchemy model for agents table."""

    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    role = Column(String(200), nullable=False)
    model = Column(String(50), default="gpt-4")


def create_engine_and_session(database_url: str):
    """Create engine and session factory."""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return engine, Session


def init_db(engine):
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
