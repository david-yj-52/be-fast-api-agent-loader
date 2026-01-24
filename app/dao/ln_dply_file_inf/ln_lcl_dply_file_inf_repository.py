# orm repository

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf import LnDplyFileInf, LhDplyFileInf


class LnDplyFileInfRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    def save_entity(self, entity: LnDplyFileInf) -> LnDplyFileInf:
        self.db.add(entity)
        return entity

    def save_history(self, entity: LnDplyFileInf) -> LhDplyFileInf:
        history_entity = entity.to_history()
        self.db.add(history_entity)
        return history_entity

    async def find_by_site_and_ap_name(self, site_id: str, grp_nm: str, ap_nm: str) -> Optional[LnDplyFileInf]:
        stmt = select(LnDplyFileInf).where(
            LnDplyFileInf.site_id == site_id,
            LnDplyFileInf.ap_grp_nm == grp_nm,
            LnDplyFileInf.ap_nm == ap_nm
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def find_by_id(self, obj_id: str) -> Optional[LnDplyFileInf]:
        stmt = select(LnDplyFileInf).where(LnDplyFileInf.obj_id == obj_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
