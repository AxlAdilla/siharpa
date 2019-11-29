from siharpa import db
from siharpa.SQLalchemyModels.Models import Prediksi  as Pds
from datetime import date

class Prediksi:
    #db Column
    epoh = ''
    learn_rate = ''
    normalisasi = ''
    neuron_input = ''
    neuron_hidden = ''
    hidden_layer = ''
    
    def save(self):
        prediksi = Pds.query.all()[0]
        prediksi.epoh = self.epoh
        prediksi.learn_rate = self.learn_rate
        prediksi.normalisasi = self.normalisasi
        prediksi.neuron_input = self.neuron_input
        prediksi.neuron_hidden = self.neuron_hidden
        prediksi.hidden_layer = self.hidden_layer
        prediksi.tanggal_update = date.today().strftime('%Y-%m-%d')
        db.session.add(prediksi)
        db.session.commit()
        return prediksi

    def all():
        return Pds.query.all()

    def __repr__(self):
        return f"Prediksi('{self.epoh}','{self.normalisasi}')"