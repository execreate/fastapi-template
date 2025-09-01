import secrets

from core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

basicSecurity = HTTPBasic()


def basic_http_credentials(
    credentials: HTTPBasicCredentials = Depends(basicSecurity),
) -> str:
    correct_username = secrets.compare_digest(
        credentials.username, settings.DOCS_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.DOCS_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
