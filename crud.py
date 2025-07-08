from database import students_collection
from bson import ObjectId
from models import StudentModel, StudentDBModel
from fastapi import HTTPException

# CREATE
async def create_student(student: StudentModel) -> StudentDBModel:
    result = await students_collection.insert_one(student.dict())
    new_student = await students_collection.find_one({"_id": result.inserted_id})
    return StudentDBModel(**new_student)

# READ ALL
async def get_all_students() -> list[StudentDBModel]:
    students = []
    async for student in students_collection.find():
        students.append(StudentDBModel(**student))
    return students

# READ BY ID
async def get_student_by_id(student_id: str) -> StudentDBModel:
    student = await students_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return StudentDBModel(**student)
    raise HTTPException(status_code=404, detail="Student not found")

# UPDATE
async def update_student(student_id: str, data: StudentModel) -> StudentDBModel:
    result = await students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": data.dict()}
    )
    if result.modified_count:
        updated = await students_collection.find_one({"_id": ObjectId(student_id)})
        return StudentDBModel(**updated)
    raise HTTPException(status_code=404, detail="Student not found")

# DELETE
async def delete_student(student_id: str) -> dict:
    result = await students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count:
        return {"message": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")
