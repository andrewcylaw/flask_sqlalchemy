from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Initializes the database with some starter data.
    """
    from server.model.department import Department
    from server.model.employee import Employee
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create the fixtures
    engineering = Department(name='Engineering')
    hr = Department(name='Human Resources')
    marketing = Department(name='Marketing')

    db_session.add_all([engineering, hr, marketing])
    db_session.add(Employee(name='Peter', salary=50000, department=engineering))
    db_session.add(Employee(name='Roy', salary=75000, department=engineering))
    db_session.add(Employee(name='Tracy', salary=25000, department=hr))

    # Arbitrarily produce data
    for i in range(50):
        if i % 3 == 0:
            db_session.add(Employee(name='George #' + str(i), salary=25000 + i, department=hr))
        elif i % 2 == 0:
            db_session.add(Employee(name='Samuel #' + str(i), salary=60000 - i, department=marketing))
        else:
            db_session.add(Employee(name='Albert #' + str(i), salary=12000 - i, department=engineering))

    db_session.commit()
