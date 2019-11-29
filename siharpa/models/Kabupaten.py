from siharpa import db
from siharpa.SQLalchemyModels.Models import Kabupaten  as Kab
class Kabupaten:
    #db Column
    kode_kabupaten=''
    kode_provinsi=''
    nama_kabupaten=''
    
    def save(self):
        new_kabupaten = Kab(kode_kabupaten=self.kode_kabupaten,nama_kabupaten=self.nama_kabupaten,kode_provinsi=self.kode_provinsi)
        db.session.add(new_kabupaten)
        db.session.commit()
        return new_kabupaten

    def all():
        return Kab.query.all()

    def __repr__(self):
        return f"Komoditas('{self.kode_kabupaten}','{self.kode_provinsi}','{self.nama_kabupaten}')"

    def where(self,id_kabupaten):
        return Kab.query.filter_by(id_kabupaten = id_kabupaten).first()

    def update(self,elem):
        elem.kode_provinsi = self.kode_provinsi
        elem.nama_kabupaten = self.nama_kabupaten
        elem.kode_kabupaten = self.kode_kabupaten
        db.session.commit()

    def delete(self,elem):
        db.session.delete(elem)
        db.session.commit()
    
    def get_option(self,kode_provinsi):
        return Kab.query.filter_by(kode_provinsi = kode_provinsi).all()

    def cekKode(self,kode):
        if(Kab.query.filter_by(kode_kabupaten = kode).first() == None):
            return True
        else:
            return False