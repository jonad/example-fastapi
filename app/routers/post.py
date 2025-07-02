from .. import models, schemas, utils
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, oauth2
from typing import Optional

router = APIRouter(prefix="/posts", tags=["Posts"])  # create a router for posts


@router.get(
    "/", response_model=List[schemas.PostOut]
)  # decorator to define a GET endpoint at /posts
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    """
    Get all posts from the database, including vote counts.
    """
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True,
        )
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    # Pydantic's `from_orm` or `model_validate` (in V2) correctly converts SQLAlchemy
    # model instances to Pydantic models without including internal state attributes
    # like `_sa_instance_state`. We pass the ORM object directly.
    posts = [
        schemas.PostOut(post=schemas.PostResponse.model_validate(post), votes=votes)
        for post, votes in results
    ]
    print(posts)
    return posts


# create a new post
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)  # decorator to define a POST endpoint at /posts
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create a new post in the database.
    """
    print(f"Current user ID: {current_user.id}")  # debug print to check current user
    post.owner_id = current_user.id  # set the owner_id to the current user's id
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get individual post by id
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(
    id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    """
    Get a post by its ID.
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    """
    Delete a post by its ID.
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Update a post by its ID.
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action",
        )
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    updated = post_query.first()
    return updated
