from flask import Flask, request
from server.database import db_session, init_db
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.route('/employees/list', methods=['GET'])
def list_employees():
    return schema.Employee.list()


@app.route('/employees/page', methods=['GET'])
def page_employees():
    page_num = request.args.get('page')
    pass


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run()
