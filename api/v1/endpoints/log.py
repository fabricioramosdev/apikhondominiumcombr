from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from models.usuario_model import UsuarioModel

from models.log_model import LogModel
from schemas.log_schema import LogSchema

from core.deps import get_session, get_current_user

router = APIRouter()

# GET Logs
@router.get('/', response_model=List[LogSchema])
async def get_logs(db: AsyncSession = Depends(get_session), user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(LogModel)
        result = await session.execute(query)
        logs: List[LogModel] = result.scalars().unique().all()

        return logs