from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2  # import the necessary models and schemas

router = APIRouter(prefix="/auth", tags=["Authentication"])  # create a router for authentication


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return a token.
    """
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user or not utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Here you would typically generate a JWT token and return it
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
