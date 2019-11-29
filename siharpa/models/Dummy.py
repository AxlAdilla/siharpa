from siharpa import db
from siharpa.SQLalchemyModels.Dummy import Dummy as Dm
class Dummy:
    #db Column
    value_dummy=''
    
    def save():
        new_dummy = Dm(value_dummy=self.value_dummy)
        db.session.add(new_dummy)
        db.session.commit()
        return new_dummy

    def all():
        return Dm.query.all()

    def __repr__(self):
        return f"Dummy('{self.value_dummy}')"

    def where(param):
        return Dm.query.filter_by(value_dummy = param).first()
    
    def update(param,new_val):
        old_dummy = Dm.query.filter_by(value_dummy = param).first()
        old_dummy.value_dummy = new_val
        db.session.commit()
        return old_dummy