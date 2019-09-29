from unittest import TestCase, main
from graphene.test import Client
from OLDschema import schema


class SchemaTestCase(TestCase):

    def test_conn(self):
        client = Client(schema)
        executed = client.execute('''
        query allEmp {
          allEmployees {
            edges {    
              node {
                id
                name
                salary
                department {
                  name
                }
              }
            }
          }
        }''')
        self.assertEquals(executed, "asdasdkjbasdbjk")

if __name__ == '__main__':
    main()