WHAT IS FASTAPI?
FastAPI is a Python web-framework for building modern APIs
- Fast (Performance)
- Fast (Development)
- https://fastapi.tiangolo.com/

Is Python 3 Installed? - python3 --version
Execute code in terminal - python3
Python Virtual Environments - A virtual environment is a Python environment that is isolated from
those in other Python environments.

How to Install Dependencies
- Pip is the Python package manager and used to install and update packages.
- pip3 list - list all the dependencies installed currently

Setting Up Virtual Environment 

1- I started by creating a brand-new folder / directory called "fastapi"
2- Within our pip we will be checking what dependencies we already have installed. => pip3 list or pip list
3- Python already has an included dependency for virtual environments called venv.
4- Creating a new FastAPI environment as a virtual environment => python3 -m venv fastapienv
5- Activating our virtual environment to install our dependencies in => source fastapienv/bin/activate
6- Deactivate environment => deactivate

Setting Up FastApi 
- install fast api => pip install fastapi
- install uvicorn => pip install "uvicorn[standard]"


Run FAST API Application 
=> uvicorn books:app --reload
uvicorn is the webserver
books is the python file that we are refering to and that has app which is fast api app
reload will alllow to reload when code changes
=> fastapi run books.py - another way to run the app in production mode
To run this command we need install => pip install "fastapi[standard]"
=> fastapi dev books.py  - developemnt mode

What are Path Parameters
• Path Parameters are request parameters that have been attached to the
URL
• Path Parameters are usually defined as a way to find information based
on location
• Think of a computer file system:
• You can identify the specific resources based on the file you are in
  /Users/mohituprim/Documents/python/fastapi/section1 
. Order Matters with Path Parameters
    Example 
        @app.get(“/books/{dynamic_param}”)
        @app.get(“/books/mybook”)  => This won't be called
    Fast api resolves endpoint in chronological order

What are Query Parameters
• Query Parameters are request parameters that have been attached after a “?”
• Query Parameters have name=value pairs
Example:
    127.0.0.1:8000/books/?category=math
    @app.get("/books/{book_author}/") => book_author is path param here 
    async def read_author_category_by_query(book_author: str, category: str):

What is Pydantics
• Python library that is used for data modeling, data parsing and has efficient error handling.
• Pydantics is commonly used as a resource for data validation and how to handle data coming to our FastAPI application.

Pydantic v1 vs Pydantic v2
FastAPI is now compatible with both Pydantic v1 and Pydantic v2.

Based on how new the version of FastAPI you are using, there could be small method name changes.



The three biggest are:

=> .dict() function is now renamed to .model_dump()

=> schema_extra function within a Config class is now renamed to json_schema_extra

=> Optional variables need a =None example: id: Optional[int] = None

Implementing Pydantics
• Create a different request model for data validation
• Field data validation on each variable / element

What are Status Codes?
• An HTTP Status Code is used to help the Client (the user or system submitting data to the server) to understand what happened on the server side application.
• Status Codes are international standards on how a Client/Server should handle the result of a request.
• It allows everyone who sends a request to know if their submission was successful or not.

HTTP Status Code Series Explained

HTTP status codes are categorized into different series based on the first digit of the code. Each series indicates the general class of response from the server:

- **1xx: Informational**
  - These codes indicate that the request has been received and the process is continuing.
  - Examples:
    - `100 Continue`: The client should continue with its request.
    - `101 Switching Protocols`: The server is switching protocols as requested by the client.

- **2xx: Success**
  - These codes indicate that the request was successfully received, understood, and accepted.
  - Examples:
    - `200 OK`: The request succeeded.
    - `201 Created`: The request succeeded and a new resource was created.
    - `204 No Content`: The server successfully processed the request, but is not returning any content.

- **3xx: Redirection**
  - These codes indicate that further action needs to be taken by the client to complete the request.
  - Examples:
    - `301 Moved Permanently`: The resource has been moved permanently to a new URL.
    - `302 Found`: The resource is temporarily located at a different URL.
    - `304 Not Modified`: The resource has not been modified since the last request.

- **4xx: Client Error**
  - These codes indicate that the request contains incorrect syntax or cannot be fulfilled by the server.
  - Examples:
    - `400 Bad Request`: The server could not understand the request due to invalid syntax.
    - `401 Unauthorized`: Authentication is required and has failed or has not yet been provided.
    - `403 Forbidden`: The client does not have access rights to the content.
    - `404 Not Found`: The server cannot find the requested resource.

- **5xx: Server Error**
  - These codes indicate that the server failed to fulfill a valid request.
  - Examples:
    - `500 Internal Server Error`: The server encountered an unexpected condition.
    - `502 Bad Gateway`: The server received an invalid response from the upstream server.
    - `503 Service Unavailable`: The server is currently unable to handle the request.

Knowing these status code series helps in understanding server responses and troubleshooting communication between client and server.

Starlette is a lightweight ASGI (Asynchronous Server Gateway Interface) framework for building async web services in Python.
Key Points:
FastAPI's Foundation: FastAPI is built on top of Starlette. FastAPI adds features like automatic API documentation, data validation with Pydantic, and dependency injection, while Starlette provides the core async web framework.
What it provides:
- Async request/response handling
- WebSocket support
- HTTP/2 support
Background tasks
- HTTP status codes (which you're using in your code)
Middleware support
    In your code: You're importing status from Starlette to use HTTP status codes like:
    status.HTTP_200_OK
    status.HTTP_201_CREATED
    status.HTTP_204_NO_CONTENT
    These are constants that represent standard HTTP status codes, making your code more readable and maintainable than using raw numbers like 200, 201, 204.