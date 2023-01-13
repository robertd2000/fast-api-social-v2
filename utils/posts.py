from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models.post import Post, Like, Dislike


def get_posts_from_db(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Post).limit(limit=limit).offset(offset=offset).all()
    for post in posts:
        likes = len(list(post.likes))
        dislikes = len(list(post.dislikes))
        post.likes_count = likes
        post.dislikes_count = dislikes
    return posts


def get_post_from_db(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Пост с id {post_id} не найден!')
    post = post.first()
    likes = len(list(post.likes))
    dislikes = len(list(post.dislikes))
    post.likes_count = likes
    post.dislikes_count = dislikes
    return post


def check_like_in_db(post_id: int, author_id: int, db: Session = Depends(get_db)) -> bool:
    like_db = db.query(Like).filter(Like.post_id == post_id, Like.user_id == author_id)
    if like_db.first():
        like_db.delete()
        db.commit()
        return True
    return False


def check_dislike_in_db(post_id: int, author_id: int, db: Session = Depends(get_db)) -> bool:
    dislike_db = db.query(Dislike).filter(Dislike.post_id == post_id, Dislike.user_id == author_id)
    if dislike_db.first():
        dislike_db.delete()
        db.commit()
        return True
    return False


def check_post_author(post_id: int, user_id: int, db: Session = Depends(get_db)) -> bool:
    post = db.query(Post).filter(Post.id == post_id).first()
    return post.author_id == user_id


def get_post_from_db_and_check_author(post_id: int, user_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Пост с id {post_id} не найден!')
    if not post.first().author_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Вы не являетесь автором поста!!')
    return post
