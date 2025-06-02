from typing import List

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import ToDo

class ToDoRepository :
    def __init__(self, session: Session =  Depends(get_db)):
        self.session = session

    def get_todos(self) -> List[ToDo]:
        return list(self.scalars(select(ToDo)))

    def get_todo_by_todo_id(self, todo_id: int) -> ToDo | None:
        return self.scalar(select(ToDo).where(ToDo.id == todo_id))

    def create_todo(self, todo: ToDo) -> ToDo:
        self.add(instance=todo)
        self.commit() # db save
        self.refresh(instance=todo) # db read -> todo_id
        return todo

    def update_todo(self, todo: ToDo) -> ToDo:
        self.add(instance=todo)
        self.commit() # db save
        self.refresh(instance=todo)
        return todo

    def delete_todo(self, todo_id) -> None:
        self.execute(delete(ToDo).where(ToDo.id == todo_id))
        self.commit()