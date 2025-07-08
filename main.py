from fastapi import FastAPI
from models import StudentModel, StudentDBModel
from crud import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student
)
from typing import List

app = FastAPI(title="Student CRUD API with MongoDB")

@app.post("/students", response_model=StudentDBModel)
async def create(student: StudentModel):
    return await create_student(student)

@app.get("/students", response_model=List[StudentDBModel])
async def read_all():
    return await get_all_students()

@app.get("/students/{student_id}", response_model=StudentDBModel)
async def read_by_id(student_id: str):
    return await get_student_by_id(student_id)

@app.put("/students/{student_id}", response_model=StudentDBModel)
async def update(student_id: str, student: StudentModel):
    return await update_student(student_id, student)

@app.delete("/students/{student_id}")
async def delete(student_id: str):
    return await delete_student(student_id)
