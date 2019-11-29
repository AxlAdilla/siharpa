from siharpa import db
from siharpa.SQLalchemyModels.Models import Pasar as Pas
class Pasar:
    #db Column
    kode_pasar=''
    nama_pasar=''
    kode_kabupaten=''
    
    def save(self):
        new_pasar = Pas(kode_pasar=self.kode_pasar,nama_pasar=self.nama_pasar,kode_kabupaten=self.kode_kabupaten)
        db.session.add(new_pasar)
        db.session.commit()
        return new_pasar

    def all():
        return Pas.query.all()

    def __repr__(self):
        return f"Komoditas('{self.kode_pasar}','{self.kode_kabupaten}','{self.nama_pasar}')"

    def where(self,id_pasar):
        return Pas.query.filter_by(id_pasar = id_pasar).first()

    def update(self,elem):
        elem.kode_kabupaten = self.kode_kabupaten
        elem.nama_pasar = self.nama_pasar
        elem.kode_pasar = self.kode_pasar
        db.session.commit()

    def delete(self,elem):
        db.session.delete(elem)
        db.session.commit()

    def get_option(self,kode_kabupaten):
        return Pas.query.filter_by(kode_kabupaten = kode_kabupaten).all()

    def cekKode(self,kode):
        if(Pas.query.filter_by(kode_pasar = kode).first() == None):
            return True
        else:
            return False