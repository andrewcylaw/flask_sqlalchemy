from graphene import relay, Schema, ObjectType, Field, Argument
from graphene_sqlalchemy import SQLAlchemyConnectionField

from schema.paging import PagingParameters
from schema.employee import EmployeeConnections, CreateEmployee, Employee, EmployeePage
from schema.department import DepartmentConnection


class Query(ObjectType):
    node = relay.Node.Field()

    # List methods
    all_employees = SQLAlchemyConnectionField(EmployeeConnections)
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)

    # Employee offset pagination
    employee_page = Field(EmployeePage, paging_parameters=Argument(PagingParameters))

    def resolve_employee_page(self, info, paging_parameters):
        return EmployeePage(paging_parameters)


class Mutation(ObjectType):
    create_employee = CreateEmployee.Field()

schema = Schema(query=Query, mutation=Mutation)
