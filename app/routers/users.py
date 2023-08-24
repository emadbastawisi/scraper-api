from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from .. import models, schemas, utils, Oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {"description": "Not found"}}

)

# get all users


@router.get('/', response_model=list[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    # Retrieve all users from the database
    users = db.execute(select(models.User)).scalars().all()

    # Return the list of users as the API response
    return users

# create a new user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.email == '' or user.username == '' or user.password == '':
        raise HTTPException(status_code=400, detail="Invalid data")
    existing_user = db.query(models.User).filter(
        or_(
            models.User.email == user.email,
            models.User.username == user.username
        )
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = utils.hash(user.password)

    new_user = models.User(
        email=user.email,
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# check username avilability
@router.get('/username/{username}')
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return True
    return False

# check email is already registerd or not


@router.get('/email/{email}')
def get_user(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == email).first()
    if not user:
        return True
    return False

# method to get currnet user


@router.get('/current', response_model=schemas.UserOut)
def get_current_user(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    print(current_user)
    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()
    if not user:
        return False
    return user

# update user password


@router.patch('/password', status_code=status.HTTP_200_OK)
def update_password(password: schemas.Password, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authorized")
    user.password = utils.hash(password.password)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)
