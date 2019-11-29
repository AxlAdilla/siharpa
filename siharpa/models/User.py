from siharpa import db
from siharpa.SQLalchemyModels.Models import User as Usr
class User:
    #db Column
    password=''    

    def all():
        return Usr.query.all()

    def __repr__(self):
        return f"User('{self.password}')"

    def where(self,id_user):
        return Usr.query.filter_by(id_user = id_user).first()
    
    def isThereUser(email,password):
        return Usr.query.filter_by(email = email,password = password).first()

    def update(self,elem):
        elem.password = self.password
        db.session.commit()
