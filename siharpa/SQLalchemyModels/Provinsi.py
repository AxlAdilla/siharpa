from siharpa import db
class Provinsi(db.Model):
    id_provinsi = db.Column(db.Integer,primary_key=True)
    kode_provinsi = db.Column(db.String(10),nullable=False)   
    nama_provinsi = db.Column(db.String(50),nullable=False)   
    def __repr__(self):
        return f"Dummy('{self.id_provinsi}','{self.kode_provinsi}','{self.nama_provinsi}')"