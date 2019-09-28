import graphene
from graphene import relay, Field, Schema
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Department as DepartmentModel, Employee as EmployeeModel
from database import db_session


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class DepartmentConnection(relay.Connection):
    class Meta:
        node = Department


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeeConnections(relay.Connection):
    class Meta:
        node = Employee


class CreateEmployeeInput(graphene.InputObjectType):
    name = graphene.String(description='Name of the new employee.')
    hired_on = graphene.DateTime(description='When the new employee was hired.')
    salary = graphene.Int(description='Salary of the new employee.')
    department_id = graphene.ID(description='Department id of the new employee.')


class CreateEmployee(graphene.Mutation):
    """Create a new employee with name, hiring date, salary, and department."""
    class Arguments:
        input = CreateEmployeeInput(description="New employee fields", required=True)

    class Meta:
        description = "Creates a new employee with the given name and department."

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


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(EmployeeConnections)

    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()

schema = Schema(query=Query, mutation=Mutation)