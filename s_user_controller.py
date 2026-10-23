from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

import s_schemas
from database import get_db
from s_repository import StudentRepository
from s_service import StudentService


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


def get_student_service() -> StudentService:
    repository = StudentRepository()
    return StudentService(repository)


@router.post(
    "/",
    response_model=s_schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: s_schemas.StudentCreate,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service)
):
    return service.create_student(db, student)


@router.get(
    "/",
    response_model=list[s_schemas.StudentResponse]
)
def get_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service)
):
    return service.get_students(db, skip, limit)


@router.get(
    "/{student_id}",
    response_model=s_schemas.StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service)
):
    return service.get_student_by_id(db, student_id)


@router.put(
    "/{student_id}",
    response_model=s_schemas.StudentResponse
)
def update_student(
    student_id: int,
    student: s_schemas.StudentUpdate,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service)
):
    return service.update_student(db, student_id, student)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service)
):
    service.delete_student(db, student_id)
    return None
