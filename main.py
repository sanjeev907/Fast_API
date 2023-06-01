from fastapi import FastAPI,Depends,status,Response,HTTPException
from database import Base,SessionLocal,engine
import schemas
import models
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def get_data():
    return {'data':"Hi Hi HI"}



def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# post api to data to databse 
@app.post('/post',status_code=status.HTTP_201_CREATED)
def post_user(request:schemas.User,db:Session=Depends(get_db)):
    new = models.User(id = request.id,name=request.name,email=request.email,password=request.password)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


# how to delete the data of the particular id from the database

@app.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session=Depends(get_db)):
    da = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    if not da:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plese enter the vaild Id ")
    return {'done'}






# how to get the data from the database of post api

@app.get('/get_data')
def all(db:Session=Depends(get_db)):
    data= db.query(models.User).all()
    return data

# how to get the data of particular id from the database 

@app.get('/single/{id}')
def show(id,response:Response,db:Session=Depends(get_db)):
    records = db.query(models.User).filter(models.User.id == id).first()
    if not records:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return records


# how to update the data from the database using put method 
@app.put('/update/{id}',status_code=status.HTTP_102_PROCESSING)
def update(id,request:schemas.User,db:Session=Depends(get_db)):
    change = db.query(models.User).filter(models.User.id == id)
    change.update(id = request.id,name=request.name,email=request.email,password=request.password)
    db.commit()
    return  'updated'
