# orm_service

from typing import Optional

from sqlalchemy.orm import Session

from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf import LnDplyFileInf
from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf_repository import LnDplyFileInfRepository


class LnDplyFileInfOrmService:
    def __init__(self, db: Session):
        self.repo = LnDplyFileInfRepository(db)
        self.db = db

    async def add_new_deployment(self, entity: LnDplyFileInf):

        try:
            self.repo.save_entity(entity)
            self.repo.save_history(entity)

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_deployment_info(self, site_id: str, grp_nm: str, ap_nm: str) -> Optional[LnDplyFileInf]:
        return await self.repo.find_by_site_and_ap_name(site_id, grp_nm, ap_nm)
