from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/users", tags=["Пользователи"], summary="Получить всех пользователей")
async def get_users():    
    return [{"id": 1, "name": "Matve"}]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)