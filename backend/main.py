from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.tasks import router as tasks_router
from database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Kiro Tasks API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Kiro Tasks API"}