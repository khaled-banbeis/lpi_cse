from sqlalchemy import select
from sqlalchemy.orm import Session

from students import Students
from s_schemas import StudentCreate, StudentUpdate


class StudentRepository:

    def create(self, db: Session, data: StudentCreate):
        student = Students(**data.model_dump())

        db.add(student)
        db.commit()
        db.refresh(student)

        return student

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):
        statement = (
            select(Students)
            .order_by(Students.student_id)
            .offset(skip)
            .limit(limit)
        )

        return db.scalars(statement).all()

    def get_by_id(self, db: Session, student_id: int):
        return db.get(Students, student_id)

    def update(
        self,
        db: Session,
        student: Students,
        data: StudentUpdate
    ):
        for field, value in data.model_dump().items():
            setattr(student, field, value)

        db.commit()
        db.refresh(student)

        return student

    def delete(self, db: Session, student: Students):
        db.delete(student)
        db.commit()
