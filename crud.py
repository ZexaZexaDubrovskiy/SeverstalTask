#  Date: 2021.03.01
#  Author: dharapx
#  Feel free to use this code
#  -------------------------------------------------------------------------------
#  Here we are having methods for CRUD operation
#  -------------------------------------------------------------------------------

from sqlalchemy.orm import Session
import model
import schema
from datetime import datetime, timedelta
from typing import List
from sqlalchemy import func, or_

def add_roll_details_to_db(db: Session, roll: schema.RollAdd):
    mv_details = model.Rolls(
        weight = roll.weight,
        lenght = roll.lenght
    )

    db.add(mv_details)
    db.commit()
    db.refresh(mv_details)

    rollInStorage = model.Storage(
        roll_id = mv_details.id
    )
    db.add(rollInStorage)
    db.commit()
    db.refresh(rollInStorage)

    

    return model.Rolls(**roll.dict())

def get_rolls(db: Session):
    return db.query(model.Rolls).all()

def get_roll_by_id(db: Session, roll_id: int):
    return db.query(model.Rolls).filter(model.Rolls.id == roll_id).first()



def get_rolls_with_filter(db: Session, sort_by: List[str]):
    
    allRollsIdInStorage = getAllRollIdInStorage(db)

    rolls = db.query(model.Rolls).filter(model.Rolls.id.in_(allRollsIdInStorage))
    
    if sort_by:
        sort_params = [param.split(":") for param in sort_by]
        for field, order in sort_params:
            if order == "desc":
                rolls = rolls.order_by(getattr(model.Rolls, field).desc())
            else:
                rolls = rolls.order_by(getattr(model.Rolls, field))

    return rolls.all()

#2024-05-24 11:30:00
def get_rolls_for_period(db: Session, startDate: datetime, endDate: datetime):

    rolls_query = db.query(model.Rolls).filter(
        model.Rolls.added_at >= startDate,
        or_(model.Rolls.deleted_at <= endDate, model.Rolls.deleted_at == None)
    )
        
    average_weight = rolls_query.with_entities(func.avg(model.Rolls.weight)).scalar()
    average_length = rolls_query.with_entities(func.avg(model.Rolls.lenght)).scalar()
    
    count_deleted = rolls_query.filter(model.Rolls.deleted_at.is_not(None)).count()
    count_added = rolls_query.filter(model.Rolls.added_at).count()

    total_weight = rolls_query.with_entities(func.sum(model.Rolls.weight)).scalar()
    
    max_length = rolls_query.with_entities(func.max(model.Rolls.lenght)).scalar()
    min_length = rolls_query.with_entities(func.min(model.Rolls.lenght)).scalar()

    max_weight = rolls_query.with_entities(func.max(model.Rolls.weight)).scalar()
    min_weight = rolls_query.with_entities(func.min(model.Rolls.weight)).scalar()
    
    time_diffs = [(roll.deleted_at or datetime.now()) - roll.added_at for roll in rolls_query]
    max_time_diff = max(time_diffs, default=timedelta(0))
    min_time_diff = min(time_diffs, default=timedelta(0))



    sum_weight_by_date = rolls_query.with_entities(
        func.sum(model.Rolls.weight).label("sum_weight"),
        func.count(model.Rolls.id).label("count_rolls"),
        func.date(model.Rolls.added_at).label("date_added")
    ).group_by(func.date(model.Rolls.added_at)).all()

    max_weight_day = max(sum_weight_by_date, key=lambda x: x.sum_weight)
    min_weight_day = min(sum_weight_by_date, key=lambda x: x.sum_weight)

    max_rolls_day = max(sum_weight_by_date, key=lambda x: x.count_rolls)
    min_rolls_day = min(sum_weight_by_date, key=lambda x: x.count_rolls)

    return {
        "count_added": count_added,
        "count_deleted": count_deleted,
        "average_weight": average_weight,
        "average_length": average_length,
        "total_weight": total_weight,
        "max_length": max_length,
        "min_length": min_length,
        "max_weight": max_weight,
        "min_weight": min_weight,
        "max_time_diff": f"Дней: {max_time_diff.days}, Секунд: {max_time_diff.seconds}, Миллисекунд: {max_time_diff.microseconds}" , 
        "min_time_diff": f"Дней: {min_time_diff.days}, Секунд: {min_time_diff.seconds}, Миллисекунд: {min_time_diff.microseconds}" ,
        "max_weight_day": max_weight_day.date_added if max_weight_day else None,
        "min_weight_day": min_weight_day.date_added if min_weight_day else None,
        "max_rolls_day": max_rolls_day.date_added if max_rolls_day else None,
        "min_rolls_day": min_rolls_day.date_added if min_rolls_day else None,
    }






def get_roll_by_id_in_storage(db: Session, roll_id: int):
    return db.query(model.Storage).filter(model.Storage.roll_id == roll_id).first()


def delete_roll_details_by_id_in_storage(db: Session, roll_id: int):
    try:
        db.query(model.Storage).filter(model.Storage.id == roll_id).delete()

        
        old_data = db.query(model.Rolls).filter(model.Rolls.id == roll_id).first()
        old_data.deleted_at = datetime.now()

        db.commit()
        
    except Exception as e:
        raise Exception(e)






#storage
def get_info_storage(db: Session):
   return db.query(model.Storage).all()



def getAllRollIdInStorage(db: Session):
    return [storage.id for storage in db.query(model.Storage).all()]
