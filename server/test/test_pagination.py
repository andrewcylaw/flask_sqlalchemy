from enum import Enum
from unittest import TestCase
from graphene.test import Client
from schema import schema
from database import init_db, db_session
from model.employee import Employee as EmployeeModel
from schema.paging import DEFAULT_PAGE_SIZE


class SortingDirection(Enum):
    DESC = 0
    ASC = 1


class EmployeePaginationTests(TestCase):
    """Test cases for employee pagination."""

    def setUp(self):
        """Add starter data and initialize Graphene test client."""
        init_db()
        self.client = Client(schema)
        self.total_num_items = db_session.query(EmployeeModel).count()


    def test_prev_page_bound(self):
        """Tests that there is no previous page at page 1."""
        result = EmployeePaginationHelper(page_num=1, page_size=5).fetch_results(self.client)['pagingInfo']
        self.assertFalse(result['hasPrevPage'])
        self.assertTrue(result['hasNextPage'])


    def test_next_page_bound(self):
        """Tests that there is no next page at the last page."""
        result = EmployeePaginationHelper(page_num=2, page_size=self.total_num_items - 1).fetch_results(self.client)['pagingInfo']
        self.assertTrue(result['hasPrevPage'])
        self.assertFalse(result['hasNextPage'])


    def test_default_page_values(self):
        """Tests that negative numbers and extremely large numbers are handled appropriately."""
        # Negative page size/num
        result = EmployeePaginationHelper(page_num=-100, page_size=-100).fetch_results(self.client)['pagingInfo']
        self.assertEqual(result['pageNum'], 1)
        self.assertEqual(result['pageSize'], DEFAULT_PAGE_SIZE)

        # Page size/num are too big
        result = EmployeePaginationHelper(page_num=self.total_num_items, page_size=self.total_num_items + 1).fetch_results(self.client)['pagingInfo']
        self.assertEqual(result['pageNum'], 1)
        self.assertEqual(result['pageSize'], DEFAULT_PAGE_SIZE)


    def test_retrieve_first_page_sorted_salary_desc(self):
        """Tests that the first page is sorted correctly on descending name."""
        results = EmployeePaginationHelper(page_num=1,
                                           page_size=10,
                                           sorting_field='salary',
                                           sorting_direction=SortingDirection.DESC).fetch_results(self.client)['employeePage']
        self.assertTrue(all(results[i]['salary'] >= results[i + 1]['salary'] for i in range(len(results) - 1)))


    def test_retrieve_first_page_sorted_department_asc(self):
        """Tests that the first page is sorted correctly by ascending department name."""
        results = EmployeePaginationHelper(page_num=1,
                                           page_size=10,
                                           sorting_field='department',
                                           sorting_direction=SortingDirection.ASC).fetch_results(self.client)['employeePage']
        self.assertTrue(all(results[i]['department']['name'] <= results[i + 1]['department']['name'] for i in range(len(results) - 1)))


    def test_default_sorting_direction_is_asc(self):
        """Tests that the default sorting order when not provided is ascending."""
        results = EmployeePaginationHelper(page_num=1, page_size=10, sorting_field='salary').fetch_results(self.client)['employeePage']
        self.assertTrue(all(results[i]['salary'] <= results[i + 1]['salary'] for i in range(len(results) - 1)))


    def test_invalid_sorting_field(self):
        """Tests that no sorting is applied if the given field is invalid."""
        invalid_sort_results = EmployeePaginationHelper(page_num=1,
                                                        page_size=10,
                                                        sorting_field='error error').fetch_results(self.client)['employeePage']
        default_sort_results = EmployeePaginationHelper(page_num=1,
                                                        page_size=10).fetch_results(self.client)['employeePage']
        self.assertEqual(invalid_sort_results, default_sort_results)


    def test_fetch_total_pages(self):
        """Tests pagination from page 1 to the last page to verify that it retrieves every item correctly."""
        total_results = []
        page_num = 1
        per_page_results = EmployeePaginationHelper(page_num=page_num, page_size=10).fetch_results(self.client)

        # Simulate navigating page by page to the last page
        while page_num <= per_page_results['pagingInfo']['totalNumPages']:
            page_num += 1
            total_results.extend(per_page_results['employeePage'])
            per_page_results = EmployeePaginationHelper(page_num=page_num, page_size=10).fetch_results(self.client)

        # Check equal number of results, uniqueness of results and ensure each result appears in the database
        self.assertEqual(len(total_results), self.total_num_items)
        self.assertTrue(len(set([e['id'] for e in total_results])), self.total_num_items)
        self.assertEqual(db_session.query(EmployeeModel.name.in_([e['name'] for e in total_results])).count(), self.total_num_items)


class EmployeePaginationHelper:
    """Convenience class for testing employee pagination."""

    def __init__(self, page_num, page_size, sorting_field=None, sorting_direction=None):
        self.page_num = page_num
        self.page_size = page_size
        self.sorting_field = sorting_field
        self.sorting_direction = sorting_direction


    def get_page_employee_query(self):
        """Convenience method for employee pagination queries."""
        template = """
            query offsetPagination {{
              employeePage(pagingParameters: {{ {params} }}) {{
                pagingInfo {{
                  pageNum
                  pageSize
                  totalNumPages
                  hasNextPage
                  hasPrevPage
                }}
                employeePage {{
                  id
                  name                  
                  salary
                  departmentId
                  department {{
                    name
                  }}
                }}
              }}
            }}
            """
        # Add input parameters as needed
        input_params = 'pageNum:{}, pageSize:{}'.format(self.page_num, self.page_size)

        if self.sorting_field is not None:
            input_params += 'sortingField: "{}"'.format(self.sorting_field)

        if self.sorting_direction is not None:
            if self.sorting_direction.value == 0:
                input_params += 'sortingDir: DESC'
            else:
                input_params += 'sortingDir: ASC'

        return template.format(params=input_params)


    def fetch_results(self, client):
        """Fetches the results from executing the query and traverses the first two layers."""
        return client.execute(self.get_page_employee_query())['data']['employeePage']
