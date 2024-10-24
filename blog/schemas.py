from typing import List,Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        from_attributes = True

class NodeBase(BaseModel):
    pwm: str
    volt: str
    ampe: str
    health: str
    log: str
    street_name: str
    uid: Optional[str] = None

class Node(NodeBase):
    
    class Config():
        from_attributes = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]
    nodes: List[Node]
    class Config():
        from_attributes = True

class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class ShowNode(BaseModel):
    pwm: str
    volt: str
    ampe: str
    health: str
    log: str
    street_name: str
    class Config():
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None