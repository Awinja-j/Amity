from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///amity.db')

Session = sessionmaker(bind=engine)

session = Session()


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    employee_type = Column(String(255), nullable=False)
    accomodation_status = Column(String(255), nullable=True)



class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, nullable=False, primary_key=True)
    room_type = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    person = relationship(Person)
    user_id = Column(Integer, ForeignKey('person.id'))


Base.metadata.create_all(engine)
