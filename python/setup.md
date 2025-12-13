Is Python 3 Installed? - python3 --version
Execute code in terminal - python3
Python Virtual Environments - A virtual environment is a Python environment that is isolated from
those in other Python environments.

How to Install Dependencies
- Pip is the Python package manager and used to install and update packages.

Run FAST API Application 
=> uvicorn books:app --reload
uvicorn is the webserver
books is the python file that we are refering to and that has app which is fast api app
reload will alllow to reload when code changes
=> fastapi run books.py - another way to run the app in production mode
To run this command we need install => pip install "fastapi[standard]"
=> fastapi dev books.py  - developemnt mode
