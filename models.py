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
    salary = Column(Integer, default=0)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))

    def __init__(self, name, salary, department, hired_on=func.now()):
        self.name = name
        self.hired_on = hired_on
        self.salary = salary
        self.department = department

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'salary': self.salary,
            'departmentName': self.department.name
        }
