from siharpa import db
class Dummy(db.Model):
    id_dummy = db.Column(db.Integer,primary_key=True)
    value_dummy = db.Column(db.String(50),nullable=False)   
    def __repr__(self):
        return f"Dummy('{self.id_dummy}','{self.value_dummy}')"