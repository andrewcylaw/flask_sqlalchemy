from sqlalchemy import *
from database import Base


class Department(Base):
    """Department model."""
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)