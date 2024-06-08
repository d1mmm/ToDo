from datetime import date

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///todo.db', echo=True)

Base = declarative_base()


class ToDo(Base):
    __tablename__ = 'ToDo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False)
    description = Column(String)
    from_date = Column(String, nullable=False)
    due_date = Column(String, nullable=False)


class Done(Base):
    __tablename__ = 'Done'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False)
    description = Column(String)
    from_date = Column(String, nullable=False)
    due_date = Column(String, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

