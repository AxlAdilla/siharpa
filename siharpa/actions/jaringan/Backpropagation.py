#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:28:13 2019

@author: axl
"""
import numpy
import random
from siharpa.actions.jaringan.FungsiAktivasi import FungsiAktivasi
class Backpropagation:
    def __init__(self,epoh,learn_rate,neuron_input,jumlah_hidden_layer,neuron_hidden,is_random_bobot,data,fungsi_aktivasi):
        self.epoh = int(epoh)
        self.learn_rate = float(learn_rate)
        self.neuron_input = int(neuron_input)
        self.jumlah_hidden_layer = int(jumlah_hidden_layer)
        self.neuron_hidden = int(neuron_hidden)
        self.is_random_bobot = is_random_bobot
        self.data = data
        self.fungsi_aktivasi = self.fungsiAktivasiDipakai(fungsi_aktivasi)
        self.bobot_hidden = []
        self.bias_hidden = []
        self.bobot_output = []
        self.bias_output = 0
        self.bobot_input = []
        self.bias_input = []
        self.data_neuron_hidden = [] 
        self.error_output=0
        self.error_hidden=[]
        self.delta_bobot_hidden = []
        self.delta_bias_hidden = []
        self.delta_bobot_output = []
        self.delta_bias_output = 0
        self.delta_bobot_input = []
        self.delta_bias_input = []
    
    #menyesuaikan fungsi aktivasi sesuai normalisasi yang dipakai
    def fungsiAktivasiDipakai(self,fungsi_aktivasi):
        if(fungsi_aktivasi == 'maks-min'):
            return 'sigmoid-biner'
        elif(fungsi_aktivasi == 'desimal'):
            return 'sigmoid-biner'
        elif(fungsi_aktivasi == 'z-score-biner'):
            return 'sigmoid-biner'
        elif(fungsi_aktivasi == 'z-score-bipolar'):
            return 'sigmoid-bipolar'
        elif(fungsi_aktivasi == 'z-score-tanh'):
            return 'tanh'
        
    def inisialisasiBobot(self):
        #membuat matriks bobot input
        self.bobot_input = numpy.zeros((self.neuron_input,self.neuron_hidden))
        
        #membuat matriks bias input
        self.bias_input = numpy.zeros((self.neuron_hidden))
        
        #membuat matriks bobot hidden
        self.bobot_hidden = numpy.zeros((self.jumlah_hidden_layer-1,self.neuron_hidden,self.neuron_hidden))
        
        #membuat matriks bias hidden
        self.bias_hidden = numpy.zeros((self.jumlah_hidden_layer-1,self.neuron_hidden))
        
        #membuat matriks bobot output
        self.bobot_output = numpy.zeros((self.neuron_hidden))
        
        #membuat matriks bias output
        self.bias_output = 0
        
        #membuat matriks neuron hidden
        self.data_neuron_hidden  = numpy.zeros((self.jumlah_hidden_layer,self.neuron_hidden))
        
        #membuat matriks error output
        self.error_output=0
        
        #membuat matriks error hidden
        self.error_hidden = numpy.zeros((self.jumlah_hidden_layer,self.neuron_hidden))
        
        #membuat matriks delta bobot hidden
        self.delta_bobot_hidden=numpy.zeros((numpy.shape(self.bobot_hidden)))
        
        #membuat matriks delta bias hidden
        self.delta_bias_hidden=numpy.zeros((numpy.shape(self.bias_hidden)))
        
        #membuat matriks delta bobot input
        self.delta_bobot_input=numpy.zeros((numpy.shape(self.bobot_input)))
        
        #membuat matriks delta bias input
        self.delta_bias_input=numpy.zeros((numpy.shape(self.bias_input)))
        
        #membuat matriks delta bobot output
        self.delta_bobot_output=numpy.zeros((numpy.shape(self.bobot_output)))

        if(self.is_random_bobot == 1):        
            #inisialisasi nilai bobot input
            for neuron_input in range(self.neuron_input):
                for neuron_hidden in range(self.neuron_hidden):
                    self.bobot_input[neuron_input][neuron_hidden]=round(random.random(),2)+0.1        
            #inisialisasi nilai bias input
            for neuron_hidden in range(self.neuron_hidden):
                self.bias_input[neuron_hidden]=round(random.random(),2)+0.1
            #inisialisasi nilai bobot hidden
            for hid_layer in range(self.jumlah_hidden_layer-1):
                for neuron_hidden_1 in range(self.neuron_hidden):
                    for neuron_hidden_2 in range(self.neuron_hidden):
                        self.bobot_hidden[hid_layer][neuron_hidden_1][neuron_hidden_2]=round(random.random(),2)+0.1        
            #inisialisasi nilai bias hidden
            for hid_layer in range(self.jumlah_hidden_layer-1):
                for neuron_hidden in range(self.neuron_hidden):
                    self.bias_hidden[hid_layer][neuron_hidden]=round(random.random(),2)+0.1
            #inisialisasi nilai bobot output
            for neuron_hidden in range(self.neuron_hidden):
                self.bobot_output[neuron_hidden]=round(random.random(),2)+0.1       
            #inisialisasi nilai bias output
            self.bias_output=round(random.random(),2)+0.1        
        else:
            random_nilai = 0.25
            #inisialisasi nilai bobot input
            for neuron_input in range(self.neuron_input):
                for neuron_hidden in range(self.neuron_hidden):
                    self.bobot_input[neuron_input][neuron_hidden]=random_nilai        
                    random_nilai+=0.1
            #inisialisasi nilai bias input
            random_nilai = 0.25
            for neuron_hidden in range(self.neuron_hidden):
                self.bias_input[neuron_hidden]=random_nilai
                random_nilai+=0.1
            #inisialisasi nilai bobot hidden
            random_nilai = 0.25
            for hid_layer in range(self.jumlah_hidden_layer-1):
                for neuron_hidden_1 in range(self.neuron_hidden):
                    for neuron_hidden_2 in range(self.neuron_hidden):
                        self.bobot_hidden[hid_layer][neuron_hidden_1][neuron_hidden_2]=random_nilai        
                        random_nilai+=0.1
            #inisialisasi nilai bias hidden
            random_nilai = 0.25
            for hid_layer in range(self.jumlah_hidden_layer-1):
                for neuron_hidden in range(self.neuron_hidden):
                    self.bias_hidden[hid_layer][neuron_hidden]=random_nilai
                    random_nilai+=0.1
            #inisialisasi nilai bobot output
            random_nilai = 0.25
            for neuron_hidden in range(self.neuron_hidden):
                self.bobot_output[neuron_hidden]=random_nilai
                random_nilai+=0.1
            #inisialisasi nilai bias output
            random_nilai = 0.25
            self.bias_output=round(random_nilai,2)   
                        
        return self.bobot_hidden,self.bias_hidden,self.bobot_output,self.bias_output,self.bobot_input,self.bias_input
        
    def pelatihan(self):
        for epoh in range(self.epoh):
            #print('======= Epoh Ke ',epoh,' =====')
                #index_latih=0
            for index_latih in range(len(self.data.data_input_latih)):
                #feedforward 
                self.feedforward(self.data.data_input_latih[index_latih],index_latih,'latih')
                #backpropagation
                self.backpropagation(self.data.data_target_latih[index_latih],index_latih)
                #update bobot
                self.updateBobot()
    
    # def uji(self):
    #     for index_uji in range(len(self.data.data_input_uji)):
    #         #feedforward 
    #         self.feedforward(self.data.data_input_uji[index_uji],index_uji,'uji')

    def prediksi(self,number_prediksi):
        for index_prediksi in range(number_prediksi):
            data_prediksi = numpy.array(self.data.data_normalisasi[-self.neuron_input:])
            #feedforward 
            self.feedforward(data_prediksi,index_prediksi,'prediksi')
        
        
    def feedforward(self,data_input,index_latih,kondisi):
        #Neuron Input -> Hidden Layer
        for index_neuron_hidden in range(self.neuron_hidden):
            #bobot ke neuron misal [v11 v21 v31 ... vn1]
            bobot = self.bobot_input[:,index_neuron_hidden]
            
            #bias ke neuron misal v01
            bias = self.bias_input[index_neuron_hidden]
            hasil = self.hitungNeuron(data_input,bobot,bias,self.neuron_input)
            self.data_neuron_hidden[0][index_neuron_hidden]=hasil
            
        #Hidden Layer -> Hidden Layer
        for i in range(self.jumlah_hidden_layer-1):
            for index_neuron_hidden in range(self.neuron_hidden):
                #bobot ke neuron hidden sebelahnya  misal [w11 w21 w31 ... wn1]
                bobot = self.bobot_hidden[i,:,index_neuron_hidden]
                
                #bias ke neuron misal w01 w02
                bias = self.bias_hidden[i,index_neuron_hidden]                
                hasil = self.hitungNeuron(self.data_neuron_hidden[i],bobot,bias,self.neuron_hidden)                
                self.data_neuron_hidden[i+1][index_neuron_hidden]=hasil
    
        #Hidden Layer -> Output Layer        
        #bobot dr neuron hidden layer ke output layer misal [v11 v21 v31 ... vn1]
        bobot = self.bobot_output[:]
        
        #bias ke neuron misal v01
        bias = self.bias_output
        hasil = self.hitungNeuron(self.data_neuron_hidden[self.jumlah_hidden_layer-1],bobot,bias,self.neuron_hidden)
        if(kondisi == 'latih'):
            self.data.data_output_latih[index_latih]=hasil
        elif(kondisi == 'prediksi'):
            self.data.normalisasi_prediksi.append(hasil) 
            self.data.data_normalisasi.append(hasil)
        # else:
        #     self.data.data_output_uji[index_latih]=hasil
            
    def hitungNeuron(self,data_input,bobot,bias,index):
        hasil = 0
        for index_input in range(index):
            hasil += data_input[index_input]*bobot[index_input]
        hasil += bias
        
        #memilih fungsi aktivasi
        if(self.fungsi_aktivasi == 'sigmoid-biner'):
            hasil = FungsiAktivasi.sigmoid_biner(hasil)
        elif(self.fungsi_aktivasi == 'sigmoid-bipolar'):
            hasil = FungsiAktivasi.sigmoid_bipolar(hasil)
        elif(self.fungsi_aktivasi == 'tanh'):
            hasil = FungsiAktivasi.tanh(hasil)
        return hasil
    
    def backpropagation(self,data_target_output,index_latih):
        #hitung error output
        #self.error_output=(data_target_output-self.data.data_output_latih[index_latih])*self.data.data_output_latih[index_latih]*(1-self.data.data_output_latih[index_latih])
        if(self.fungsi_aktivasi == 'sigmoid-biner'):
            turunan = FungsiAktivasi.turunan_sigmoid_biner(self.data.data_output_latih[index_latih])
        elif(self.fungsi_aktivasi == 'sigmoid-bipolar'):
            turunan = FungsiAktivasi.turunan_sigmoid_bipolar(self.data.data_output_latih[index_latih])
        elif(self.fungsi_aktivasi == 'tanh'):
            turunan = FungsiAktivasi.turunan_tanh(self.data.data_output_latih[index_latih])
            
        self.error_output=(data_target_output-self.data.data_output_latih[index_latih])*turunan
        #hitung delta bobot output
        for index_output in range(len(self.delta_bobot_output)):
            self.delta_bobot_output[index_output] = self.learn_rate*self.error_output*self.data_neuron_hidden[self.jumlah_hidden_layer-1][index_output]
        
        #hitung delta bias output                
        self.delta_bias_output=self.learn_rate*self.error_output        
        
        #hitung error hidden
        for index_hidden_layer in reversed(range(self.jumlah_hidden_layer)):
            
            for index_neuron_hidden in range(self.neuron_hidden):
                #menghubungkan hidden layer dengan output layer
                if(index_hidden_layer == self.jumlah_hidden_layer-1):
                    #self.error_hidden[index_hidden_layer][index_neuron_hidden]=self.error_output*self.bobot_output[index_neuron_hidden]*self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden]*(1-self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
                    if(self.fungsi_aktivasi == 'sigmoid-biner'):
                        turunan = FungsiAktivasi.turunan_sigmoid_biner(self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
                    elif(self.fungsi_aktivasi == 'tanh'):
                        turunan = FungsiAktivasi.turunan_tanh(self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
                    elif(self.fungsi_aktivasi == 'sigmoid-bipolar'):
                        turunan = FungsiAktivasi.turunan_sigmoid_bipolar(self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
                    
            
                    self.error_hidden[index_hidden_layer][index_neuron_hidden]=self.error_output*self.bobot_output[index_neuron_hidden]*turunan
        
                #menghubungkan hidden layer dengan hidden layer
                else:
                    #self.error_output*self.bobot_output[index_neuron_hidden]
                    sigma_error_dikali_bobot=0
                    for index_neuron_hidden_2 in range(self.neuron_hidden):
                        err_hidden = self.error_hidden[index_hidden_layer+1][index_neuron_hidden_2]
                        bobot_hidden = self.bobot_hidden[index_hidden_layer][index_neuron_hidden][index_neuron_hidden_2]
                        sigma_error_dikali_bobot += err_hidden*bobot_hidden
                    #self.error_hidden[index_hidden_layer][index_neuron_hidden]=sigma_error_dikali_bobot*self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden]*(1-self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
                    if(self.fungsi_aktivasi == 'sigmoid-biner'):
                        turunan = FungsiAktivasi.turunan_sigmoid_biner(self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
                    elif(self.fungsi_aktivasi == 'sigmoid-bipolar'):
                        turunan = FungsiAktivasi.turunan_sigmoid_bipolar(self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
                    elif(self.fungsi_aktivasi == 'tanh'):
                        turunan = FungsiAktivasi.turunan_tanh(self.data_neuron_hidden[index_hidden_layer][index_neuron_hidden])
            
                    self.error_hidden[index_hidden_layer][index_neuron_hidden]=sigma_error_dikali_bobot*turunan


                if(index_hidden_layer == 0):
                    #hitung delta bobot dan bias input
                    for index_neuron_input in range(self.neuron_input):
                        self.delta_bobot_input[index_neuron_input][index_neuron_hidden]=self.learn_rate*self.error_hidden[0][index_neuron_hidden]*self.data.data_input_latih[index_latih][index_neuron_input]
                    
                    self.delta_bias_input[index_neuron_hidden]=self.learn_rate*self.error_hidden[0][index_neuron_hidden]
                else:
                    #hitung delta bobot dan bias hidden
                    for index_neuron_hidden_2 in range(self.neuron_hidden):
                        #hitung delta bobot hidden
                        self.delta_bobot_hidden[index_hidden_layer-1][index_neuron_hidden_2][index_neuron_hidden] = self.learn_rate*self.error_hidden[index_hidden_layer][index_neuron_hidden]*self.data_neuron_hidden[index_hidden_layer-1][index_neuron_hidden_2]
                    #hitung delta bias hidden                
                    self.delta_bias_hidden[index_hidden_layer-1][index_neuron_hidden]=self.learn_rate*self.error_hidden[index_hidden_layer][index_neuron_hidden]
        
    def updateBobot(self):
        self.bobot_input = self.bobot_input+self.delta_bobot_input
        self.bias_input = self.bias_input+self.delta_bias_input
        self.bobot_hidden = self.bobot_hidden+self.delta_bobot_hidden
        self.bias_hidden = self.bias_hidden+self.delta_bias_hidden
        self.bobot_output = self.bobot_output+self.delta_bobot_output
        self.bias_output = self.bias_output+self.delta_bias_output
    
    def calcAccuracy(self,data_output,data_target):
        hasil = 0;
        banyak_data =len(data_output)
        for index in range(banyak_data):
            hasil += (data_output[index]-data_target[index])**2
        return hasil/banyak_data
        
    def meanAbsolutePrecentageError(self,target,predict):
        absolute_value = 0
        for index in range(len(target)):
            absolute_value = abs((target[index]-predict[index])/target[index])
        return absolute_value/len(target)*100
    