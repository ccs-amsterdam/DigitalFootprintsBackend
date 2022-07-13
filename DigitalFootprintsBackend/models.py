import json
from sqlalchemy import func,  Column, Integer, String
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
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    password = Column(String, nullable=True)

class TiktokVideo(Base):
    __tablename__ = 'tiktokvideos'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    video_id = Column(Integer, index=True)
    user = Column(String)
    
class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(String)
    data = Column(JsonString)


#  codingjob_id = Column(Integer, ForeignKey("codingjobs.id"), index=True)
#     jobset = Column(String)
#     codebook = Column(JsonString, nullable=True)

#     codingjob = relationship("CodingJob", back_populates="jobsets")