from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    API_V2_STR: str = '/api/v2'
    
    DB_URL: str = 'postgresql+asyncpg://tvyjxoryioyven:ecc0a6540844dd12a252d9342429675f35618aeeadac57c5818e751f2acfe163@ec2-3-210-173-88.compute-1.amazonaws.com:5432/d1f77p8c2b8ppv'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'qS96E1oCfq5gEZH-ngD91NC2qkcl0cffhNTIDGpF4pw'
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
