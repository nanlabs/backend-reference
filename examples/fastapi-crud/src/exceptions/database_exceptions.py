from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


class DatabaseExceptions:

    @staticmethod
    def throw_internal_server_error(e: Exception) -> None:
        """Throws a generic DB error"""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Oops, we couldn't connect to the db, please try again later"
        ) from e

    @staticmethod
    def throw_not_found_error(item: str) -> None:
        """Throws a Not Found DB error for an specific item"""
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item} not found"
        )

    @staticmethod
    def throw_db_integrity_error(integrity_error: IntegrityError):
        """Throws SqlAlchemy integrity error detail"""
        detail = ""
        if integrity_error.orig.diag.message_detail:
            detail = integrity_error.orig.diag.message_detail
        else:
            detail = str(integrity_error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        ) from integrity_error
