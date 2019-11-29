
from siharpa.models.Komoditas import Komoditas
from siharpa import db
from siharpa.actions.IndonesiaScrap import IndonesiaScrap
from siharpa.actions.jaringan.DataPreprocessing import DataPreprocessing
from siharpa.actions.jaringan.Backpropagation import Backpropagation
import time

class PrediksiUmum:
    def __init__(self,komoditas,hari_prediksi):
        start_time = time.time()
        hari_diprediksi    = int(hari_prediksi)              # inisialisasi banyak hari diprediksi
        self.komoditas = Komoditas.where(komoditas)
        self.data = IndonesiaScrap(self.komoditas.kode_komoditas,self.komoditas.nama_komoditas,hari_diprediksi)
        #self.hargaPangan = self.data.hargaPangan
        #self.tanggalPangan = self.data.tanggalPangan

        harga_cabe =self.data.hargaPangan
        #rasio banyak data uji dengan data latih range 0-1
        rasio_uji = 0
        #banyaknya jumlah data input
        data_input = 5
        #'maks-min','desimal','z-score-biner','z-score-bipolar','z-score-tanh'
        tipe_normalisasi = 'z-score-bipolar'
        #inisialisasi pembentukan pola data
        cabe = DataPreprocessing(harga_cabe,rasio_uji,data_input,tipe_normalisasi)
        #normalisasi dengan metode maks-min,desimal,z-score,sigmoid-biner,sigmoid-bipolar, atau tanh
        cabe.normalisasi() #'maks-min','desimal','z-score-biner','z-score-bipolar','z-score-tanh'
        #proses membuat pola dataset
        cabe.polaData();
        #proses pola data agar mendapat pola uji dan latih yang terpisah, dan pola input dan target yang terpisah
        cabe.splitPolaData()
        
        #Memasuki Model Jaringan Syaraf Tiruan
        #inisialisasi Parameter

        epoh = 500                          #inisialisasi banyak epoh/perulangan
        learn_rate = 0.25                    #inisialisasi kecepatan pembelajaran
        neuron_input = data_input           #banyak neuron input sesuai masukan pada pola
        jumlah_hidden_layer = 1             #inisialisasi banyak hidden layer
        neuron_hidden = 2                  #inisialisasi banyak neuron pada hidden layer
        is_random_bobot=0                   #inisialisasi apakah jaringan akan menggunakan random bobot dalam inisialisasi atau sudah ditentukan 
        fungsi_aktivasi = tipe_normalisasi  #penggunaan funsi aktivasi sesuai normalisasi data
        
        jst = Backpropagation(epoh,learn_rate,neuron_input,jumlah_hidden_layer,neuron_hidden,is_random_bobot,cabe,fungsi_aktivasi)
        jst.inisialisasiBobot()
        jst.pelatihan()
        jst.uji()
        jst.prediksi(hari_diprediksi)
        jst.data.transformNormalisasi()
        self.hargaPangan = jst.data.transform_target_latih.tolist()
        self.tanggalPangan = self.data.tanggalPangan[5:]
        print(jst.data.transform_output_latih.tolist())
        print(jst.data.transform_prediksi.tolist())
        self.hargaPrediksi = []
        self.hargaPrediksi.extend(jst.data.transform_output_latih.tolist())
        self.hargaPrediksi.extend(jst.data.transform_prediksi.tolist())
        print("--- %s seconds ---" % (time.time() - start_time))
