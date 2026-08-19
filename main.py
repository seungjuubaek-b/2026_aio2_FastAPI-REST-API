from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import system, books, external

tags_metadata = [
    {"name": "도서", "description": "도서 등록, 조회, 검색"},
    {"name": "외부 연동", "description": "Google Books와 날씨 API 연동"},
    {"name": "시스템", "description": "서버 상태 확인"},
]

# app = FastAPI()
app = FastAPI(
    title="도서 관리 API~~",
    description="도서를 등록·조회하고 외부 검색으로 정보를 가져오는 API",
    version="1.0.0",
    contact={"name": "홍길동", "email": "hong@example.com"},
    openapi_tag=tags_metadata
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(system.router)
app.include_router(books.router)
app.include_router(external.router)


    # for i, b in enumerate(books):
    #     if b["id"] == book_id:
    #         books.pop(i)
    #         return None
    # raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")

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


# 엔드 포인트
# @app.get("/books/external", response_model=list[GoogleBooks])
# async def search_external_books(keyword:str, limit:int=5):
#     return await fetch_books(keyword, limit)