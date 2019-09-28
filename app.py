from flask import Flask
from flask_graphql import GraphQLView

from database import db_session, init_db
from schema import schema


app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

# 127.0.0.1:5000/list
# app.add_url_rule(
#     '/list'
# )
#
# app.add_url_rule(
#     '/post'
# )

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run()
