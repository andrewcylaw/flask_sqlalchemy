import graphene
from graphene import relay, Schema, ObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField
from server.schema.employee import EmployeeConnections, CreateEmployee
from server.schema.department import DepartmentConnection


class Query(ObjectType):
    node = relay.Node.Field()

    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(EmployeeConnections)

    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)


class Mutation(ObjectType):
    create_employee = CreateEmployee.Field()

schema = Schema(query=Query, mutation=Mutation)

'''

a) I should have the ability to see the total number of pages when I’m at any given
page
b) I should have the ability to see the current page number
c) I should have the ability to goto Nth page, navigate to the previous page and next
page


'''