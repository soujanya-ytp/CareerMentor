from fastapi import Depends, HTTPException, status

from app.db.dependencies import get_current_user, get_db
from app.models.user import User, UserRole


def require_roles(*allowed_roles: UserRole):
    allowed_role_names = {role.value for role in allowed_roles}

    async def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role_name not in allowed_role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return dependency

__all__ = ["get_current_user", "get_db", "require_roles"]
