from pydantic import BaseModel, Field, field_validator

class Publisher(BaseModel):
    name: str = Field(min_length=1, max_length=100,
                description="출판사 이름",
                examples=["플레이 출판사"])
    city: str = Field(default="고양",
                description="출판사 소재지",
                examples=["고양"])

class BookCreate(BaseModel):
    title : str = Field(min_length=1, max_length=100,
    description="도서 제목",
    examples=["처음 시작하는 FastAPI"],)
    author: str = Field(min_length=1, max_length=50,
    description="도서 저자",
    examples=["홍길동"],)
    year  : int = Field(ge=1900, le=2026,
    description="출판 연도",
    examples=[2024],)
    tags : list[str] = Field(default_factory=list,
    description="도서 태그 목록",
    examples=["python", "web"],)
    publisher : Publisher | None = Field(default=None, description="출판사 정보")


    @field_validator("title")
    @classmethod
    def strip_title(cls, v:str) -> str:
        v= v.strip()
        if not v :
            raise ValueError("제목은 필수입력입니다.(공백안됨)")
        return v

class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    author: str | None = Field(default=None, min_length=1, max_length=50)
    year  : int | None = Field(default=None, ge=1900, le=2026,
                            description="출판 연도",
                            examples=[2024],)
    tags : list[str] | None = Field(default=None,
                                description="도서 태그 목록",
                                examples=["python", "web"],)
    publisher : Publisher | None = Field(default=None, description="출판사 정보")

class BookResponse(BookCreate):
    id: int
class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature: float
    time: str

class GoogleBooks(BaseModel):
    title: str
    authors: list[str] = Field(default_factory=list)
    published_date: str=""

class ExternalBook(BaseModel):
    title: str
    authors: list[str] = Field(default_factory=list)
    published_date: str = ""