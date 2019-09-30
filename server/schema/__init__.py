import graphene
from graphene import relay, Schema, ObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField

from schema.paging import PagingParameters
from server.schema.employee import EmployeeConnections, CreateEmployee, Employee, EmployeePage
from server.schema.department import DepartmentConnection


class Query(ObjectType):
    node = relay.Node.Field()

    # List methods
    all_employees = SQLAlchemyConnectionField(EmployeeConnections)
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)

    # Employee offset pagination
    employee_page = graphene.Field(EmployeePage,
                                   paging_parameters=graphene.Argument(PagingParameters))

    def resolve_employee_page(self, info, paging_parameters):
        return EmployeePage(paging_parameters)


class Mutation(ObjectType):
    create_employee = CreateEmployee.Field()

schema = Schema(query=Query, mutation=Mutation)

'''

a) I should have the ability to see the total number of pages when I’m at any given
page
b) I should have the ability to see the current page number
c) I should have the ability to goto Nth page, navigate to the previous page and next
page
d) (bonus) sorting while in a page

'''