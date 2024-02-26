from fastapi import APIRouter, HTTPException, Path
from starlette import status
from modals.todos import Todos
from database import db_dependency
from helper  import user_dependency

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not Authorized')

    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not Authorized')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()