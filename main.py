from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Todo List API",
    description="A simple todo list API built with FastAPI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

# In-memory storage (for demo purposes)
todos_db = {}
next_id = 1

# Routes
@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to Todo List API", "docs_url": "/docs"}

@app.get("/todos", response_model=List[Todo], tags=["todos"])
def get_todos(completed: Optional[bool] = None):
    """Get all todos, optionally filtered by completion status"""
    todos = list(todos_db.values())
    if completed is not None:
        todos = [todo for todo in todos if todo["completed"] == completed]
    return todos

@app.get("/todos/{todo_id}", response_model=Todo, tags=["todos"])
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

@app.post("/todos", response_model=Todo, status_code=201, tags=["todos"])
def create_todo(todo: TodoCreate):
    """Create a new todo"""
    global next_id
    todo_id = next_id
    next_id += 1
    
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    todos_db[todo_id] = new_todo
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo, tags=["todos"])
def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update a specific todo"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo = todos_db[todo_id]
    if todo_update.title is not None:
        todo["title"] = todo_update.title
    if todo_update.description is not None:
        todo["description"] = todo_update.description
    if todo_update.completed is not None:
        todo["completed"] = todo_update.completed
    todo["updated_at"] = datetime.now()
    
    return todo

@app.patch("/todos/{todo_id}/complete", response_model=Todo, tags=["todos"])
def complete_todo(todo_id: int):
    """Mark a todo as completed"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo = todos_db[todo_id]
    todo["completed"] = True
    todo["updated_at"] = datetime.now()
    return todo

@app.delete("/todos/{todo_id}", status_code=204, tags=["todos"])
def delete_todo(todo_id: int):
    """Delete a specific todo"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]
    return None

@app.delete("/todos", status_code=204, tags=["todos"])
def delete_all_todos():
    """Delete all todos"""
    global next_id
    todos_db.clear()
    next_id = 1
    return None
