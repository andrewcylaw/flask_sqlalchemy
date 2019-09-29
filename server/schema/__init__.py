import graphene
from graphene import relay, Schema
from graphene_sqlalchemy import SQLAlchemyConnectionField
from server.schema.employee import EmployeeConnections, CreateEmployee
from server.schema.department import DepartmentConnection


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(EmployeeConnections)

    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()

schema = Schema(query=Query, mutation=Mutation)