from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    age: int | None = Field(default=None, ge=0)


class StudentUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    age: int | None = Field(default=None, ge=0)


class StudentResponse(BaseModel):
    student_id: int
    name: str
    email: str
    department: str | None = None
    age: int | None = None

    model_config = ConfigDict(from_attributes=True)
