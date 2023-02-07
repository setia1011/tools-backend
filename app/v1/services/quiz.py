from fastapi import Depends
from sqlalchemy.orm import Session, selectinload, lazyload
from app.models import QuesCategory, QuesSession, QuesQuestion, QuesOption, QuesAnswer, Ques


def category_all(db: Session = Depends):
    d_categories = db.query(QuesCategory).all()
    return d_categories


def category_create(
        category: str,
        category_description: str,
        db: Session = Depends):
    d_category = QuesCategory(
        category=category, 
        category_description=category_description
        )
    return d_category


def session_all(db: Session = Depends):
    d_sessions = db.query(QuesSession).all()
    return d_sessions


def session_create(
        session: str,
        session_description: str,
        db: Session = Depends):
    d_session = QuesSession(
        session=session, 
        session_description=session_description
        )
    return d_session


def question_create(category_id: int, question: str, db: Session = Depends):
    d_question = QuesQuestion(category_id=category_id, question=question)
    return d_question


# def question_by_session(session_id: int, db: Session = Depends):
#     d_questions = db.query(QuesQuestion).filter(QuesQuestion.session_id == session_id).all()
#     return d_questions


def option_create(question_id: int, option: str, db: Session = Depends):
    d_option = QuesOption(question_id=question_id, option=option)
    return d_option


def answer_create(question_id: int, answer: str, db: Session = Depends):
    d_answer = QuesAnswer(question_id=question_id, answer=answer)
    return d_answer


def ques_create(session_id: int, question_id: int, db: Session = Depends):
    exists = db.query(Ques).filter(Ques.session_id==session_id).filter(Ques.question_id==question_id).all()
    if exists:
        return "Question already exists"
    else:
        valid = db.query(QuesQuestion).\
        filter(QuesQuestion.id==question_id).\
            options(selectinload(QuesQuestion.ref_option)).\
                options(selectinload(QuesQuestion.ref_answer)).first()

        if (valid.ref_option and valid.ref_answer):
            d_ques = Ques(session_id= session_id, question_id=question_id)
            return d_ques
        else:
            return "Question doesn't valid"


def question_by_session(session_id: int, db: Session = Depends):
    d_questions = db.query(Ques).\
        filter(Ques.session_id==session_id).\
            options(selectinload(Ques.ref_session)).\
            options(selectinload(Ques.ref_question)).all()

    ct = 0
    if d_questions:
        for i in d_questions:
            d_options = db.query(QuesOption).filter(QuesOption.question_id == i.question_id).all()
            d_questions[ct].__setattr__("ref_options", d_options)
            d_category = db.query(QuesCategory).filter(QuesCategory.id == i.ref_question.category_id).first()
            d_questions[ct].__setattr__("ref_category", d_category)
            # include answers, but better hide it for now
            # d_answers = db.query(QuesAnswer).filter(QuesAnswer.question_id==i.question_id).all()
            # d_questions[ct].__setattr__("ref_answers", d_answers)
            ct += 1
    return d_questions


def answer_single(question_id: int, db: Session = Depends):
    d_answers = db.query(QuesAnswer).filter(QuesAnswer.question_id==question_id).all()
    return d_answers