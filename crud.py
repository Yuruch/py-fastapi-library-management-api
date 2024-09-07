from sqlalchemy.future import select
from sqlalchemy.orm import Session

import models
import schemas


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[models.Author]:
    query = select(models.Author).offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    query = select(models.Author).filter(models.Author.name == name)
    result = db.execute(query).scalar_one_or_none()
    return result


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    query = select(models.Author).filter(models.Author.id == author_id)
    result = db.execute(query).scalar_one_or_none()
    return result


def get_books(
    db: Session,
    author_id: int = None,
    skip: int = 0,
    limit: int = 100
) -> list[models.Book]:
    query = select(models.Book).offset(skip).limit(limit)

    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    result = db.execute(query).scalars().all()
    return result


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
