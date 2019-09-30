from unittest import TestCase
from graphene.test import Client
from schema import schema
from database import init_db


class MutationTests(TestCase):
    """Test cases for employee creation."""

    def setUp(self):
        """Add starter data and initialize Graphene test client."""
        init_db()
        self.client = Client(schema)


    def test_employee_creation(self):
        """Basic test for employee creation."""
        helper = EmployeeHelper(name='Andrew', hired_on='2019-10-01T00:00:00', salary=50000, department_id=1)

        # Returned result is an OrderedDict
        result = self.client.execute(helper.get_create_employee_query())['data']['createEmployee']['employee']

        self.assertEqual(result['name'], helper.name)
        self.assertEqual(result['hiredOn'], helper.hired_on)
        self.assertEqual(result['salary'], helper.salary)
        self.assertEqual(result['departmentId'], helper.department_id)


    def test_employee_creation_bad_fields(self):
        """Tests that the invalid fields are discarded and the the default values are used."""
        helper = EmployeeHelper(name='Andrew', hired_on='2019-10-01T00:00:00', salary=None, department_id=None)
        result = self.client.execute(helper.get_create_employee_query())['data']['createEmployee']['employee']

        self.assertEqual(result['name'], helper.name)
        self.assertEqual(result['hiredOn'], helper.hired_on)
        self.assertEqual(result['salary'], 0)
        self.assertIsNone(result['departmentId'])


class EmployeeHelper:
    """Convenience class for storing and validating employee fields."""

    def __init__(self, name, hired_on, salary, department_id):
        self.name = name
        self.hired_on = hired_on
        self.salary = salary
        self.department_id = department_id

    def get_create_employee_query(self):
        """Convenience method for creating employee creation queries."""
        template = """
            mutation createEmployee {{
              createEmployee(input: {{ {params} }}) {{
                employee {{
                  name
                  hiredOn
                  salary
                  departmentId
                }}
              }}
            }}
            """
        # Add input parameters as needed
        input_params = 'name:"{}",'.format(self.name)

        if self.hired_on is not None:
            input_params += 'hiredOn: "{}", '.format(self.hired_on)

        if self.salary is not None:
            input_params += 'salary: {}, '.format(self.salary)

        if self.department_id is not None:
            input_params += 'departmentId: {}'.format(self.department_id)

        return template.format(params=input_params)
