from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from database import Base


class Department(Base):
    """Department model."""
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    """Employee model."""
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))

    def __init__(self, name, department, department_id=None):
        self.name = name
        self.department = department
    #
    #     if department_id:
    #         self.department_id = department_id
