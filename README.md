# Simple GraphQL - Flask - SQLAlchemy Application

## Project Setup
0. **Requirements: Python, pip, and virtualenv**
1. Clone this repository `git clone https://github.com/andrewcylaw/flask_sqlalchemy.git` and `cd flask_sqlalchemy`
2. From the root directory, create a virtual env: `virtualenv env`.
3. Activate the virtual env (I used Windows powershell): `.\env\Scripts\activate.ps1`
4. Install the dependencies in the virtual env: `pip install -r requirements.txt`
5. Start the Flask app: `python ./server/app.py`
6. Open `http://127.0.0.1:5000/` to use GraphiQL and run queries.
7. To run tests: 
```
cd ./server
python -m unittest discover
```


## Interview Questions

**What are some of the challenges in implementing this solution on a database that constantly adds, deletes and updates records?**

* There is the possibility that some items are either skipped altogether or shown twice.
* Items can shift positions in the database if the database has been modified after the user loads a page but before the load the next one and rows have been inserted before/after the pagination offset. 


**What other approaches can you think of in implementing this solution if some of these
constraints does not exist?**

* Right now, offset-based pagination via Relay can't be used out of the box because Facebook's implementation of Relay was not built with windowed pagination in mind.
* So if we did not have the constraint of going to a page N or being able to navigate to the previous page, we would be able to use Relay's built-in connections/edges via cursor-based navigation.
* (It is possible to implement offset-based pagination using Relay, but apparently it uses some trickery to stash node cursors in a stack to emulate pages. [referenced from here](https://engineering.dubsmash.com/bi-directional-pagination-using-graphql-relay-b523c919c96))

## Sample Queries

* Employee creation
```
mutation createEmployee {
  createEmployee(input: {name: "Andrew Law :)", hiredOn: "2019-10-01T00:00:00Z", salary: 5, departmentId: 1}) {
    employee {
      id
      name
      hiredOn
      salary
      departmentId
    }
  }
}

```
* Pagination without sorting 
```
query offsetPagination {
  employeePage(pagingParameters: {pageNum: 1, pageSize: 10}) {
    pagingInfo {
      pageNum
      pageSize
      totalNumPages
      hasNextPage
      hasPrevPage
    }
    employeePage {
      id
      name
      departmentId
      salary
    }
  }
}
```
* Pagination sorting by descending salary 
```
query offsetPagination {
  employeePage(pagingParameters: {pageNum: 3, pageSize: 10, sortingField: "salary", sortingDir: DESC}) {
    pagingInfo {
      pageNum
      pageSize
      totalNumPages
      hasNextPage
      hasPrevPage
    }
    employeePage {
      id
      name
      departmentId
      salary
    }
  }
}
```
* Pagination sorting by ascending department (optional sorting direction omitted)
```
query offsetPagination {
  employeePage(pagingParameters: {pageNum: 2, pageSize: 7, sortingField: "department"}) {
    pagingInfo {
      pageNum
      pageSize
      totalNumPages
      hasNextPage
      hasPrevPage
    }
    employeePage {
      id
      name
      departmentId
      salary
    }
  }
}
```

## Misc. Implementation Notes
* Unit tests are implemented using Python's builtin package `unittest`.
* Department (and other fields) is not mandatory in the employee table, making it possible to create employees with `null` departments.
