# Todo App

A simple Todo application built with FastAPI.

## Features

- Create, read, update, and delete todos
- Mark todos as completed
- RESTful API endpoints
- Automatic API documentation

## Running the Application

```bash
# From the fastapi directory
uvicorn todo.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## API Endpoints

- `GET /api/todos/` - Get all todos
- `GET /api/todos/{todo_id}` - Get a specific todo
- `POST /api/todos/` - Create a new todo
- `PUT /api/todos/{todo_id}` - Update a todo
- `DELETE /api/todos/{todo_id}` - Delete a todo

## Example Request

### Create a Todo
```bash
curl -X POST "http://localhost:8000/api/todos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "completed": false
  }'
```

### Get All Todos
```bash
curl "http://localhost:8000/api/todos/"
```

### Update a Todo
```bash
curl -X PUT "http://localhost:8000/api/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

## Project Structure

```
todo/
├── __init__.py      # Package initialization
├── main.py          # FastAPI application entry point
├── models.py        # Pydantic models for request/response
├── routes.py        # API route handlers
├── database.py      # In-memory database (replace with real DB in production)
└── README.md        # This file
```

