import math

import graphene
from graphene import relay, Field, InputObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType

from schema.paging import PagingInfo
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


class EmployeePage(graphene.ObjectType):
    """Retrieve a page of employees with the given page size and page number."""
    class Meta:
        model = EmployeeModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paging_parameters = args[0]

    paging_info = graphene.Field(PagingInfo,
                                 page_num=graphene.Int(),
                                 page_size=graphene.Int(),
                                 total_num_pages=graphene.Int(),
                                 has_next_page=graphene.Boolean(),
                                 has_prev_page=graphene.Boolean())
    employee_page = graphene.List(Employee)

    # Paginate via offset pagination. Pages are 1-indexed!
    def resolve_paging_info(parent, info):
        page_num = parent.paging_parameters.page_num
        page_size = parent.paging_parameters.page_size
        total_num_pages = math.ceil(Employee.get_query(info).count() / page_size)

        return PagingInfo(page_num=page_num,
                          page_size=page_size,
                          total_num_pages=total_num_pages,
                          has_next_page=not (page_num >= total_num_pages),
                          has_prev_page=page_num != 1)


    def resolve_employee_page(parent, info):
        page_num = parent.paging_parameters.page_num
        page_size = parent.paging_parameters.page_size
        offset = (page_num - 1) * page_size + 1 # For 1-indexed pages

        return Employee.get_query(info).offset(offset).limit(page_size).all()


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

    def mutate(parent, info, input=None):
        department = db_session.query(DepartmentModel).filter_by(id=input.department_id).first()
        employee = EmployeeModel(name=input.name,
                                 hired_on=input.hired_on,
                                 salary=input.salary,
                                 department=department)

        db_session.add(employee)
        db_session.commit()

        return CreateEmployee(employee=employee)
