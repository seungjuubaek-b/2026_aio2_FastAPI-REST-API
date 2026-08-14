from fastapi import FastAPI, status, HTTPException
from schemas import WeatherResponse, BookResponse, BookCreate, GoogleBooks
from external_api import fetch_weather, fetch_books
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

books = [
 {"id": 1, "title": "파이썬 입문", "author": "김철수", "year": 2021, "tags": [], "publisher": None},
 {"id": 2, "title": "FastAPI 실전", "author": "이영희", "year": 2023, "tags": [], "publisher": None},
 {"id": 3, "title": "파이썬 웹개발", "author": "김철수", "year": 2022, "tags": [], "publisher": None},
 {"id": 4, "title": "데이터 분석 기초", "author": "박민수", "year": 2020, "tags": [], "publisher": None},
 {"id": 5, "title": "FastAPI로 배우는 백엔드", "author": "이영희", "year": 2024, "tags": [], "publisher": None},
 ]

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

# @app.get("/weather/raw")
# async def weather_raw():
#     async with httpx.AsyncClient(timeout=5.0) as client:
#         response = await client.get(
#             "https://api.open-meteo.com/v1/forecast",
#             params={
#                 "latitude": 36.8,
#                 "longitude": 127.1,
#                 "current": "temperature_2m",
#             },
#         )
#         return response.json()

@app.get("/weather", response_model=WeatherResponse)
async def weather(latitude: float= 36.8, longitude: float=127.1):
    return await fetch_weather(latitude, longitude)

# 엔드 포인트
@app.get("/books/external", response_model=list[GoogleBooks])
async def search_external_books(keyword:str, limit:int=5):
    return await fetch_books(keyword, limit)

# 항상 마지막
@app.get("/books/{book_id}", response_model=BookResponse) # /books까지는 요청, {book_id} f스트링때 썼던 거
def read_book(book_id : int) :
    for book in books:
        if book_id == book['id'] :
            return book
    # return {"error": "Not found"}
    raise HTTPException(status_code=404, detail="우리 책이 아니에요")