import graphene
from graphene import relay, Field, InputObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType
from server.model.department import Department as DepartmentModel
from server.model.employee import Employee as EmployeeModel
from server.database import db_session


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )

class EmployeeConnections(relay.Connection):
    class Meta:
        node = Employee


class CreateEmployeeInput(InputObjectType):
    """Class representation of employee creation fields."""
    name = graphene.String(description='Name of the new employee.')
    hired_on = graphene.DateTime(description='When the new employee was hired.')
    salary = graphene.Int(description='Salary of the new employee.')
    department_id = graphene.ID(description='Department id of the new employee.')


class CreateEmployee(graphene.Mutation):
    """Create a new employee with name, hiring date, salary, and department."""
    class Arguments:
        input = CreateEmployeeInput(description="New employee fields", required=True)

    class Meta:
        description = 'Creates a new employee with the given inputs.'

    employee = Field(Employee)

    def mutate(self, info, input=None):
        department = db_session.query(DepartmentModel).filter_by(id=input.department_id).first()
        employee = EmployeeModel(name=input.name,
                                 hired_on=input.hired_on,
                                 salary=input.salary,
                                 department=department)

        db_session.add(employee)
        db_session.commit()

        return CreateEmployee(employee=employee)
