from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, Oauth2, utils
from ..database import get_db

router = APIRouter(
    prefix='/search',
    tags=['Search'],
    # responses={404: {"description": "Not found"}}
)
# get user search_keywords


@router.get('/', )
def get_search_keywords(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    user_query = db.query(models.User_Keyword).filter(
        models.User_Keyword.user_id == current_user.id).first()
    if user_query:
        print(user_query.keywords)
        return user_query.keywords
    else:
        raise HTTPException(
            status_code=404, detail="User has no search keywords")

# add search_keywords


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_search_keyword(request: schemas.keywords, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    user_query = db.query(models.User_Keyword).filter(
        models.User_Keyword.user_id == current_user.id).first()
    if user_query:
        if request.keywords in user_query.keywords.split(','):
            raise HTTPException(
                status_code=400, detail="keyword already exists")
        else:
            new_keywords = user_query.keywords + ',' + request.keywords
            db.query(models.User_Keyword).filter(models.User_Keyword.user_id ==
                                                 current_user.id).update({models.User_Keyword.keywords: new_keywords})
            db.commit()
            db.refresh(user_query)
        return user_query.keywords
    else:
        new_user_keywords = models.User_Keyword(
            user_id=current_user.id, keywords=request.keywords)
        db.add(new_user_keywords)
        db.commit()
        db.refresh(new_user_keywords)
        return new_user_keywords.keywords

# delete search_keywords


@router.patch('/', status_code=status.HTTP_200_OK)
def delete_search_keyword(request: schemas.keywords, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    user_query = db.query(models.User_Keyword).filter(
        models.User_Keyword.user_id == current_user.id).first()
    if user_query:
        list_of_keywords = request.keywords.split(',')
        for keyword in list_of_keywords:
            if keyword in user_query.keywords.split(','):
                new_keywords = utils.remove_word(keyword, user_query.keywords)
                if new_keywords == '':
                    db.query(models.User_Keyword).filter(
                        models.User_Keyword.user_id == current_user.id).delete(synchronize_session=False)
                db.query(models.User_Keyword).filter(
                    models.User_Keyword.user_id == current_user.id).update({models.User_Keyword.keywords: new_keywords})
                db.commit()
                db.refresh(user_query)
            else:
                raise HTTPException(
                    status_code=404, detail="keyword not found")
        return user_query.keywords
    else:
        raise HTTPException(
            status_code=404, detail="user has no search keywords")
