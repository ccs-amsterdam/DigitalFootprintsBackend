import json
from sqlalchemy import func,  Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship

from DigitalFootprintsBackend.database import Base


class JsonString(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    password = Column(String, nullable=True)

class PublicData(Base):
    """
    This can be used to store data that is safe enough to make public, such as certain aggregated data.
    Submission id is only required to prevent duplicate uploads, but will not be made available via API (so is not public).
    But the data stored here is public, so make sure it doesn't contain information to identify participants by.
    """
    __tablename__ = 'itemscore'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project = Column(Integer, ForeignKey('project.id'))
    submission_id = Column(String)
    modified = Column(Integer)
    publicdata = Column(JsonString)

# class PrivateData(Base):
#     # Should only be able to GET data with project password AND specific submission id  
#     __tablename__ = 'privatedata'

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     project = Column(integer, ForeignKey('project.id'))
#     submission_id = Column(String)
#     privatedata = Column(JsonString)

class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project = Column(Integer, ForeignKey('project.id'))
    submission_id = Column(String)
    log = Column(JsonString)


class Transformer(Base):
    __tablename__ = 'transformer'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input = Column(JsonString)
    output = Column(JsonString)


#  codingjob_id = Column(Integer, ForeignKey("codingjobs.id"), index=True)
#     jobset = Column(String)
#     codebook = Column(JsonString, nullable=True)

#     codingjob = relationship("CodingJob", back_populates="jobsets")