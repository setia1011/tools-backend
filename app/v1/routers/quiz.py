from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import db_session
from app.v1.schemas import error as schema_error
from app.v1.schemas import quiz as quiz_schema
from app.v1.services import quiz as serv_quiz

router = APIRouter()


@router.get('/category',
    responses={200: {'model': list[quiz_schema.CategoryDetail]}, 422: {'model': schema_error.HTTPError}}, 
    description='Get all categories')
async def category(db: Session = Depends(db_session)):
    try:
        d_categories = serv_quiz.category_all(db=db)
        return d_categories
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.post('/category', 
    responses={200: {'model': quiz_schema.CategoryDetail}, 422: {'model': schema_error.HTTPError}},
    description='Create category')
async def category(t: quiz_schema.CategoryCreate, db: Session = Depends(db_session)):
    try:
        d_category = serv_quiz.category_create(
            category=t.category, 
            category_description=t.category_description, 
            db=db
        )
        db.add(d_category)
        db.commit()
        db.refresh(d_category)
        return d_category
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.get('/session', 
    responses={200: {'model': list[quiz_schema.SessionDetail]}, 422: {'model': schema_error.HTTPError}}, 
    description='Get all seasons')
async def session(db: Session = Depends(db_session)):
    try:
        d_sessions = serv_quiz.session_all(db=db)
        return d_sessions
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.post('/session', 
    responses={200: {'model': quiz_schema.SessionDetail}, 422: {'model': schema_error.HTTPError}},
    description='Create season')
async def session(t: quiz_schema.SessionCreate, db: Session = Depends(db_session)):
    try:
        d_session = serv_quiz.session_create(
            session=t.session, 
            session_description=t.session_description, 
            db=db
        )
        db.add(d_session)
        db.commit()
        db.refresh(d_session)
        return d_session
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.post('/question', 
    responses={200: {'model': quiz_schema.QuestionDetail}, 422: {'model': schema_error.HTTPError}},
    description='Create question')
async def question(t: quiz_schema.QuestionCreate, db: Session = Depends(db_session)):
    try:
        q_question = serv_quiz.question_create(
            category_id=t.category_id,
            question=t.question, 
            db=db
        )
        db.add(q_question)
        db.commit()
        db.refresh(q_question)
        return q_question
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.post('/option', 
    responses={200: {'model': quiz_schema.OptionDetail}, 422: {'model': schema_error.HTTPError}},
    description='Create option')
async def option(t: quiz_schema.OptionCreate, db: Session = Depends(db_session)):
    try:
        q_option = serv_quiz.option_create(
            question_id=t.question_id,
            option=t.option,
            db=db
        )
        db.add(q_option)
        db.commit()
        db.refresh(q_option)
        return q_option
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.post('/answer',  
    responses={200: {'model': quiz_schema.AnswerDetail}, 422: {'model': schema_error.HTTPError}},
    description='Create answer')
async def answer(t: quiz_schema.AnswerCreate, db: Session = Depends(db_session)):
    try:
        q_answer = serv_quiz.answer_create(
            question_id=t.question_id,
            answer=t.answer,
            db=db
        )
        db.add(q_answer)
        db.commit()
        db.refresh(q_answer)
        return q_answer
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.post('/ques', 
    responses={200: {"model": quiz_schema.Ques}, 422: {"model": schema_error.HTTPError}}, 
    description='Assign question to session')
async def ques(t: quiz_schema.Ques, db: Session = Depends(db_session)):
    try:
        q_ques = serv_quiz.ques_create(
            session_id=t.session_id,
            question_id=t.question_id,
            db=db
        )
        db.add(q_ques)
        db.commit()
        db.refresh(q_ques)
        return q_ques
    except Exception:
        raise HTTPException(status_code=422, detail=q_ques)
    finally:
        db.close()


@router.post('/question-by-session', 
    responses={200: {"model": list[quiz_schema.QuestionBySessionDetail]}, 422: {"model": schema_error.HTTPError}}, 
    description='Get questions by session')
async def question_by_session(t: quiz_schema.QuestionBySession, db: Session = Depends(db_session)):
    try:
        q_questions = serv_quiz.question_by_session(
            session_id=t.session_id,
            db=db
        )
        return q_questions
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()


@router.post('/answer-single', 
    responses={200: {"model": list[quiz_schema.AnswerDetail]}, 422: {"model": schema_error.HTTPError}}, 
    description='Check an answer of a question')
async def answer_single(t: quiz_schema.AnswerSingle, db: Session = Depends(db_session)):
    try:
        d_answers = serv_quiz.answer_single(question_id=t.question_id, db=db)
        return d_answers
    except Exception:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()