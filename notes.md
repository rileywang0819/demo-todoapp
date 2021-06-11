# SQL & Data Modeling for the Web

- [1. Introduction](#1-introduction)
- [2. Interacting with Databases](#2-interacting-with-databases)
  - [2.1 Overview](#21-overview)
  - [2.2 Relational Databases](#22-relational-databases)
  - [2.3 SQL](#23-sql)
  - [2.4 Client-Server Model](#24-client-server-model)
  - [2.5 TCP/IP](#25-tcpip)
  - [2.6 Transactions](#26-transactions)
  - [2.7 DBAPIs and psycopg2](#27-dbapis-and-psycopg2)
  - [2.8 Summary](#28-summary)
- [3. SQLAlchemy Basics](#3-sqlalchemy-basics)
  - [3.1 Overview](#31-overview)
  - [3.2 SQLAlchemy's Layers of Abstraction](#32-sqlalchemys-layers-of-abstraction)
  - [3.3 Layers of SQLAlchemy](#33-layers-of-sqlalchemy)
    - [3.3.1 DBAPI](#331-dbapi)
    - [3.3.2 The Dialect](#332-the-dialect)
    - [3.3.3 The Connection Pool](#333-the-connection-pool)
    - [3.3.4 The Engine](#334-the-engine)
    - [3.3.5 SQL Expressions](#335-sql-expressions)
    - [3.3.6 SQLAlchemy ORM](#336-sqlalchemy-orm)
  - [3.4 Mapping Between Tables and Classes](#34-mapping-between-tables-and-classes)
  - [3.5 Hello APP with Flask-SQLAlchemy](#35-hello-app-with-flask-sqlalchemy)
- [4. SQLAlchemy ORM in Depth](#4-sqlalchemy-orm-in-depth)
  - [4.1 Model.query](#41-modelquery)
  - [4.2 SQLAlchemy Object Lifecycle](#42-sqlalchemy-object-lifecycle)
- [5. Build a CRUD App with SQLAlchemy ORM : Part I](#5-build-a-crud-app-with-sqlalchemy-orm--part-i)
  - [5.1 Overview](#51-overview)
  - [5.2 MVC: Model-View-Controller](#52-mvc-model-view-controller)
  - [5.3 Handling User Input](#53-handling-user-input)
    - [5.3.1 Getting user data in Flask](#531-getting-user-data-in-flask)
    - [5.3.2 Using AJAX to send data to Flask asynchronously](#532-using-ajax-to-send-data-to-flask-asynchronously)
    - [5.3.3 Using sessions in controllers](#533-using-sessions-in-controllers)
- [6. Migrations](#6-migrations)
  - [6.1 Introduction](#61-introduction)
  - [6.2 Flask Migrations](#62-flask-migrations)
  - [6.3 Work with existing data](#63-work-with-existing-data)
- [7. Build a CRUD App with SQLAlchemy ORM : Part II](#7-build-a-crud-app-with-sqlalchemy-orm--part-ii)
  - [7.1 Update a Todo Item](#71-update-a-todo-item)
  - [7.2 Delete a Todo Item](#72-delete-a-todo-item)
  - [7.3 Modeling Relationships](#73-modeling-relationships)
    - [7.3.1 Review: Relationships & Joins](#731-review-relationships--joins)
    - [7.3.2 db.relationship](#732-dbrelationship)
    - [7.3.3 Foreign Key Constraint Setup](#733-foreign-key-constraint-setup)
    - [7.3.4 One-to-Many Relationship Setup](#734-one-to-many-relationship-setup)

## 1. Introduction

**Goal:** learn the skills needed to traverse the stack and develop an entire database-backed web application.

**Tech stack:**

- programming language: Python 3
- web server framework: Flask
- database: PostgresSQL
- Python libraries:
  - psycopg2
  - SQLAlchemy
  - Flask-SQLAlchemy

`pip:` the pip comes preinstalled in the recent versions of Python. The pip is used to install specific Python packages that we need from the `Python Package Index (PyPI)`

**Final Project:** `Fyyur`

## 2. Interacting with Databases

### 2.1 Overview

1. Interacting with a (remote) database

Backend developers need to interact with databases on a regular basis in order to manipulate and maintain the models behind their web applications.

In working with a database, we'll need to use a `Database Management System (DBMS)`.

```text
A Database Management System (DBMS) is simply software that allows you to interact with a database (e.g.to access or modify the data in that database).
```

There are many different Database Management Systems out there, but the particular DBMS we'll be using is called `PostgreSQL` (or simply Postgres).

2. Database Application Programming Interfaces (DBAPIs)

Once we've looked at the basics of interacting with a database, we'll need to understand how to interface with that database from another language or web server framework (such as Python, NodeJS, Ruby on Rails, etc.). This is where `DBAPIs` come in.

3. psycopg2

Finally, we'll get some experience working with the widely used `psycopg2 library`, which will allow us to interact with a database from Python.

```text
psycopg2 is a database adapter(适配器) that allows us to interact with a Postgres database from Python.
```

---

Anything that implements the DB-API to connect to an external database can be reasonably called a database driver or database adapter. The two are pretty much interchangeable. Any DB-API implementation must be a Python module. Python modules are programming language libraries, in that they're collections of re-usable code. Some are also C shared libraries, in that they're compiled C code that gets linked into the CPython executable.

CPython是用C语言实现的Python解释器。

---

### 2.2 Relational Databases

Key characteristics of database:

![](imgs/key-characteristic-of-database.JPG)

1. Primary Keys & Foreign Keys

![](imgs/primary-key.JPG)
![](imgs/foreign-key.JPG)

### 2.3 SQL

![](imgs/SQL.JPG)

- Execution Plan(执行计划)

The `execution plan` gives important insight into the performance of the query. Since there can multiple ways of performing queries against a database with various performance tradeoffs, it's important to choose the one with the best execution plan for quickly and efficiently returning the results that you need.

🤠 Visit [database bootcamp](https://github.com/rileywang0819/database-bootcamp) to learn more SQL.

### 2.4 Client-Server Model

![](imgs/server-client-model.JPG)
![](imgs/request-and-response.JPG)

**A database client is any program that sends requests to a database. In some cases, the database client is a web server!**

![](imgs/db-web-server-with-client.JPG)

```text
Basically, we call things clients when they are making a request and servers when they are fulfilling a request with a repsonse.

Since a web server can do both, it sometimes acts as a server and sometimes acts as a client.
```

- Client-Server Model Example: Jane's Store

![](imgs/ex-jane-online-store.JPG)

Click the Polo product and show a product detail page as follows :

![](imgs/ex-jane-online-store2.JPG)

Let's look the steps under the hood :

- Clicking on the Polo product leads to a click event being registered by the browser, on the client computer.
- A click handler in the view would send a request, including information about the request type and any user input data, to the server (in Javascript) from the client browser.
- A client could request more data and a different view to be rendered (with that data).
- A server process listens to the request sent from the view, and uses the user input data to determine how to shape its request to the database, and sends a request to the database.
- The database processes this request, and sends a response back to the web server.
- The web server receives the response from the database, and uses it to determine the view + powers the view template with the fetched data, sending it back to the client's browser.
- The client is responsible for rendering something to the user, that represents both the data and its representation.

(`MVC: model-view-controller`)

Let's use some pseudocode to illustrate this process.

```jsx
// frontend

<!-- view.html -->
<div id="polo" data-id="1"> Polo </div>

document.getElementById("polo").onclick = function() {
  var request = new Request();
  request.send('GET product detail on product with id ', 1);  // send request
}

/**
request 2 things:
1. request more data;
2. reder a different page to the client web app
*/
```

```py
# backend (web server)

''' server.py '''

result = application.listen_on(request)

print(result.id)  # --> 1

"""
server does: (database)
1. send request to the database, about info about object with result.id;
2. receives the response and sends back info about the view and the data;
"""

application.render_view('product_details.html', data)
```

### 2.5 TCP/IP

- Transmission Control Protocol (TCP)
- Internet Protocol (IP)

TCP/IP is a suite of communication protocols that is used to connect devices and transfer data over the Internet.

![](imgs/TCP-IP.JPG)

- `Port 80`: The port number most commonly used for HTTP requests. For example, when a client makes a request to a web server, this request is usually sent through port 80.
- `Port 5432`: The port number used by most database systems; also the default port for PostgreSQL.

```text
Q: Why are ports used?

Ports allow multiple types of traffic being received at the same time on a given device, to be tracked and routed to where they need to go.

Ports are much like the different terminals of an airport, tracking and receiving different airplanes at the same time, allowing for the effective receipt of multiple types of traffic at the same IP address.
```

[Additional Resource : 14 of the most common ports](https://opensource.com/article/18/10/common-network-ports)

**TCP/IP is a connection-based protocal.** Over TCP/IP, we'll always need to establish a `connection` between clients and servers in order to enable communications.

- Open a connection to start communications.
- Close a connection to end communications. 

 Moreover :

- Deliveries over the connection are `error-checked`: if packets arrive damaged or lost, then they are resent (known as retransmission).


----
**Supplement: TCP vs UDP**

The internet also offers the UDP protocol. 
UDP is much simpler than TCP: hosts on the network send data (in units called datagrams) without any connections needing to be established.

If TCP is like building highways between houses before sending packages between them, then UDP is much like sending over a carrier pigeon from one house to another in order to deliver packages: you don't know whether the pigeon will head in the right way, drop your package along the way, or encounter an issue mid-travel. On the other hand, there is less overhead to use UDP than managing a connection over TCP / building a highway.

When speed is more important than reliability, especially when applications need to stream very small amounts of information quickly (smaller packages of information means less issues with reliability), then UDP is preferred. A lot of real time streaming applications, (e.g. live TV streaming, Voice over IP (VoIP)) prefer UDP over TCP. Since UDP does not need to retransmit lost datagrams, nor does it do any connection setup, there are fewer delays over UDP than TCP. TCP's continuous connection is more reliable but has more latency(时延).

---

![](imgs/session1.JPG)
![](imgs/session2.JPG)

### 2.6 Transactions

`Transactions(事务)` are atomic units of work for the database to perform as a whole.

![](imgs/transaction.JPG)
![](imgs/transaction2.JPG)
![](imgs/transaction3.JPG)

**Transactions capture logical bundles of work.**
Work is bundled into transactions, so that in case of system failures, data in your database is still kept in a valid state (by rolling back the entire transaction if any part of it fails). To ensure a database is consistent before and after work is done to it, databases uses atomic transactions, and actions like `commits` and `rollbacks` to handle failures appropriately. Transactions are, in other words, [ACID](https://www.geeksforgeeks.org/acid-properties-in-dbms/) .

![](imgs/bundle-work.JPG)

### 2.7 DBAPIs and psycopg2

We will sometimes want to interact with our database and use its results in a specific programming language. E.g. to build web applications or data pipelines in a specific language (Ruby, Python, Javascript, etc.). That's where `DBAPIs` come in.

`DBAPI:`

- provides a standard interface for one programming language (like Python) to talk to a relational database server;
- is a low level library for writing SQL statements that connect to a database;
- is also known as database adapters

Different DBAPIs exist for every server framework or language + database system.
Database adapters define a standard for using a database (with SQL) and using the results of database queries as input data in the given language.

```text
example: SELCET * FROM <table>

- list of rows into an array of objects in Javascript for say a NodeJS adapter;
- or a list of tuples in Python for a Python adapter
```

![](imgs/dbapis.jpg)

In this course, we use `psycopg2` to establish a connection to our postgres server, and interact with it in python.

Demos - see scripts in "psycopg2" folder : 

- psycopg2: basic usage
- psycopg2: string composition
- psycopg2: fetching results

### 2.8 Summary

With psycopg2, we can interact with PostgreSQL database in Python programming language. However, just like shown in demos, we still need to write SQL ourselves.

Writing SQL directly is a fairly clunky way of doing web development. It's useful to learn some higher level libraries that let us interact with a database, using Python classes and expressions. Let's get to learn one of the most powerful Python libraries for interacting with databases : `SQLAlchemy`.

## 3. SQLAlchemy Basics

### 3.1 Overview

SQLAlchemy

- SQLAlchemy is the most popular open-source library for working with relational databases from Python.
  - an end-to-end tool for working with relational databases without writing raw SQL (avoid SQL's dialect)
  - allows SQL clauses to be built via Python functions and expressions
  - avoids sending SQL to the database on every call. The SQLAlchemy ORM library features automatic caching, caching collections and references between objects once initially loaded
- It is one type of `ORM library`, a.k.a an `Object-Relational Mapping library`, which provides an interface for using object oriented programming to interact with a database.
  - maps tables and columns to class objects and attributes

![](imgs/SQLAlchemy-other-than-raw-SQL.JPG)
![](imgs/notes-on-ORM.JPG)

### 3.2 SQLAlchemy's Layers of Abstraction

![](imgs/sqlalchemy-abstract.JPG)
![](imgs/sqlalchemy-abstract2.JPG)

SQLAlchemy vs psycopg2 :

- SQLAlchemy **generates** SQL statements
- psycopg2 directly **sends** SQL statements to the database.
- SQLAlchemy depends on psycopg2 or other database drivers to communicate with the database, under the hood.

SQLALchemy lets you traverse through all 3 layers of abstraction to interact with your database.

- Can stay on the ORM level
- Can dive into database operations to run customized SQL code specific to the database, on the Expressions level.
- Can write raw SQL to execute, when needed, on the Engine level.
  - Can more simply use psycopg2 in this case

### 3.3 Layers of SQLAlchemy

**Overview :**

![](imgs/sqlalchemy-layers-of-abstraction.JPG)

#### 3.3.1 DBAPI

#### 3.3.2 The Dialect

The dialect layer allows us to forget about the database system we're using

[SQLAlchemy Docs on the Dialect](https://docs.sqlalchemy.org/en/14/dialects/)

#### 3.3.3 The Connection Pool

The connecting pool let's us avoid open and close connection manually using DBAPI alone. With connection pool, the opening and closing of connections and which connection you are using when you're executing statements within a session is completely abstracted.

![](imgs/connecting-pool.JPG)

#### 3.3.4 The Engine

![](imgs/sqlalchemy-engine1.JPG)

Moreover,

- The Engine in SQLAlchemy refers to both itself, the Dialect and the Connection Pool, which all work together to interface with our database.
- A connection pool gets automatically created when we create a SQLAlchemy engine.

[SQLAlchemy Docs on the Engine](https://docs.sqlalchemy.org/en/14/core/engines.html)

#### 3.3.5 SQL Expressions

Instead of sending raw SQL (using the Engine), we can compose SQL statements by building Python objects.

![](imgs/sqlalchemy-sql-expression.JPG)

#### 3.3.6 SQLAlchemy ORM

Moreover, with SQLAlchemy ORM, you can compose SQL expressions by building Python classes of objects which map to tables in the database -- **Maps classes to tables**

![](imgs/sqlalchemy-orm.JPG)

### 3.4 Mapping Between Tables and Classes

![](imgs/map-class-table.JPG)

### 3.5 Hello APP with Flask-SQLAlchemy

`Flask:` A very simple web framework for serving web pages with data

`Flask-SQLAlchemy:` a Flask extension that supports SQLAlchemy

**demo:** see 'flask-sqlalchemy' folder

**Running the flask app:**

```shell
# start the server
# specify the location of the flask app
~$ FLASK_APP=flask_hello_app.py flask run

# alternative way:
~$ python flask_hello_app.py
```

**Connect to database :**

![](imgs/database-connection-uri-parts.JPG)

By default, SQLAlchemy will automatically choose which DBAPI you use underneath.You can also optionally specify it (for Python application psycopg2 is the default database adpater).

```py
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pupu0819@localhost:5432/example'
db = SQLAlchemy(app)
```

**Map class to tables :**

- `db.Model` lets us create and manipulate data models
- `db.session` lets us create and manipulate database transactions
- `db.create_all()` will detect models and creates tables for them (if they don't exist)

```text
SQLAlchemy names the table by the name of the class, all lower cased, by default. 

Then, if it finds a table with that name already, regardless of whether the schema matches the class, it will skip creating another table by that same name, and do nothing.
```

**SQLALchemy data type :**

![](imgs/screen-shot-2019-08-18-at-11.36.57-pm.JPG)

**SQLAlchemy constraints :**

- Column constraints ensure data integrity across our database, allowing for database accuracy and consistency.
- Constraints are conditions on your column, that provide checks on the data's validity. It does not allow data that violates constraints to be inserted into the database (it will raise an error if you attempt to).
- In SQLAlchemy, constraints are set in db.Column() after setting the data type.

```py
# column contraint demo
class User(db.Model):
  name = db.Column(db.String(), nullable=False, unique=True)

# check constraint
class Product(db.Model):
  """ensures that no product goes into the table with a nonpositive price value"""
  price = db.Column(db.Float, db.CheckConstraint('price>0'))
```

## 4. SQLAlchemy ORM in Depth

### 4.1 Model.query

- `db.Model.query` offers us the Query object. The Query object lets us generate SELECT statements that let us query and return slices of data from our database.
- Query has method chaining.
- The Query object can be accessed on a model using either:
  - `MyModel.query` directly on the model, 
  - or `db.session.query(MyModel)` using `db.session.query` instead.

**Useful query methods:**

- Select records

```py
MyModel.query.all()
"""same as doing a SELECT *, fetching all records from the model's table. Returns a list of objects."""

MyModel.query.first()
"""Fetches just the first result. Returns either None or an object if found."""
```

- Filtering

```py
MyModel.query.filter_by(my_table_attribute='some value')
"""Similar to doing a SELECT * from ... WHERE SQL statement for filtering data by named attributes."""

OrderItem.query.filter(Product.id=3 Product.name=computer)
"""Similar to filter_by, but instead, you specify attributes on a given Model."""
```

See [common filter operators](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#common-filter-operators) for more filtering.

- Ordering

```py
MyModel.order_by(db.desc(MyModel.created_at))
"""To order the results by a given attribute. Use db.desc to order in descending order."""

Order.query.limit(100).all()
"""limit(max_num_rows) limits the number of returned records from the query. ala LIMIT in SQL."""
```

- Aggregates

```py
query = Task.query.filter(completed=True)
query.count()
"""Returns an integer set to the number of records that would have been returned by running the query."""

model_id = 3
MyModel.query.get(model_id)
"""Returns the object as a result of querying the model by its primary key."""
```

- Bulk Deletes(批量删除)
  
```py
query = Task.query.filter_by(category='Archived')
query.delete()
"""delete() does a bulk delete operation that deletes every record matching the given query."""
```

- Joined Queries

```py
Driver.query.join('vehicles')
"""Query has a method join(<table_name>) for joining one model to another table."""
```

![](imgs/model-query-2-ways.JPG)

### 4.2 SQLAlchemy Object Lifecycle

- Within a session, we create transactions every time we want to commit work to the database.
- Proposed changes are not immediately committed to the database and instead go through stages to allow for undos.
- The ability to undo is allowed via `db.session.rollback()`

![](imgs/life-cycle.JPG)
![](imgs/life-cycle2.JPG)
![](imgs/life-cycle3.JPG)

Let's dive into Flush stage.

![](imgs/flush.JPG)
![](imgs/life-cycle4.JPG)

Especially, when a statement has been flushed already, SQLAlchemy knows not to do the work again of translating actions to SQL statements (caching).

## 5. Build a CRUD App with SQLAlchemy ORM : Part I

### 5.1 Overview

| Operation | SQL | SQLAlchemy ORM |
| :---: | :---: | :---: |
| CEATE | INSERT | db.session.add(users) |
| READ | SELECT | db.session.query(User) or User.query.all() |
| UPDATE | UPDATE | user1.foo = 'new value' |
| DELETE | DELETE | db.session.delete(user1) |

We will master the following skills in this section:

- Traversing across all layers of our backend stack, from our backend server in Flask to our database in Postgres, by understanding mappings between user operations, to the ORM, to the SQL executed on a database.
- Developing using the MVC (Model-View-Controller) pattern, for architecting out our application
- Handling changes to our data schema over time
- Modeling relationships between objects in our web application
- Implementing Search

### 5.2 MVC: Model-View-Controller

- `MVC` stands for Model-View-Controller, a common pattern for architecting web applications
- Describes the 3 layers of the application we are developing
  - Models manage data and business logic for us. What happens inside models and database, capturing logical relationships and properties across the web app objects
  - Views handles display and representation logic. What the user sees (HTML, CSS, JS from the user's perspective)
  - Controllers: routes commands to the models and views, containing control logic. Control how commands are sent to models and views, and how models and views wound up interacting with each other.

![](imgs/MVC.JPG)

```html
<!-- views -->
<h1>My Todo App</h1>
```

```py
# models
Todo.query.all()

# controllers
render_template('index.html', data=data)
```

### 5.3 Handling User Input

Creating, updating, and deleting information from a database requires handling user input on what is being created/updated/deleted.

![](imgs/MVC-with-user-input.JPG)

What we will learn next are:

- **How we accept and get user data** in the context of a Flask app
- **Send data in controllers** using database sessions in a controller
- **Manipulating models** adding records in SQLAlchemy Models
- **Direct how the view should update** within the controller and views

#### 5.3.1 Getting user data in Flask

There are 3 methods of getting user data from a view to a controller.

- URL query parameters
- Forms
- JSON

![](imgs/get-user-data.JPG)
![](imgs/get-user-data2.JPG)

**Using HTML form submission to get the data:**

- forms take an `action` (name of the route) and `method` (route method) to submit data to our server.
- The `name` attribute on a form control element is the key used to retrieve data from `request.get(<key>)`.
- All forms either define a submit button, or allow the user to hit ENTER on an input to submit the form.

![](imgs/submit-data-with-HTML-form.JPG)

**Form methods:**

The way form data traverses from the client to server differs based on whether we are using a `GET` or a `POST` method on the form.

1. The POST submission : On submit, we send off an HTTP POST request to the route "/create" with a request body.
The request body stringifies(字符串化) the key-value pairs of fields from the form (as part of the name attribute) along with their values.
2. The GET submission : Sends off a GET request with URL query parameters that appends the form data to the URL, which is ideal for smaller form submissions.

POSTs are ideal for longer form submissions, since URL query parameters can only be so long compared to request bodies (max 64K, i.e. 2048 characters). Moreover, forms can only send POST and GET requests, and nothing else.

![](imgs/post-vs-get.JPG)
![](imgs/post-vs-get2.JPG)

*Click [here](https://www.oschina.net/news/77354/http-get-post-different) to see more details about POST and GET.*

Read more about [sending form data](https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data)

#### 5.3.2 Using AJAX to send data to Flask asynchronously

There are 2 ways to do data request from the client to the server.

- do synchronously(同步)
- do asynchronously(异步)
  - Async data requests are requests that get sent to the server and back to the client without a page refresh.

---

1. 什么是AJAX？

AJAX: Asynchronous Javascript + XML

如果网页没有使用AJAX技术，你点一个按钮就要刷新一下页面，尽管新页面上只有一行字和当前页面不一样，但你还是要无聊地等待页面刷新。用了AJAX之后，你点击，然后页面上的一行字就变化了，页面本身不用刷。AJAX只是一种技术，不是某种具体的东西。不同的浏览器有自己实现AJAX的组件。

而所谓异步，在这里简单地解释就是：向服务器发送请求的时候，我们不必等待结果，而是可以同时做其他的事情，等到有了结果我们可以再来处理这个事。

2. 什么是同步请求？什么是异步请求？

同步请求的原理：当浏览器向服务器发送同步请求时，服务处理同步请求的过程中，浏览器会处于等待的状态，服务器处理完请求把数据响应给浏览器并覆盖浏览器内存中原有的数据，浏览器——重新加载页面并展示服务器响应的数据。


异步请求的原理：浏览器把请求交给代理对象—XMLHttpRequest（绝大多数浏览器都内置了这个对象），由代理对象向服务器发起请求，接收、解析服务器响应的数据，并把数据更新到浏览器指定的控件上。从而实现了页面数据的局部刷新。

![](imgs/sync-async.jpg)

---

There are various libraries (such as axios and JQuery) candidates can be used to send AJAX requests from the client. But no matter what library you use, under the hood, you are using two methods to send AJAX request (Async requests) :

- XMLHttpRequest
- Fetch (modern way)

1. XMLHttpRequest

```js
// build out request object
var xhttp = new XMLHttpRequest();

// fetch the data from the DOM
description = document.getElementById("description").value;

// open a connection from client to the server
xhttp.open("GET", "/todos/create?description=" + description);

// send the request and close the connection
xhttp.send();
```

In a synchronous request, when you finish processing your requests on the server, the server dictates(命令) how the view should then update.

In a asynchronous request, it is on the client side that you react to the server and you figure out how to update the DOM that is already loaded on the client based on the request you get.

```js
/* XMLHttpRequest on success */

xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) { 
      // on successful response
      console.log(xhttp.responseText);
    }
};


/**
1. this.readyState === 4: indicates that the operation on a server has already been completed;

2. this.status === 200: indicates that the reponse is successful
*/
```

2. Fetch

With fetch, in order to send a request to the server, we would specify fetch and then pass the request to the URL route, followed by a request object where you can specify the method as well as the request body, followd by any possible custom header.

```js
fetch('/my/request', {
  method: 'POST',
  body: JSON.stringify({
    'description': 'some description here'
  }),
  headers: {
    'Content-Type': 'application/json'
  }
});
```

The Fetch API provides a fetch() method defined on the window object, which you can use to perform requests. This method returns a Promise that you can use to retrieve the response of the request.

Appendix: click to learn more [fetch](https://developers.google.com/web/updates/2015/03/introduction-to-fetch) and [promise](https://zhuanlan.zhihu.com/p/26523836)

#### 5.3.3 Using sessions in controllers

- Commits can succeed or fail.
- On fail, we want to rollback the session to avoid potential implicit commits done by the database on closing a connection;
- Close connections at the end of every session used in a controller, to return the connection back to the connection pool.

```py
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit() 
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # jsonify:return json data to the client
        return jsonify({
            'description': todo.description
        })
```

If we do things like above, when we run the app, the terminal will show error message, and the view will show error information.

```shell
~$ python app.py
...
sqlalchemy.orm.exc.DetachedInstanceError: Instance <Todo at 0x18d2c644e48> is not bound to a Session; attribute refresh operation cannot proceed
```

But check the database, the new todo record has already created. Why this happened?

See the code. Actually, we close the session before returning json data to the client. It's like our todo objects was detached from our session.

There is a default setting that is applied to every database session instance.

![](imgs/expire_on_commit.JPG)

Additionally, the route handler should always return something or raise an intentional exception, in the case of an error. To fix this with a simple solution, we can simply import abort from Flask:

```py
from flask import abort
```

and we can call `abort(<status code>)`, e.g. with status code 500, `abort(500)` to rise an HTTPException for an Internal Server Error, in order to abort a request and prevent it from expecting a returned result.

## 6. Migrations

Until now, we have learned how to handling READ and CREATE data, and MVC pattern. We have also learned how to send request asynchronously using AJAX.

In this section, we will learn how to change our data models over time.

### 6.1 Introduction

![](imgs/migration-goal.JPG)
![](imgs/what-is-migration.JPG)

```text
Upgrades and Rollbacks

- Migrations stack together in order to form the latest version of our database schema;
- We can upgrade our database schema by applying migrations;
- We can roll back our database schema to a former version by reverting migrations that we applied
```

Migrations:

- encapsulate a set of changes to our database schema, made over time.
- are uniquely named
- are usually stored as local files in our project repo, e.g. a "migrations/" folder
- There should be a 1-1 mapping between the changes made to our database, and the migration files that exist in our migrations/ folder.
- Our migrations files set up the tables for our database.
- All changes made to our db should exist physically as part of migration files in our repository.

There are generally 3 migration command line scripts needed :

- `migrate:` creating a migration script template to fill out ; generating a migration file based on changes to be made
- `upgrade:` applying migrations that hadn't been applied yet ("upgrading" our database)
- `downgrade:` rolling back applied migrations that were problematic ("downgrading" our database)

The migration tool that we use is going to differ based on which framework we use. For Flask, we typically use `FLASK-Migrate` and `Flask-Script`.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is our migration manager for migrating changes using SQLAlchemy. It uses a library called [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) underneath the hood.
- `Flask-Script` (flask_script) lets us run migration scripts we defined, from the terminal

```text
Flask-Migrate autodetects changes in our SQLAlchemy models, but we still have to manually run the migrations ourselves (using Flask-Script underneath).
```

Finally, let's talk about why use migrations.

![](imgs/manage-changes-to-the-schema.JPG)

Without Migrations vs With Migrations

![](imgs/without-migration.JPG)
![](imgs/with-migration.JPG)

### 6.2 Flask Migrations

```text
Migration就是一些管理数据库结构的文件，这些文件其实都是抽象化的SQL，可以通过命令行执行而改变数据库的结构，这些文件都是存放在项目下的，随着项目版本的迭代而迭代。

即使没有migration,我们也可以使用SQL来实现数据库结构的改变。然而，
1） 手写SQL是很麻烦的；
2） team-work的时候，如果数据库的某个表只是发生了一个微小的变动，我们也需要将这个变动的SQL传给每个开发组员，让他们在本地手动更新，这是很麻烦的。

在开发过程中，如果一位小伙伴改动了数据库的表结构，她只需要生成一个migration文件并推送到版本控制系统中，如：Git，并通知其他小伙伴，其他小伙伴只需要pull然后在命令行执行下migration命令就可以了，简化了传统的数据库变动流程，加快项目的开发。

Using migration allows us to have version control over our database schema.
```

While we can extend the model using `psql` or another Postgres client to simply alter our table to add a new column using the `ALTER TABLE ADD COLUMN` command in SQL, we should use migrations to handle changes to our database schema for better maintainability and the ability to rollback quickly in case of issues.

- Creat initial migrations folder structure

```shell
~$ flask db init
```

- Sync models

Detect the model changes to be made, and create a migration file with upgrade and sowngrade logic set up.

```shell
~$ flask db migrate

# or with message
~$ flask db migrate -m "Initial migration."
```

- Upgrade & downgrade

Runs the upgrade/downgrade commande in the migration file, to apply the migration

```shell
~$ flask db upgrade

~$ flask db downgrade
```

![](imgs/recap-flask-migrate.JPG)

### 6.3 Work with existing data

```py
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    # add a new column
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id}, {self.description}>'
```

If we run `flask db upgrade`, it will cause `NotNullViolation Error`. This is because we declared that the completed column shouldn't be null. In this context, we can revise the migration file like below:

```py
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=False))
    """ Modify from False to True, so we can add a column that applies to our
    existing data successfully. """
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))

    """ add the following two lines """

    # update the existing recoreds that don't yet have a 
    # completed column with SQL
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')

    # update the column on todos
    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###
```




## 7. Build a CRUD App with SQLAlchemy ORM : Part II

### 7.1 Update a Todo Item

An update involves setting the attributes of an existing object in the database.

In SQL:

```SQL
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

In SQLAlchemy ORM:

```py
user = User.query.get(some_id)
user.name = 'Some new name'
db.session.commit()
```

### 7.2 Delete a Todo Item

Deletes deal with removing existing objects in our database

In SQL:

```SQL
DELETE FROM table_name
WHERE condition;
```

In SQLAlchemy ORM:

```py
todo = Todo.query.get(todo_id) 
db.session.delete(todo) # or...
Todo.query.filter_by(id=todo_id).delete()
db.session.commit()
```

![](imgs/delete-steps.JPG)

### 7.3 Modeling Relationships

The relationships between models can determine if certain actions on one model should happen on other models, so that when something happens to one model, related model objects should also be affected (by being created, read, updated, or deleted).

Examples are:

- Removing a User's account should remove all of that user's photos, documents, etc.
- Deleting a Discussion Thread should delete all of its comments.
- Deactivating the profile of an Airbnb host should deactivate all of that host's listings.
- Accessing a Blog Post should also access all of its comments.
- Accessing an Airbnb host's profile should also access all of their listings.

In order to handle CRUD across related models that can often have relationships with one another, we'll need to learn about how we model relationships, both reviewing relationship modeling in SQL and learning particularly about how we implement them in SQLAlchemy ORM.

Let's put aside our To-Do app development for now to learn about mapping relationships between models. Once we've done that, we'll come back to our To-Do app to implement them.

#### 7.3.1 Review: Relationships & Joins

![](imgs/relational-mapping.JPG)

We retrieve information accross tables using foreign keys.

![](imgs/relational-mapping2.JPG)
![](imgs/relational-mapping3.JPG)

#### 7.3.2 db.relationship

SQLAlchemy configures the settings between model relationships once, and generates JOIN statements for us whenever we need them.

`db.relationship:` an interface offered by SQLAlchemy to provide and configure a mapped relationship between two models.

![](imgs/db-relationship.JPG)

```py
child1 = SomeChild(name='Andrew')
child1.some_parent  # returns the parent object that child1 object belongs to

""" db.relationship allows you to configure when joined assets should be loaded """
```

So when do we load `child1.some_parent` from the database?

![](imgs/load-pattern-importance.JPG)

There are two different ways that we can optimize the loading of joined assets: Lazy loading & Eager loading

- Lazy loading

**Load needed joined data only as needed. Default in SQLAlchemy.**

Pro: no initial wait time. Load only what you need.

Con: produces a join SQL call every time there is a request for a joined asset. Bad if you do this a lot.

`lazy=True` (lazy loading) is the default option in `db.relationship`:

```py
children = db.relationship('ChildModel', backref='some_parent', lazy=True)
```

- Eager loading

**Load all needed joined data objects, all at once.**

Pro: reduces further queries to the database. Subsequent SQL calls read existing data

Con: loading the joined table has a long upfront initial load time.

- Other loading options we can use

See the [SQLAlchemy Docs on Relationship Loading Techniques](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html) for more loading options.

Besides lazt loading and eager loading, there are also a couple of other options that you can set on relationships. The two very handy options are:

- collection_class
- cascade

![](imgs/optional-relationship.JPG)

```py
class Parent(db.Model):
  ...
  children = db.relationship(
    ...
    collection_class = list,
    cascade = 'save-update'
  )

'''
collection_class = list: whether or not we want the collection of children to be set equal to the data type list, or we want to set it to a dictionary or set in Python instead
'''

'''
cascade(级联)
'''
```

Check [SQLALchemy ORM Relationship Docs](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) for more possible ways.

[SQLAlchemy 1.4 Doc (zh version)](https://www.osgeo.cn/sqlalchemy/orm/cascades.html#cascade-save-update)

#### 7.3.3 Foreign Key Constraint Setup

![](imgs/db-relationship2.JPG)

- `db.relationship` does not set up foreign key constraints for you. We need to add a column, `some_parent_id`, on the child model that has a foreign key constraint
- Whereas we set db.relationship on the **parent** model, we set the foreign key constraint on the **child** model.
- A foreign key constraint prefers **referential integrity** from one table to another, by ensuring that the foreign key column always maps a primary key in the foreign table.

![](imgs/refer-foreign-key-with-primary-key-id.png)

So how this is done using SQLAlchemy?

![](imgs/db-foreign-key.JPG)
![](imgs/setup-foreign-key-constraint.JPG)

Resources : [SQLAlchemy Docs on Defining Constraints](https://docs.sqlalchemy.org/en/14/core/constraints.html)

Now, let's look at an example.

![](imgs/exercise.JPG)

```py
# Solution

class Driver(db.Model):
  __tablename__ = "drivers"
  id = db.Column(db.Integer, primary_key=True)
  ...
  vehicles = db.relationship('Vehicle', backref='driver', lazy=True)

class Vehicle(db.Model):
  __tablename__ = "vehicles"
  id = db.Column(db.Integer, primary_key=True)
  make = db.Column(db.String(), nullable=False)
  ...
  driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
```

#### 7.3.4 One-to-Many Relationship Setup

Now that we've reviewed how to use `db.relationship` and `db.ForeignKey` to set up relationships between models, let's focus back on our To-Do App and use these concepts to model To-Do Lists in our app and set up the relationship between our **To-Do model** and our new **To-Do List model**.

```text
To-Do Lists have many To-Dos, and every To-Do belongs to exactly one To-Do List, which indicates the existence of a one to many relationship between To-Dos and To-Do Lists.
```

Reading: [3 Types of Relationships in Database Design](https://database.guide/the-3-types-of-relationships-in-database-design/)

**Overall steps taken:**

![](imgs/overall-steps-taken.JPG)

![](imgs/example-of-terminal-output.JPG)

Add items with a list "Urgent" with ID of 2 and check if we get the expected results.

```shell
>>> from app import db, TodoList, Todo
>>> list = TodoList(name='urgent')
>>> todo = Todo(description='This is a really important thing.')
>>> todo2 = Todo(description='Urgent todo 2')
>>> todo3 = Todo(description='Urgent todo 3')
>>> todo.list = list
>>> todo2.list = list
>>> todo3.list = list
>>> todo.completed = False
>>> todo2.completed = False
>>> todo3.completed = False
>>> db.session.add(list)
>>> db.session.commit()
```

7.3.5 Many-to-Many Relationship

![](imgs/relationship-type.JPG)
![](imgs/relationship-type2.JPG)
![](imgs/relationship-type3.JPG)

Takeaways
- In one-to-many and one-to-one, the foreign key is established on the child model.
- In many-to-many, a special **association table** exists to join the two tables together, storing two foreign keys that link to the two foreign tables that have a relationship with each other.

- Setup many-to-many relationships

![](imgs/setup-many-to-many.JPG)

To set up a many-to-many in SQLALchemy, we:

- Define an association table using Table from SQLAlchemy
- Set the multiple foreign keys in the association table
- Map the association table to a parent model using the option secondary in db.relationship

![](imgs/setup-many-to-many2.JPG)
