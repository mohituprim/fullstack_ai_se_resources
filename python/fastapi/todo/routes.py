from typing import List
from fastapi import APIRouter, HTTPException, Path
from starlette import status
from todo.models import Todo, TodoCreate, TodoUpdate
from todo.database import todos_db, get_next_id

router = APIRouter()


@router.get("/", response_model=List[Todo], status_code=status.HTTP_200_OK)
async def get_all_todos():
    """Get all todos"""
    return list(todos_db.values())


@router.get("/{todo_id}", response_model=Todo, status_code=status.HTTP_200_OK)
async def get_todo(todo_id: int = Path(..., gt=0, description="Todo ID")):
    """Get a specific todo by ID"""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todos_db[todo_id]


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    """Create a new todo"""
    from datetime import datetime
    
    new_id = get_next_id()
    now = datetime.now()
    
    new_todo = Todo(
        id=new_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=now,
        updated_at=now
    )
    
    todos_db[new_id] = new_todo
    return new_todo


@router.put("/{todo_id}", response_model=Todo, status_code=status.HTTP_200_OK)
async def update_todo(
    todo_id: int = Path(..., gt=0, description="Todo ID"),
    todo_update: TodoUpdate = ...
):
    """Update an existing todo"""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    from datetime import datetime
    existing_todo = todos_db[todo_id]
    
    # Update only provided fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_todo, field, value)
    
    existing_todo.updated_at = datetime.now()
    todos_db[todo_id] = existing_todo
    
    return existing_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(..., gt=0, description="Todo ID")):
    """Delete a todo"""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    del todos_db[todo_id]
    return None

