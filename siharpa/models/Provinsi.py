from siharpa import db
from siharpa.SQLalchemyModels.Models import Provinsi  as Pr
class Provinsi:
    #db Column
    kode_provinsi=''
    nama_provinsi=''
    
    def save(self):
        new_provinsi = Pr(kode_provinsi=self.kode_provinsi,nama_provinsi=self.nama_provinsi)
        db.session.add(new_provinsi)
        db.session.commit()
        return new_provinsi

    def all():
        return Pr.query.all()

    def __repr__(self):
        return f"Komoditas('{self.kode_provinsi}','{self.nama_provinsi}')"

    def where(self,kode_provinsi):
        return Pr.query.filter_by(id_provinsi = kode_provinsi).first()

    def update(self,elem):
        elem.kode_provinsi = self.kode_provinsi
        elem.nama_provinsi = self.nama_provinsi
        db.session.commit()

    def delete(self,elem):
        db.session.delete(elem)
        db.session.commit()
    
    def cekKode(self,kode):
        if(Pr.query.filter_by(kode_provinsi = kode).first() == None):
            return True
        else:
            return False