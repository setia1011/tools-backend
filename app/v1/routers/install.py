import pandas as pd
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database import db_session
from app.utils.auth import get_password_hash
from app.core.config import settings
from app.schemas import simple
from app.v1.services import install as service_reference
import os


router = APIRouter()


@router.post("/db-initial/", response_model=simple.Simple, status_code=status.HTTP_200_OK)
async def db_initial(db: Session = Depends(db_session)):
    try:
        # Insert groups
        groups = settings.ROOT_PATH + "/app/data/user_group.csv"
        df_groups = pd.read_csv(groups, usecols=["group_name","group_description"])
        for i, val in df_groups.iterrows():
            user_group = service_reference.create_user_group(
                group_name=val['group_name'],
                group_description=val['group_description'],
                db=db)
            db.add(user_group)
            db.commit()
            db.refresh(user_group)

        # Insert id types
        id_types = settings.ROOT_PATH + "/app/data/user_id_type.csv"
        df_id_types = pd.read_csv(id_types, usecols=["id_type", "id_description"])
        for i, val in df_id_types.iterrows():
            user_id_type = service_reference.create_id_type(
                id_type=val['id_type'],
                id_description=val['id_description'],
                db=db)
            db.add(user_id_type)
            db.commit()
            db.refresh(user_id_type)

        # Insert superuser
        superuser = settings.ROOT_PATH + "/app/data/user.csv"
        df_superuser = pd.read_csv(superuser, usecols=["name","username","password","email","group_id"])
        for i, val in df_superuser.iterrows():
            user_superuser = service_reference.create_superuser(
                name=val['name'],
                username=val['username'],
                password=get_password_hash(str(val['password'])),
                email=val['email'],
                group_id=val['group_id'],
                status="enabled",
                db=db)
            db.add(user_superuser)
            db.commit()
            db.refresh(user_superuser)
    except:
        raise HTTPException(status_code=422, detail='Failed')
    finally:
        db.close()
