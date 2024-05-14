from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from servprog78.dependencies.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    fake_users_db
)

router = APIRouter()



@router.post("/token", tags=["auth"], response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "roles": user.roles}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/users/me", response_model=User)
# def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

# @app.post("/items/", status_code=201)
# def add_item(item: dict, current_user: User = Depends(check_user_role("writer"))):
#     return {"item": item, "user": current_user.username}

# @app.get("/items/")
# def read_items(current_user: User = Depends(check_user_role("reader"))):
#     return [{"item_id": "1", "owner": current_user.username}]
