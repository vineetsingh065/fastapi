from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest( BaseModel ):
    id: Optional[int] = Field( description="Optional", default=None )
    title: str = Field( min_length=3 )
    author: str = Field( min_length=3 )
    description: str = Field( max_length=100 )
    rating: int = Field( gt=0, le=5 )
    published_date: int = Field( gt=1000, lt=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "test_title",
                "author": "test_author",
                "description": "test description",
                "rating": 5,
                "published_date": "year of publish date"
            }
        }
    }


BOOKS = [
    Book( id=1, title='Title One', author='Author One', description='science', rating=4, published_date=2012 ),
    Book( id=2, title='Title two', author='Author two', description='math', rating=4, published_date=2013 ),
    Book( id=3, title='Title three', author='Author three', description='english', rating=4, published_date=2014 ),
    Book( id=4, title='Title four', author='Author four', description='computer science', rating=4,
          published_date=2015 ),
    Book( id=5, title='Title five', author='Author five', description='social', rating=4, published_date=2016 )
]


@app.get( '/books', status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS


@app.post( '/create_book', status_code=status.HTTP_200_OK )
async def create_book(book_request: BookRequest):
    new_book = Book( **book_request.dict() )
    BOOKS.append( find_book_id( new_book ) )
    return BOOKS


@app.get( "/books/{book_id}", status_code=status.HTTP_200_OK )
async def read_book(book_id: int = Path(gt=0)):
    book = [book for book in BOOKS if book.id == book_id]
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get( "/books/", status_code=status.HTTP_200_OK )
async def get_book_by_rating(rating: int = Query(gt=0, le=5)):
    books_to_returned = [book for book in BOOKS if book.rating == rating]
    return books_to_returned


@app.get( "/books/publish/", status_code=status.HTTP_200_OK )
async def get_book_by_publishdate(year: int):
    books_to_returned = [book for book in BOOKS if book.published_date == year]
    print(books_to_returned)
    return books_to_returned


@app.put( "/books/update_book" , status_code=status.HTTP_201_CREATED)
async def update_book(book: BookRequest):
    update = False
    for i in range( len( BOOKS ) ):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            update = True
    if not update:
        raise HTTPException(status_code=404, detail="Item not found")
    return BOOKS


@app.delete( '/books/{book_id}', status_code=status.HTTP_200_OK )
async def delete_book(book_id: int = Path(gt=0)):
    for i in range( len( BOOKS ) ):
        if BOOKS[i].id == book_id:
            BOOKS.pop( i )
            break
    return BOOKS


def find_book_id(book: Book):
    book.id = 1 if len( BOOKS ) == 0 else BOOKS[-1].id + 1
    return book
