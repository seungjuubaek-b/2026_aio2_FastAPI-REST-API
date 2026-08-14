from pydantic import BaseModel, Field, field_validator

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
class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature: float
    time: str

class GoogleBooks(BaseModel):
    title: str
    author: list[str] = Field(default_factory=list)
    Published_date: str=""