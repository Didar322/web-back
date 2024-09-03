
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    
users_db = {
    "admin": User(username="admin", password="admin"),
    "user": User(username="user", password="password"),
}