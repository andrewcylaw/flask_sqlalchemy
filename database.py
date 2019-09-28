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
    from models import Department, Employee
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create the fixtures
    engineering = Department(name='Engineering')
    hr = Department(name='Human Resources')

    db_session.add_all([engineering, hr])
    db_session.add(Employee(name='Peter', department=engineering))
    db_session.add(Employee(name='Roy', department=engineering))
    db_session.add(Employee(name='Tracy', department=hr))

    db_session.commit()
