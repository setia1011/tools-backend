import datetime
from pydantic import BaseModel
from typing import Optional
from fastapi import Form, UploadFile, File


class CategoryCreate(BaseModel):
    category: str
    category_description: str

    class Config:
        orm_mode = True


class CategoryDetail(BaseModel):
    id: int
    category: str
    category_description: str

    class Config:
        orm_mode = True


class SessionCreate(BaseModel):
    session: str
    session_description: str

    class Config:
        orm_mode = True


class SessionDetail(BaseModel):
    id: int
    session: str
    session_description: str

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    category_id: int
    question: str

    class Config:
        orm_mode = True


class QuestionBySession(BaseModel):
    session_id: int

    class Config:
        orm_mode = True


class QuestionDetail(BaseModel):
    id: int
    category_id: int
    question: str

    class Config:
        orm_mode = True

class OptionCreate(BaseModel):
    question_id: int
    option: str

    class Config:
        orm_mode = True


class OptionDetail(BaseModel):
    id: int
    question_id: int
    option: str

    class Config:
        orm_mode = True


class AnswerCreate(BaseModel):
    question_id: int
    answer: int

    class Config:
        orm_mode = True


class AnswerDetail(BaseModel):
    id: int
    question_id: int
    answer: int

    class Config:
        orm_mode = True


class Ques(BaseModel):
    session_id: int
    question_id: int

    class Config:
        orm_mode = True


class QuestionBySession(BaseModel):
    session_id: int

    class Config:
        orm_mode = True


class QuestionBySessionDetail(BaseModel):
    session_id: int
    ref_session: SessionDetail
    question_id: int
    question_status: str
    ref_question: QuestionDetail
    ref_category: CategoryDetail
    ref_options: list[OptionDetail]

    class Config:
        orm_mode = True


class AnswerSingle(BaseModel):
    question_id: int

    class Config:
        orm_mode = True

