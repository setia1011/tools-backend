import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Core
from app.utils.auth import create_access_token
from app.database import db_session
from app.v1.schemas import user as schema_user
from app.utils import auth
from app.utils import email
from app.utils.useful import dayday, acticode, current_datetime

# Services
from app.v1.services import user as service_user

# Models
from app.models.user import User

router = APIRouter()


@router.post("/register/", response_model=schema_user.ResponseData, status_code=status.HTTP_201_CREATED)
async def register(
        user: schema_user.UserRegister,
        db: Session = Depends(db_session)):
    try:
        # Check username duplicate
        dt_new = service_user.find_user_by_username(username=user.username, db=db)
        if dt_new:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Silahkan menggunakan username yang lain"
            )

        # Check if email exists
        dt_email = service_user.find_email(email=user.email, db=db)
        if dt_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Silahkan menggunakan email yang lain",
            )

        # Create user
        dt_user = service_user.create_user(
            name=user.name,
            username=user.username,
            password=auth.get_password_hash(user.password),
            email=user.email,
            db=db
        )
        db.add(dt_user)
        db.commit()
        db.refresh(dt_user)

        acticodex = acticode(6)
        expired = dayday(3)
        dt_activation = service_user.create_activation(
            user_id=dt_user.id,
            acticode=acticodex,
            expired=expired
        )
        db.add(dt_activation)
        if dt_activation:
            # Send acticode to register email
            email.send(
                email=user.email,
                name=user.name,
                code=acticodex,
                expired=expired
            )
        db.commit()
        data = {"data": "Kode aktivasi telah dikirimkan ke email, segera lakukan aktivasi"}
        return data
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.post("/activation/", response_model=schema_user.ResponseData, status_code=status.HTTP_200_OK)
async def activation(schema: schema_user.Activation, db: Session = Depends(db_session)):
    dt_activation = service_user.find_acticode(acticode=schema.acticode, db=db)
    if not dt_activation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode aktivasi tidak valid",
        )

    if dt_activation.status == 'activated':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode aktivasi sudah pernah diaktifkan sebelumnya",
        )

    dt_user = service_user.find_user_by_id(id=dt_activation.user_id, db=db)
    if not dt_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode aktivasi tidak valid",
        )

    a = dt_activation.expired
    b = datetime.datetime.strptime(current_datetime(), "%Y-%d-%m %H:%M:%S")
    if a >= b:
        try:
            dt_activation.status = 'activated'
            db.add(dt_activation)
            db.commit()
            db.refresh(dt_activation)

            dt_user.status = 'enabled'
            db.add(dt_user)
            db.commit()
            db.refresh(dt_user)
            response = "Aktivasi berhasil, silahkan login"
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    else:
        response = "Kode aktivasi sudah tidak berlaku"
    data = {"data": response}
    return data


@router.post("/login/", response_model=schema_user.UserLoginOut, status_code=status.HTTP_200_OK)
async def login(user: schema_user.UserLogin, db: Session = Depends(db_session)):
    try:
        dt_user = service_user.find_user_by_username(username=user.username, db=db)
        # ensure the user exist in the system
        if not dt_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data user tidak ditemukan di dalam sistem",
            )
        # verify password
        if not auth.verify_password(user.password, dt_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password yang digunakan tidak sesuai",
            )
        data = {
            "access_token": create_access_token(sub=dt_user.username),
            "token_type": "bearer"
        }
        return data
    except Exception:
        raise
    finally:
        db.close()


@router.put("/update/", response_model=schema_user.UserUpdate, dependencies=[Depends(auth.default)], status_code=status.HTTP_201_CREATED)
async def update(
        user: schema_user.UserUpdate,
        current_user: User = Depends(auth.get_current_active_user),
        db: Session = Depends(db_session)):
    try:
        if current_user.email != user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not authenticated")
        if not current_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data tidak valid")
            
        current_user.editor = current_user.id
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(current_user, key, value)
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.patch("/password/", response_model=schema_user.ResponseData, dependencies=[Depends(auth.default)], status_code=status.HTTP_201_CREATED)
async def password(
        schema: schema_user.UpdatePassword,
        current_user: User = Depends(auth.get_current_active_user),
        db: Session = Depends(db_session)):
    try:
        dt_user = service_user.find_user_by_username(username=current_user.username, db=db)
        # ensure the user exist in the system
        if not dt_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data user tidak ditemukan di dalam sistem",
            )
        # verify new password with confirm new password
        if schema.old_password == schema.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password lama tidak boleh sama dengan password baru",
            )
        # verify new password with confirm new password
        if schema.new_password != schema.confirm_new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password baru tidak sama dengan password konfirmasi",
            )
        # verify old password
        if not auth.verify_password(schema.old_password, dt_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password lama tidak sesuai",
            )
        # update with the new password
        dt_user.password = auth.get_password_hash(schema.new_password)
        db.add(dt_user)
        db.commit()
        db.refresh(dt_user)
        data = {"data": "Berhasil melakukan update password"}
        return data
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.get("/detail/", response_model=schema_user.UserDetailOut, response_model_by_alias=True, dependencies=[Depends(auth.default)], status_code=status.HTTP_200_OK)
async def detail(current_user: User = Depends(auth.get_current_active_user), db: Session = Depends(db_session)):
    try:
        dt_user = service_user.find_user_by_username_3(username=current_user.username, db=db)
        return dt_user
    except Exception:
        raise
    finally:
        db.close()


