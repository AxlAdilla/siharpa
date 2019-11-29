from siharpa import db
from siharpa.SQLalchemyModels.Models import Komoditas as Km
class Komoditas:
    #db Column
    kode_komoditas=''
    nama_komoditas=''
    
    def save(self):
        new_komoditas = Km(kode_komoditas=self.kode_komoditas,nama_komoditas=self.nama_komoditas)
        db.session.add(new_komoditas)
        db.session.commit()
        return new_komoditas

    def all():
        return Km.query.all()

    def __repr__(self):
        return f"Komoditas('{self.kode_komoditas}','{self.nama_komoditas}')"

    def where(self,id_komoditas):
        return Km.query.filter_by(id_komoditas = id_komoditas).first()

    def update(self,elem):
        elem.kode_komoditas = self.kode_komoditas
        elem.nama_komoditas = self.nama_komoditas
        db.session.commit()

    def delete(self,elem):
        db.session.delete(elem)
        db.session.commit()
    
    def cekKode(self,kode):
        if(Km.query.filter_by(kode_komoditas = kode).first() == None):
            return True
        else:
            return False