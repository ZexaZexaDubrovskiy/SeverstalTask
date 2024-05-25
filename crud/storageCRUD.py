from sqlalchemy.orm import Session
import models.model as model


def get_all_roll_id_in_storage(db: Session):
    return [storage.id for storage in db.query(model.Storage).all()]

def get_roll_by_id_in_storage(db: Session, roll_id: int):
    return db.query(model.Storage).filter(model.Storage.roll_id == roll_id).first()
