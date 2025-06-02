from sqlalchemy import Boolean, Column, DateTime, String, Integer, Text
from sqlalchemy.orm import declarative_base

from schema.request import CreateToDoRequest

Base = declarative_base()

# 엔티티? 같은 것 같음
# declarative_base를 상속받아 데이터베이스 테이블을 나타내도록
class ToDo(Base) :
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    # 오버라이딩
    def __repr__(self) :
        return f"todo(id={self.id}, contents='{self.contents}', is_done={self.is_done})"

    @classmethod
    def create(cls, request: CreateToDoRequest) -> "ToDo":
        return cls(
            contents=request.contents,
            is_done=request.is_done,
        )

    #인스턴스 메서드 -> 유지보수가 편해짐
    def done(self) -> "ToDo":
        self.is_done = True
        return self

    def undone(self) -> "ToDo":
        self.is_done = False
        return self

