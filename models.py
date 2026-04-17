from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str = None
    disabled: bool = None

class Todo(BaseModel):
    id: int
    user_id: int
    title: str
    description: str = None
    completed: bool = False
    created_at: str
    updated_at: str
