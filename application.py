from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import crud.rollCRUD as rollCRUD
import crud.storageCRUD as storageCRUD
import models.model as model
import schemas.schema as schema
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


@app.post('/add_new_roll', response_model=schema.RollAdd, description="Enter the weight and length of the roll")
def add_new_roll(roll: schema.RollAdd, db: Session = Depends(get_db)):
    roll = rollCRUD.add_roll_details_to_db(db=db, roll = roll)
    return roll

@app.delete('/delete_roll_by_id_in_storage', description="Specify the address of the roll in the storage")
def delete_roll_by_id_in_storage(roll_id: int, db: Session = Depends(get_db)):
    rollDeleted = storageCRUD.get_roll_by_id_in_storage(db=db, roll_id=roll_id)
    if not rollDeleted:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        rollCRUD.delete_roll_details_by_id_in_storage(db=db, roll_id=roll_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return rollCRUD.get_roll_by_id(db=db,  roll_id = rollDeleted.id)


@app.get('/get_rolls_with_filter', response_model=List[schema.Roll], description="Use this mask for each filter\"id:asc\" and\or \"weight:desc\"")
def get_rolls_with_filter(db: Session = Depends(get_db), sort_by: List[str] = Query(None)):
    try:
        return rollCRUD.get_rolls_with_filter(db=db, sort_by = sort_by)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"incorrect mask: {e}")
    

@app.get('/get_rolls_for_period', description="Enter the date in the dateTime format")
def get_rolls_for_period(startDate: datetime, endDate: datetime, db: Session = Depends(get_db)):
    return rollCRUD.get_rolls_for_period(db=db, startDate = startDate, endDate = endDate)
