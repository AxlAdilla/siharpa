
from siharpa.actions.jaringan.DataPreprocessing import DataPreprocessing
from siharpa.actions.jaringan.Backpropagation import Backpropagation
from datetime import date,timedelta,datetime
import pandas as pd
import re
import io

class PrediksiImport:
    def __init__(self,hari_prediksi,excel,neuron_input,neuron_hidden,epoh,learn_rate,hidden_layer,normalisasi):
        print(hari_prediksi)
        print(excel)
        hari_diprediksi = int(hari_prediksi)              # inisialisasi banyak hari diprediksi
        print('df')
        
        data = pd.read_excel(excel) #(use "r" before the path string to address special character, such as '\'). Don't forget to put the file name at the end of the path + '.xlsx'
        df = pd.DataFrame(data)
        print(df)
        arrOfExcel = df.values.tolist()

        # data = io.BytesIO(excel.read())
        # df = pd.read_excel(data,sheet_name='Laporan Harian')
        # arrOfExcel = df.values.tolist()

        print(arrOfExcel)

        raw_harga_pangan = arrOfExcel[-1][2:]

        if(len(raw_harga_pangan) < 6):
            raise Exception("Data histori terlalu sedikit")
        
        print('raw harga pangan ',raw_harga_pangan)

        harga_pangan=[]

        for harga in raw_harga_pangan:
            print(harga)
            x = re.findall("\d+", str(harga))
            x=''.join(x)
            harga_pangan.append(int(x))
        
        print('harga pangan',harga_pangan)
        
        #self.tanggalPangan = self.data.tanggalPangan[int(neuron_input):]
        
        #banyaknya jumlah data input
        data_input = neuron_input

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
        self.tanggalPangan = arrOfExcel[7][2+int(neuron_input):]
        today = datetime.strptime(self.tanggalPangan[-1],'%d/%m/%Y')
        for index_hari_diprediksi in range(hari_diprediksi):
            #self.tanggalPangan.append(date(today.year,today.month,today.day+index_hari_diprediksi+1).strftime('%d/%m/%Y'))
            self.tanggalPangan.append((today+timedelta(days=index_hari_diprediksi+1)).strftime('%d/%m/%Y'))
        
        print('tanggal pangan',self.tanggalPangan)
        print(jst.data.transform_output_latih.tolist())
        print(jst.data.transform_prediksi.tolist())
        
        #Buat Array Prediksi
        self.hargaPrediksi = []
        self.hargaPrediksi.extend(jst.data.transform_output_latih.tolist())
        self.hargaPrediksi.extend(jst.data.transform_prediksi.tolist())
