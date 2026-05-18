from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secret123@localhost:5432/elearning")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ── Models ──────────────────────────────────────────────

class Course(Base):
    __tablename__ = "courses"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    description = Column(Text)
    instructor  = Column(String(100))
    duration    = Column(String(50))
    level       = Column(String(50))
    emoji       = Column(String(10), default="📚")
    lessons     = relationship("Lesson", back_populates="course", cascade="all, delete")
    quizzes     = relationship("Quiz",   back_populates="course", cascade="all, delete")

class Lesson(Base):
    __tablename__ = "lessons"
    id        = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title     = Column(String(200))
    content   = Column(Text)
    order     = Column(Integer, default=0)
    course    = relationship("Course", back_populates="lessons")

class Quiz(Base):
    __tablename__ = "quizzes"
    id         = Column(Integer, primary_key=True, index=True)
    course_id  = Column(Integer, ForeignKey("courses.id"))
    question   = Column(Text)
    option_a   = Column(String(300))
    option_b   = Column(String(300))
    option_c   = Column(String(300))
    option_d   = Column(String(300))
    answer     = Column(String(1))   # "a" | "b" | "c" | "d"
    course     = relationship("Course", back_populates="quizzes")

class Progress(Base):
    __tablename__ = "progress"
    id        = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    done      = Column(Boolean, default=False)
    updated   = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ── Schemas ─────────────────────────────────────────────

class LessonOut(BaseModel):
    id: int; course_id: int; title: str; content: str; order: int
    class Config: from_attributes = True

class QuizOut(BaseModel):
    id: int; course_id: int; question: str
    option_a: str; option_b: str; option_c: str; option_d: str
    class Config: from_attributes = True

class CourseOut(BaseModel):
    id: int; title: str; description: str; instructor: str
    duration: str; level: str; emoji: str
    class Config: from_attributes = True

class ProgressIn(BaseModel):
    course_id: int; lesson_id: int; done: bool

class AnswerIn(BaseModel):
    quiz_id: int; answer: str

# ── App ─────────────────────────────────────────────────

app = FastAPI(title="EduPortal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Depends

@app.get("/")
def root():
    return {"status": "ok", "message": "EduPortal API is running"}

@app.get("/courses", response_model=list[CourseOut])
def list_courses(db=Depends(get_db)):
    return db.query(Course).all()

@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db=Depends(get_db)):
    c = db.query(Course).filter(Course.id == course_id).first()
    if not c:
        raise HTTPException(404, "Course not found")
    return c

@app.get("/courses/{course_id}/lessons", response_model=list[LessonOut])
def get_lessons(course_id: int, db=Depends(get_db)):
    return db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()

@app.get("/courses/{course_id}/quiz", response_model=list[QuizOut])
def get_quiz(course_id: int, db=Depends(get_db)):
    return db.query(Quiz).filter(Quiz.course_id == course_id).all()

@app.post("/progress")
def save_progress(data: ProgressIn, db=Depends(get_db)):
    row = db.query(Progress).filter(
        Progress.course_id == data.course_id,
        Progress.lesson_id == data.lesson_id
    ).first()
    if row:
        row.done = data.done
        row.updated = datetime.utcnow()
    else:
        row = Progress(**data.model_dump())
        db.add(row)
    db.commit()
    return {"saved": True}

@app.get("/progress/{course_id}")
def get_progress(course_id: int, db=Depends(get_db)):
    rows = db.query(Progress).filter(Progress.course_id == course_id, Progress.done == True).all()
    return {"completed_lessons": [r.lesson_id for r in rows]}

@app.post("/quiz/check")
def check_answer(data: AnswerIn, db=Depends(get_db)):
    q = db.query(Quiz).filter(Quiz.id == data.quiz_id).first()
    if not q:
        raise HTTPException(404, "Quiz not found")
    correct = q.answer.lower() == data.answer.lower()
    return {"correct": correct, "correct_answer": q.answer}