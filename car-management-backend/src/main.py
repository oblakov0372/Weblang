import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Project")


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
