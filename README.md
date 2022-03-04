# Individual Project

## Table of contects
- [About The Project](#about-the-project)
  * [Information about student](#information-about-student)
  * [Features](#features)
- [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Folders structure and Files description](#folders-structure-and-files-description)
- [Usage](#usage)
  * [Instructions for executing the Flask application and unit tests](#instructions-for-executing-the-flask-application-and-unit-tests)
  * [Default database product value](#default-database-product-value)
  * [Unit test details](#unit-test-details)
  * [Usage and JSON format of web service (requests and responses)](#usage-and-json-format-of-web-service-requests-and-responses)
- [Discussion of adopting advanced technologies](#discussion-of-adopting-advanced-technologies)
  * [1. Publish subscribe messaging](#1-publish-subscribe-messaging)
  * [2. Asynchronous programming](#2-asynchronous-programming)
-   [License](#license)

# About The Project
In this project, I build an online shopping application with web service access.
In addition to the server program, I also develop associated tests and documentation. Furthermore, I will discuss two advanced technologies can be used in future.

## Information about student
-   Student Name: Cheng Wong Kwan

## Features

1.  Web service APIs
    1.  Query a product
        -   Input: product ID
        -   Return: all attributes of the product.
    2.  Buy a product
        -   Inputs: product ID, quantity (integer) to buy, and a credit-card number (a string of 16 digits)
        -   Action: updates the quantity in stock if appropriate
        -   Returns either:
            1.  success status and the amount deducted from the credit card
            2.  failure status and the failure reason
    3.  Replenish a product
        -   Inputs: product ID and a quantity (integer) to replenish the stock of the product
        -   Action: updates the quantity instock if appropriate
        -   Return: returns a success status
2.  Server execution ID
    -   The server uses an execution ID that is unique for each execution of the server program.
    -   SHA256 checksum of TCP daytime (from time-b-g.nist.gov)
3. Data persistence
    -   This project use `flask_sqlalchemy` with `SQLite` as a database (described below)
4. Concurrency access
    -   This project avoid race conditions and implement mutual exclusion
5. Unit tests
    -   Unit tests for buy, query, replenish, server operations (described below)
6. Discussion of adopting advanced technologies
    -   This project will discuss how to adopt advanced technologies in Unit 11 and Unit 12 (described below)

> This project is develop under Windows 10. MacOS and Linux is not compatible.

> Python version is 3.9.7

# Getting Started
## Installation

The project file provided a `requirements.txt`. 

The following command will install the packages according to the configuration file `requirements.txt`. 
```sh
cd projectpath
pip install -r requirements.txt
```
> `projectpath` is the path of project.

> make sure your current working directory is the project file

Or you can use the following command, `path/to/requirements.txt` is the path you put `requirements.txt`
```sh
pip install -r path/to/requirements.txt
```

If you want to install the package in your own way, these are the package and its version.
```
click==8.0.3
colorama==0.4.4
Flask==2.0.2
Flask-SQLAlchemy==2.5.1
greenlet==1.1.2
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.0.1
python-dotenv==0.19.2
SQLAlchemy==1.4.28
Werkzeug==2.0.2
```
## Briefly description of third-party libraries
-   [Flask]: a micro web framework

-   [Flask-SQLAlchemy]: an extension for Flask that adds support for SQLAlchemy

-   [python-dotenv]: reads the key,value pair from .env and adds them to environment variable


***
## Folders structure and Files description

```
project/
├── .env                            Flask configuration variables
├── README.md                       README file
├── config.py                       Set Flask configuration from .env file
├── requirements.txt                Install the packages
├── src/
│   ├── __init__.py                 Initialize Flask app
│   ├── database/
│   │   ├── models.py               Data models for database
│   │   └── products_data.db        SQLite database
│   ├── lib/
│   │   └── lib_routes.py           Flask routes library (exe_id, validation)
│   ├── main.py                     Main program to run Flask App (Entry point)
│   └── routes.py                   Flask Application routes (buy, query, replenish)
└── tests/
    ├── lib/
    │   └── lib_tests.py            Unit test library (ws_client)
    ├── test_all.py                 Unit test for all (buy, query, replenish, common)
    ├── test_buy.py                 Unit test for buy
    ├── test_query.py               Unit test for query
    ├── test_replenish.py           Unit test for replenish
    └── test_server_common.py       Unit test for server common operations
```

# Usage

## Instructions for executing the Flask application and unit tests

1. Config the variables in `.env`

    Deafult value, you can change or not change the following variables:
    -   SQLALCHEMY_DATABASE_URI=sqlite:///database\\\products_data.db
    -   FLASK_RUN_HOST=localhost
    -   FLASK_RUN_PORT=5000 
2. Run the Unit test
    -   If you want to test all cases (buy, query, replenish, common)
        -   Run `test_all.py`            
            ```sh
            cd projectpath
            python projectpath\tests\test_all.py
            ```
            > `projectpath` is the path of project.
        -   You can also comment out the test case you don't want
            ```python
            # comment out test cases (buy and replenish)
            #testcase_buy = unittest.TestLoader().loadTestsFromModule(test_buy)
            #unittest.TextTestRunner(verbosity=2).run(testcase_buy)

            testcase_query = unittest.TestLoader().loadTestsFromModule(test_query)
            unittest.TextTestRunner(verbosity=2).run(testcase_query)

            #testcase_replenish = unittest.TestLoader().loadTestsFromModule(test_replenish)
            #unittest.TextTestRunner(verbosity=2).run(testcase_replenish)

            testcase_common = unittest.TestLoader().loadTestsFromModule(test_server_common)
            unittest.TextTestRunner(verbosity=2).run(testcase_common)
            ```
    -   If you want to run specific test case only
        -   run `test_buy.py` for testing buy operation 
        -   run `test_query.py` for testing query operation 
        -   run `test_replenish.py` for testing replenish operation 
        -   run `test_server_common.py` for testing server common operation
            ```sh
            cd projectpath
            python projectpath\tests\test_buy.py
            python projectpath\tests\test_query.py
            python projectpath\tests\test_replenish.py
            python projectpath\tests\test_server_common.py
            ```  
3. Wait until Unit test pass 
4. Run the Flask Application
    -   Run the `main.py` 
        ```sh
        cd projectpath
        python projectpath\src\main.py
        ```  
        > time-b-g.nist.gov: a server more frequently than once every 4 seconds may be considered as attempting a denial-of-service attack.

        > So if you want to reopen server, be careful the frequence 

If you did not change the variables in `.env`, the server will run on
```sh
localhost:5000
```
with SQLite database
```
├── src/
│   ├── database/
│   │   └── products_data.db        SQLite database
```
> If the `SQLALCHEMY_DATABASE_URI` point to a path with no SQLite database, the program will generate a new SQLite database at the location. 

***
## Default database product value

| ID | Description| Price |Quantity |
| ---------- | -----------| -----------| -----------|
| 0   | apple   | 10 | 100 |
| 1   | orange   | 20 | 200 |
| 2   | watermelon   | 30 | 300 |
| 3   | banana   | 40 | 400 |
| 4   | cherry   | 50 | 500 |
| 5   | figs   | 60 | 600 |
| 6   | lime   | 70 | 700 |
| 7   | pear   | 80 | 800 |
| 8   | plum   | 90 | 900 |
| 9   | olive   | 100 | 1000 |
| 10   | pineapple   | 110 | 1100 |

***

## Unit test details 

Briefly show what inside unit test

-   `test_buy.py` for testing buy operation 
    -   buy success with vaild input
    -   buy fail with vaild input
    -   buy error with invaild input
        -   missing input (id, quantity to buy, credit card number)
        -   invalid input (id, quantity to buy, credit card number)
        -   id not found
-   `test_query.py` for testing query operation
    -   query success with vaild input
    -   query error with invaild input
        -   missing input (id)
        -   invalid input (id)
        -   id not found
-   `test_replenish.py` for testing replenish operation 
    -   replenish success with vaild input
    -   replenish error with invaild input
        -   missing input (id, quantity to replenish)
        -   invalid input (id, quantity to replenish)
        -   id not found
-   `test_server_common.py` for testing server common operation 
    -   check data persistence (after reopen server)
    -   check is the execution ID different from last time
    -   To terminate the subprocess, windows command are required
        ```sh
        taskkill /t /f /pid {pid}
        ```
        so, linux user need to change the above code to following
        ```sh
        os.killpg(int(pid),signal.SIGKILL)
        ```
    > time-b-g.nist.gov: a server more frequently than once every 4 seconds may be considered as attempting a denial-of-service attack.

    > So in the unit test of `test_server_common.py`, reopen server will wait 5 seconds
***

## Usage and JSON format of web service (requests and responses)

-   Query, **[GET]** method
    -   Request
        - Input: product id (zero or a positive integer)
            ```python
            /api/product/query/<id>
            ```
    -   Response
        -   product id found
            ```python
            {"exe_id": exe_id, 'id': id, 'desc': desc, 'price': price, 'quantity': quantity}
            ```
        -   product id is not zero or a positive integer, 400 error
            ```python
            {"exe_id": exe_id, "error": "id is not zero or a positive integer"}
            ```
        -   product id is not found, 404 error
            ```python
            {"exe_id": exe_id, "error": "product ID does not exist"}
            ```
-   Buy, **[PUT]** method
    -   Request
        - Input: product id (zero or a positive integer)
            ```python
            /api/product/buy/<id>
            ```
        -   Data: quantity want to buy (integer), credit-card number (a string of 16 digits)
            ```python
            {"quantity": buy_quantity , "credit_card": credit_card_number}
            ```
    -   Response
        -   buy success
            ```python
            {"exe_id": exe_id, "status": "success", "amount_deducted": credit_card_amount_deducted}
            ```
        -   buy fail
            ```python
            {"exe_id": exe_id, "status": "failure (insufficient quantity in stock)"}
            ```
        -   product id is not zero or a positive integer, 400 error
            ```python
            {"exe_id": exe_id, "error": "id is not zero or a positive integer"}
            ```
        -   product quantity is not zero or a positive integer, 400 error
            ```python
            {"exe_id": exe_id, "error": "quantity is not a positive integer"}
            ```
        -   credit card number is not 16 digits, 400 error
            ```python
            {"exe_id": exe_id, "error": "incorrect credit card format (isn't 16 digits)"}
            ```
        -   product quantity is missing, 400 error
            ```python
            {"exe_id": exe_id, "error": "missing quantity"}
            ```
        -   credit card number is missing, 400 error
            ```python
            {"exe_id": exe_id, "error": "missing credit card number"}
            ```
        -   product quantity and credit card number is missing, 400 error
            ```python
            {"exe_id": exe_id, "error": "missing quantity, missing credit card number"}
            ```
        -   product id is not found, 404 error
            ```python
            {"exe_id": exe_id, "error": "product ID does not exist"}
            ```
-   Replenish, **[PUT]** method
    -   Request
        - Input: product id (zero or a positive integer)
            ```python
            /api/product/replenish/<id>
            ```
        -   Data: quantity want to replenish (integer)
            ```python
            {"quantity": replenish_quantity}
            ```
    -   Response
        -   replenish success
            ```python
            {"exe_id": exe_id, "status": "success", "id": id, "current_quantity": quantity}
            ```
        -   product id is not zero or a positive integer, 400 error
            ```python
            {"exe_id": exe_id, "error": "id is not zero or a positive integer"}
            ```
        -   product quantity is not zero or a positive integer, 400 error
            ```python
            {"exe_id": exe_id, "error": "quantity is not a positive integer"}
            ```
        -   product quantity is missing, 400 error
            ```python
            {"exe_id": exe_id, "error": "missing quantity"}
            ```
        -   product id is not found, 404 error
            ```python
            {"exe_id": exe_id, "error": "product ID does not exist"}
            ```

# Discussion of adopting advanced technologies

I selected two technologies (or techniques) and discuss their adoption in the application. There are `publish–subscribe messaging` and `asynchronous programming`.

## 1. Publish subscribe messaging

When a publisher posts a message, it is visible to all subscribers

-   Background
    -   Users size scaled-up
    -   Only one way users can get the information of products (especially quantity) is by using query web service
        ```python
        /api/product/query/<id>
        ```
    -   For multi product, need multi query requests
-   Problem
    -   If the users wants to buy a product that is out of stock, they can only keep sending query request and know whether the quantity is available now. 
        > Q: What if the users scramble to buy, but isn't buy after query?

        > A: Those users need to take the risk if the price increase (project assume price is fix, however in real case should be changable)
    -   To users, it is not convenient
    -   To server, it is heavy due to huge number of requests
-   How publish–subscribe messaging solve the problem
    -   We can add a tcp server that allow users subscribe a message channel if any update of products
        -   such as: price lower (discount), out of stock, replenish 
-   Implementation
    -   Packages used
        -   [ZeroMQ]
    -   Server side
        1. Make a routes of web service that client can subscribe the message channel
            ```python
            @app.route("/api/product/subscribe/", methods=["GET"])
            def subscribe_prodcuct():
                # code that get tcp-server, example here is tcp://localhost:5556
                # black box here
                return jsonify({"exe_id": exe_id, "tcp-server": "tcp://localhost:5556"})
            ```
        2.  Create a server side program to send message
            ```python
            # File: subscribe_server.py
            import zmq
            import datetime, time
            context = zmq.Context()
            socket = context.socket(zmq.PUB)
            socket.bind("tcp://*:5556")
            while True:
                # code that get update of products
                # black box here
                message = {"time": time, "id": id, "price": price, "quantity": quantity, "news": news}
                socket.send_json(message)
            ```
    -   Client side
        1.  Subscribe the product message update channel by web service. E.g.,
            ```python
            /api/product/subscribe
            ```
            And it will return a status, maybe
            ```python
            {"exe_id": exe_id, "tcp-server": "tcp://localhost:5556"}
            ```
        2.  Create a client side program to receive message
            ```python
            # File: subscribe_client.py
            import zmq
            context = zmq.Context()
            socket = context.socket(zmq.SUB)
            socket.connect("tcp://localhost:5556")
            # set message prefix filter; "" accepts all messages
            socket.setsockopt_string(zmq.SUBSCRIBE, "")
            message = socket.recv_json()
            if message["id"] == id_i_concern:
                # if price now is less than $100 and sufficient stock
                if message["price"] < 100 and message["quantity"] >= quantity_to_buy:
                    # do buy WS operation
                    ws_client(f"http://{SERVER}/api/product/buy/{id_i_concern}","PUT",{"quantity": quantity_to_buy, "credit_card": credit_card})                
            ```
    - Suggested JSON format of the message could be
        -   product turn to out of stock
            ```python
            {"time": time, "id": id, "price": price, "quantity": 0, "news": "out of stock"}
            ```
        -   product replenish
            ```python
            {"time": time, "id": id, "price": price, "quantity": 100, "news": "replenish 100"}
            ```
        -   product discount
            ```python
            {"time": time, "id": id, "price": 50, "quantity": quantity, "news": "70% discount"}
            ```
        > {"`news`": news} is for human readable
    -   Publish/Subscribe Structure
        ```
                               Publisher
                               (server)
                    ┌─────────────┼─────────────┬──────────┬── ...
                 update         update       update       ...
                    │             │             │
               subscriber     subscriber    subscriber
                (client)       (client)     (client)
              (may do WS)    (may do WS)   (may do WS)
        ```

## 2. Asynchronous programming

- Key concept
    -   IO-Bound: the execution time of a operation is determined by the time taken for an input/output operation, but not CPU speed.
    -   Synchronous: wait for a task to finish before moving on to another task
    -   Asynchronous: move on to another task before a task finishes
-   Background
    -   Users size scaled-up
    -   This project mainly do IO operation of database, so this server is IO-Bound
-   Problem
    -   It is hard to handle millions of requests in a server, which mostly do IO operation
    -   To users, the response maybe slow and user experience is bad
    -   To server, an individual thread is IO blocked and cannot be used to handle other work until that IO operation is finished. it is not efficient.
-   How asynchronous programming solve the problem
    -   Our server can handle very high levels of throughput
        -   The thread is released back to the thread pool while waiting for IO
        -   After IO completed, a callback will be executed
-   Implementation
    -   Packages used
        -   [asyncio]
            1.  You need to install Flask with the extra `async` via `pip install "Flask[async]"`.
            2.  Then, you can add the `async` keyword to your functions and use `await`.
    -   Server side

        -   modify the routes to async routes, example below
            ```python
            @app.route("/api/product/query/<id>", methods=["GET"])
            async def query_prodcuct(id):
                data = await async_db_query(...)
                return jsonify(data)
            ```
            > It is new in Flask version 2.0. -- [Flask async Doc]
    -   Client side
        -   Modify the ws_client to async function, following example is query product id (0,1,2)
            ```python
            import json, asyncio
            from urllib.request import Request, urlopen

            SERVER = "localhost:5000"
            JSON_CONTENT_TYPE = "application/json; charset=UTF-8"

            async def ws_client(url, method=None, data=None):
                if not method:
                    method = "PUT" if data else "GET"
                if data:
                    data = json.dumps(data).encode("utf-8")
                headers = {"Content-type": JSON_CONTENT_TYPE} \
                            if data else {}
                req = Request(url=url, data=data, headers=headers, method=method)
                with urlopen(req) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                return result

            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(asyncio.gather(*[
                    ws_client(f"http://{SERVER}/api/product/query/0"), 
                    ws_client(f"http://{SERVER}/api/product/query/1"),
                    ws_client(f"http://{SERVER}/api/product/query/2")
                ]))
            print(*results)
            ```
            -   Expected JSON response
            ```python
            {'desc': 'apple', 'exe_id': 'c00e7f606b0d1532e20388ef4751f2609aa8db077f0d22db98f73fa09106bfc7', 'id': 0, 'price': 10, 'quantity': 100} {'desc': 'orange', 'exe_id': 'c00e7f606b0d1532e20388ef4751f2609aa8db077f0d22db98f73fa09106bfc7', 'id': 1, 'price': 20, 'quantity': 200} {'desc': 'watermelon', 'exe_id': 'c00e7f606b0d1532e20388ef4751f2609aa8db077f0d22db98f73fa09106bfc7', 'id': 2, 'price': 30, 'quantity': 300}
            ```
            > Only show query operation as an example

## License
[Hong Kong Metropolitan University]


[//]: # 

[Hong Kong Metropolitan University]:<https://www.hkmu.edu.hk/>
[ZeroMQ]:<https://zeromq.org/>
[asyncio]:<https://docs.python.org/3/library/asyncio.html>
[Flask async Doc]:<https://flask.palletsprojects.com/en/2.0.x/async-await/>
[Flask]:<https://flask.palletsprojects.com/en/2.0.x/>
[Flask-SQLAlchemy]:<https://flask-sqlalchemy.palletsprojects.com/en/2.x/>
[python-dotenv]:<https://pypi.org/project/python-dotenv/>