import imp
from pyexpat import model
from fastapi import FastAPI, responses, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id ==vote.post_id, models.Votes.user_id ==current_user.id)
    found_vote = vote_query.first()
    print(vote_query)
    if vote.dir ==1:
        # UPDATE THE VOTE
        if found_vote:
            # IF VOTE ALREADY EXIST RAISE EXCEPTION
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vote already exit by {current_user.id} on post {vote.post_id}")
        else:
            new_vote = models.Votes(user_id=current_user.id, post_id = vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message": "Successfully New vote added"}
    else:
        # DELETE THE VOTE
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with post ID: {vote.post_id} exist")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote successfully removed"}
