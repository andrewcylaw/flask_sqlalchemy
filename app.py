from flask import Flask, jsonify
from flask_graphql import GraphQLView

from database import db_session, init_db
from schema import schema
from models import Employee as EmployeeModel


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

@app.route('/list-employees', methods=['GET'])
def list_employees():
    return jsonify([e.serialize for e in db_session.query(EmployeeModel).all()])


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run()
