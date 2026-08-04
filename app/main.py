from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="AI Agent Automation API",
    description="Production-ready AI agent system",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "AI Agent Automation API is running"
    }

