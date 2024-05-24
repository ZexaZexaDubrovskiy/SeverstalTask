from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import crud
import model
import schema
from db_handler import SessionLocal, engine
from datetime import datetime

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Warehouse RESTfull API"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/add_new_roll', response_model=schema.RollAdd)
def add_new_roll(roll: schema.RollAdd, db: Session = Depends(get_db)):
    roll = crud.add_roll_details_to_db(db=db, roll = roll)
    return roll


@app.get('/get_rolls', response_model=List[schema.Roll])
def get_rolls(db: Session = Depends(get_db)):
    rolls = crud.get_rolls(db=db)
    return rolls

@app.delete('/delete_roll_by_id_in_storage')
def delete_roll_by_id_in_storage(roll_id: int, db: Session = Depends(get_db)):
    details = crud.get_roll_by_id_in_storage(db=db, roll_id=roll_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud.delete_roll_details_by_id_in_storage(db=db, roll_id=roll_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return crud.get_roll_by_id(db=db,  roll_id = details.id)



@app.get('/get_rolls_with_filter', response_model=List[schema.Roll])
def get_rolls_with_filter(db: Session = Depends(get_db), sort_by: List[str] = Query(None)):
    return crud.get_rolls_with_filter(db=db, sort_by = sort_by)

@app.get('/get_rolls_for_period')
def get_rolls_for_period(startDate: datetime, endDate: datetime, db: Session = Depends(get_db)):
    return crud.get_rolls_for_period(db=db, startDate = startDate, endDate = endDate)






@app.get('/get_info_storage', response_model=List[schema.Storage])
def get_info_storage(db: Session = Depends(get_db)):
    storage = crud.get_info_storage(db=db)
    return storage
