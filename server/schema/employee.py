import math

from graphene import relay, Field, InputObjectType, Int, Boolean, List, ObjectType, String, DateTime, ID, Mutation
from graphene_sqlalchemy import SQLAlchemyObjectType

from schema.paging import PagingInfo, SortingDirection, DEFAULT_PAGE_SIZE
from model.department import Department as DepartmentModel
from model.employee import Employee as EmployeeModel
from database import db_session


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeeConnections(relay.Connection):
    class Meta:
        node = Employee


class EmployeePage(ObjectType):
    """Retrieve a page of employees.

    Required args:
        page_num - Page number to retrieve.
        page_size - Number of items per page.

    Optional args:
        sorting_field - Field to sort by. Only supports 'department' (department name)
                        and 'salary' right now.
        sorting_dir - Sorting direction enum. Either ASC or DESC.

    If the sorting_field is present but sorting_dir is not, defaults to ASC.
    """
    class Meta:
        model = EmployeeModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paging_parameters = args[0]

    paging_info = Field(PagingInfo,
                        page_num=Int(),
                        page_size=Int(),
                        total_num_pages=Int(),
                        has_next_page=Boolean(),
                        has_prev_page=Boolean())
    employee_page = List(Employee)


    # Generate paging information metadata.
    def resolve_paging_info(parent, info):
        total_num_items = Employee.get_query(info).count()

        # Bound given page_size if <1 or >total number of items
        if parent.paging_parameters.page_size < 0 or parent.paging_parameters.page_size > total_num_items:
            parent.paging_parameters.page_size = DEFAULT_PAGE_SIZE

        total_num_pages = math.ceil(total_num_items / parent.paging_parameters.page_size)

        # Bound given page_num if it exceeds 0 or max number of pages
        parent.paging_parameters.page_num = page_num = max(1, min(total_num_pages, parent.paging_parameters.page_num))

        return PagingInfo(page_num=parent.paging_parameters.page_num,
                          page_size=parent.paging_parameters.page_size,
                          total_num_pages=total_num_pages,
                          has_next_page=not (page_num >= total_num_pages),
                          has_prev_page=page_num != 1)


    # Fetch a page via offset pagination. Pages are 1-indexed!
    def resolve_employee_page(parent, info):
        page_num = parent.paging_parameters.page_num
        page_size = parent.paging_parameters.page_size
        offset = (page_num - 1) * page_size # For 1-indexed pages

        query = Employee.get_query(info).offset(offset).limit(page_size).from_self()

        # Check for applicable sorting column and direction
        sorting_by = parent.paging_parameters.sorting_field
        sorting_dir = parent.paging_parameters.sorting_dir

        if sorting_by == 'department':
            if sorting_dir == SortingDirection.DESC.value:
                query = query.join(DepartmentModel).order_by(DepartmentModel.name.desc())
            else:
                query = query.join(DepartmentModel).order_by(DepartmentModel.name.asc())

        elif sorting_by == 'salary':
            if sorting_dir == SortingDirection.DESC.value:
                query = query.order_by(EmployeeModel.salary.desc())
            else:
                query = query.order_by(EmployeeModel.salary.asc())

        return query.all()


class CreateEmployeeInput(InputObjectType):
    """Class representation of employee creation fields."""
    name = String(description='Name of the new employee.')
    hired_on = DateTime(description='When the new employee was hired.')
    salary = Int(description='Salary of the new employee.')
    department_id = ID(description='Department id of the new employee.')


class CreateEmployee(Mutation):
    """Create a new employee with name, hiring date, salary, and department."""
    class Arguments:
        input = CreateEmployeeInput(description='New employee fields', required=True)

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
