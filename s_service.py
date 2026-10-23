from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

import students
from s_repository import StudentRepository
from s_schemas import StudentCreate, StudentUpdate


class StudentService:

    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def create_student(
        self,
        db: Session,
        data: StudentCreate
    ):
        try:
            return self.repository.create(db, data)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists or database constraint failed"
            ) from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            ) from exc

    def get_students(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):
        return self.repository.get_all(db, skip, limit)

    def get_student_by_id(
        self,
        db: Session,
        student_id: int
    ):
        student = self.repository.get_by_id(db, student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return student

    def update_student(
        self,
        db: Session,
        student_id: int,
        data: StudentUpdate
    ):
        student = self.repository.get_by_id(db, student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        try:
            return self.repository.update(db, student, data)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists or database constraint failed"
            ) from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            ) from exc

    def delete_student(
        self,
        db: Session,
        student_id: int
    ):
        student = self.repository.get_by_id(db, student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        try:
            self.repository.delete(db, student)
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            ) from exc
