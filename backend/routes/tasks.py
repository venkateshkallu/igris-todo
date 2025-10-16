from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime
from models import Task, TaskCreate
from database import get_database

router = APIRouter()

@router.get("", response_model=List[Task])
async def get_tasks():
    try:
        db = get_database()
        tasks = []
        async for task in db.tasks.find():
            tasks.append(Task(**task))
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    try:
        db = get_database()
        task_dict = {
            "title": task.title,
            "completed": False,
            "created_at": datetime.utcnow()
        }
        result = await db.tasks.insert_one(task_dict)
        created_task = await db.tasks.find_one({"_id": result.inserted_id})
        return Task(**created_task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )

@router.put("/{task_id}", response_model=Task)
async def toggle_task(task_id: str):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID"
            )
        
        db = get_database()
        task = await db.tasks.find_one({"_id": ObjectId(task_id)})
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        new_completed_status = not task["completed"]
        await db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"completed": new_completed_status}}
        )
        
        updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})
        return Task(**updated_task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID"
            )
        
        db = get_database()
        result = await db.tasks.delete_one({"_id": ObjectId(task_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )