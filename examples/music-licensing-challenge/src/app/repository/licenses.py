from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from ..models.licenses import LicenseStatus


class LicenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_licenses(self) -> List[LicenseStatus]:
        """
        Retrieves all license status data.
        """
        result = self.db.execute(select(LicenseStatus))
        return result.unique().scalars().all()
