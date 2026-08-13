from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  
from pydantic import BaseModel, Field
from fastapi import status
from fastapi import HTTPException
from pydantic import field_validator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

books = [
 {"id": 1, "title": "파이썬 입문", "author": "김철수", "year": 2021, "tags": [], "publisher": None},
 {"id": 2, "title": "FastAPI 실전", "author": "이영희", "year": 2023, "tags": [], "publisher": None},
 {"id": 3, "title": "파이썬 웹개발", "author": "김철수", "year": 2022, "tags": [], "publisher": None},
 {"id": 4, "title": "데이터 분석 기초", "author": "박민수", "year": 2020, "tags": [], "publisher": None},
 {"id": 5, "title": "FastAPI로 배우는 백엔드", "author": "이영희", "year": 2024, "tags": [], "publisher": None},
 ]

class Publisher(BaseModel):
    name: str
    city: str = "서울"

class BookCreate(BaseModel):
    title : str = Field(min_length=1, max_length=100) # 속성(attribute), 필드
    author : str = Field(min_length=1, max_length=50)
    year : int = Field(ge=1900, le=2026)
    tag: list[str] = Field(default_factory=list)
    publisher : Publisher | None = None

    @field_validator("title")
    @classmethod
    def strip_title(cls, v:str) -> str:
        v= v.strip()
        if not v :
            raise ValueError("제목은 필수입력입니다.(공백안됨)")
        return v

class BookResponse(BookCreate):
    id: int

@app.get("/")
def read_root() :
    return {"message" : "Hello World!"}

@app.get("/health")
def health() :
    return {"status" : "healthy"}

@app.get("/info")
def info() :
    return {"name" : "도서 관리 API", "version" : "0.1.0"}

# 도서의 목록을 제공하는 엔드 포인트
@app.get("/books", response_model=list[BookResponse])
def list_books() :
    return books

@app.get("/books/search") # 데코레이터 를 통해서 FastAPI와 대화
def search_books(keyword: str = ""):
    if not keyword:
        return books
    return [b for b in books if keyword in b["title"]]

@app.get("/books/filter")
def filter_books(keyword: str = "", sort: str = ""):
    result = books
    #for book in books:
    # 리스트 컴프리헨션 - for + if > 리스트
    result = [b for b in result if b['author'] == keyword]

    if sort == "year" :
        result = sorted(result, key=lambda b: b["year"])
    return result
# 스웨거에서 keyword 에 김철수 앞에 빈칸 넣어서 오류남

@app.get("/books/page")
def page_books(skip:int=0, limit:int=2) :
    return books[skip: skip+limit]

@app.get("/books/{book_id}", response_model=BookResponse) # /books까지는 요청, {book_id} f스트링때 썼던 거
def read_book(book_id : int) :
    for book in books:
        if book_id == book['id'] :
            return book
    # return {"error": "Not found"}
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")

@app.post("/books", response_model=BookResponse, 
          status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(status_code=409, detail="기존에 등록된 도서입니다.")
    new_id = max([b["id"] for b in books], default=0) + 1
    # new_book = {"id" : new_id, 
    #             "title" : book.title, 
    #             "author" : book.author, 
    #             "year" : book.year}
    new_book = {"id" : new_id, **book.model_dump()}
    books.append(new_book)
    return new_book
# 테스트 시나리오
# 1. 새로운 책 등록
# 2. 북 목록을 조회
# 3. 등록한 책을 검색

# result = books 다 담고

# 요청을 하면 응답으로 상태코드가 나와야 한다.
# 404 내가 요청하는 uri 자체가 없어요 하면 나오는 오류