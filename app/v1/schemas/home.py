import datetime
from pydantic import BaseModel
from typing import Optional
from fastapi import Form, UploadFile, File


class Home(BaseModel):
    data: str


class TranslateIn(BaseModel):
    text: str

    class Config:
        orm_mode = True


class TranslateOut(BaseModel):
    from_: str
    to: str
    origin: str
    translated: str
    part: list[str, str]

    class Config:
        orm_mode = True


class QrCodeIn(BaseModel):
    text: str

    class Config:
        orm_mode = True


class QrCodeOut(BaseModel):
    qrcode: str

    class Config:
        orm_mode = True


class PolaroidIn(BaseModel):
    # file: str = None
    caption: str

    class Config:
        orm_mode = True