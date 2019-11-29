
from siharpa.models.Komoditas import Komoditas
from siharpa import db
from siharpa.actions.PasarScrap import PasarScrap
from siharpa.actions.jaringan.DataPreprocessing import DataPreprocessing
from siharpa.actions.jaringan.Backpropagation import Backpropagation
from datetime import date,timedelta

class PrediksiDaerah:
    def __init__(self,komoditas,hari_prediksi,neuron_input,neuron_hidden,epoh,learn_rate,hidden_layer,normalisasi,kode_provinsi,kode_kabupaten,kode_pasar):
        print([kode_provinsi,kode_kabupaten,kode_pasar])
        hari_diprediksi    = int(hari_prediksi)              # inisialisasi banyak hari diprediksi
        komod_obj = Komoditas()
        self.komoditas = komod_obj.where(komoditas)

        #Hari ini
        today = date.today()

        #End Date
        end_date = today.strftime('%d-%m-%Y')
        
        #Start Date
        start_date = date(today.year,today.month-1,today.day).strftime('%d-%m-%Y')

        print('Start Date ',start_date)
        print('End Date ',end_date)
        
        self.data = PasarScrap(self.komoditas.kode_komoditas,self.komoditas.nama_komoditas,hari_diprediksi,start_date,end_date,kode_provinsi,kode_kabupaten,kode_pasar)
        #self.hargaPangan = self.data.hargaPangan
        #self.tanggalPangan = self.data.tanggalPangan
        
        harga_pangan = self.data.hargaPangan

        #banyaknya jumlah data input
        data_input = neuron_input
        print(harga_pangan)
        #inisialisasi pembentukan pola data
        pangan = DataPreprocessing(harga_pangan,data_input,normalisasi)
        #normalisasi dengan metode maks-min,desimal,z-score,sigmoid-biner,sigmoid-bipolar, atau tanh
        pangan.normalisasi() #'maks-min','desimal','z-score-biner','z-score-bipolar','z-score-tanh'
        #proses membuat pola dataset
        pangan.polaData();
        #proses pola data agar mendapat pola uji dan latih yang terpisah, dan pola input dan target yang terpisah
        pangan.splitPolaData()
        print(len(pangan.data_normalisasi))
        #Memasuki Model Jaringan Syaraf Tiruan
        
        jst = Backpropagation(epoh,learn_rate,neuron_input,hidden_layer,neuron_hidden,0,pangan,normalisasi)

        jst.inisialisasiBobot()
        jst.pelatihan()
        jst.prediksi(hari_diprediksi)
        jst.data.transformNormalisasi()
        
        #Buat Array Harga Pangan
        self.hargaPangan = []
        self.hargaPangan.extend(jst.data.transform_target_latih.tolist())
        #self.hargaPangan.extend(harga_pangan[-hari_diprediksi:])

        self.tanggalPangan = self.data.tanggalPangan[int(neuron_input):]
        
        print(jst.data.transform_output_latih.tolist())
        print(jst.data.transform_prediksi.tolist())
        
        #Buat Array Prediksi
        self.hargaPrediksi = []
        self.hargaPrediksi.extend(jst.data.transform_output_latih.tolist())
        self.hargaPrediksi.extend(jst.data.transform_prediksi.tolist())