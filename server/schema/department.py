from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from server.model.department import Department as DepartmentModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )

class DepartmentConnection(relay.Connection):
    class Meta:
        node = Department