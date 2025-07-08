from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from pydantic_core.core_schema import ValidationInfo
from pydantic.json_schema import JsonSchemaValue


# Custom ObjectId class compatible with Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info: ValidationInfo):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler) -> JsonSchemaValue:
        return {"type": "string"}

# Input schema
class StudentModel(BaseModel):
    name: str
    age: int
    grade: str

# Output schema with MongoDB ObjectId
class StudentDBModel(StudentModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
