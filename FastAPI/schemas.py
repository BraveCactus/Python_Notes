from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI

app = FastAPI()

data = {
    "email": "abcd@mail.ru",
    "bio": "это я",
    "age": 12,
}

data2 = {
    "email": "abcd@mail.ru",
    "bio": "это я",
    "age": 12,
    "gender": "male",
    "birthday": "2022"
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)

    model_config = ConfigDict(extra='forbid') # запрещает дополнительные поля

class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130)

users = []

@app.post("/users")
def add_user(user: UserAgeSchema):
    users.append(user)
    return {"success": True}

@app.get("/users")
def get_users() -> list[UserAgeSchema]:
    return users
    




