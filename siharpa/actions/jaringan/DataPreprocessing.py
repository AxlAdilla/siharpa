#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:33:18 2019

@author: axl
"""
from statistics import stdev,mean
import math
import numpy
from siharpa.actions.jaringan.FungsiAktivasi import FungsiAktivasi
class DataPreprocessing:
    def __init__(self,data,data_input,tipe_normalisasi):
        self.data = data
        self.data_normalisasi = []
        self.tipe_normalisasi = tipe_normalisasi
        self.data_input = int(data_input)
        self.pola_data =[]
        self.normalisasi_prediksi = []
        self.data_input_latih = []
        # self.data_input_uji = []
        self.data_output_latih = []
        # self.data_output_uji = []
        self.data_target_latih = []
        # self.data_target_uji = []
        self.transform_output_latih = []
        # self.transform_output_uji = []
        self.transform_target_latih = []
        # self.transform_target_uji = []
        self.max_data = max(self.data)
        self.min_data = min(self.data)
        self.pembagi = 10**(int((math.log10(self.max_data))) + 1)
        self.stdev_data = stdev(self.data)
        self.mean_data = mean(self.data)
        pass
    
    def z_score_calculate(self,data):
        return (data-self.mean_data)/self.stdev_data
    
    def normalisasi(self):
        normalisasi = []
        if self.tipe_normalisasi == 'maks-min':
            for data in self.data:
                #operasi maks-min
                normalisasi_data = ((data - self.min_data)/(self.max_data-self.min_data))*0.8+0.1
                normalisasi.append(normalisasi_data)            
        elif self.tipe_normalisasi == 'desimal':
            for data in self.data:
                #operasi desimal
                normalisasi_data = data/self.pembagi
                normalisasi.append(normalisasi_data)
        elif self.tipe_normalisasi == 'z-score-biner':
            for data in self.data:
                #operasi z-score
                normalisasi_data = self.z_score_calculate(data)
                #operasi sigmoid-biner
                normalisasi_data = FungsiAktivasi.sigmoid_biner(normalisasi_data)
                normalisasi.append(normalisasi_data)
        elif self.tipe_normalisasi == 'z-score-bipolar':
            for data in self.data:
                #operasi z-score
                normalisasi_data = self.z_score_calculate(data)
                #operasi sigmoid-biner
                normalisasi_data = FungsiAktivasi.sigmoid_bipolar(normalisasi_data)
                normalisasi.append(normalisasi_data)
        elif self.tipe_normalisasi == 'z-score-tanh':
            for data in self.data:
                #operasi z-score
                normalisasi_data = self.z_score_calculate(data)
                #operasi sigmoid-biner
                normalisasi_data = FungsiAktivasi.tanh(normalisasi_data)
                normalisasi.append(normalisasi_data)         
        self.data_normalisasi = normalisasi
        return self.data_normalisasi

    def normalisasiKonfigurasi(self,hari_diprediksi):
        normalisasi = []
        if self.tipe_normalisasi == 'maks-min':
            for data in self.data:
                #operasi maks-min
                normalisasi_data = ((data - self.min_data)/(self.max_data-self.min_data))*0.8+0.1
                normalisasi.append(normalisasi_data)            
        elif self.tipe_normalisasi == 'desimal':
            for data in self.data:
                #operasi desimal
                normalisasi_data = data/self.pembagi
                normalisasi.append(normalisasi_data)
        elif self.tipe_normalisasi == 'z-score-biner':
            for data in self.data:
                #operasi z-score
                normalisasi_data = self.z_score_calculate(data)
                #operasi sigmoid-biner
                normalisasi_data = FungsiAktivasi.sigmoid_biner(normalisasi_data)
                normalisasi.append(normalisasi_data)
        elif self.tipe_normalisasi == 'z-score-bipolar':
            for data in self.data:
                #operasi z-score
                normalisasi_data = self.z_score_calculate(data)
                #operasi sigmoid-biner
                normalisasi_data = FungsiAktivasi.sigmoid_bipolar(normalisasi_data)
                normalisasi.append(normalisasi_data)
        elif self.tipe_normalisasi == 'z-score-tanh':
            for data in self.data:
                #operasi z-score
                normalisasi_data = self.z_score_calculate(data)
                #operasi sigmoid-biner
                normalisasi_data = FungsiAktivasi.tanh(normalisasi_data)
                normalisasi.append(normalisasi_data)         
        self.data_normalisasi = normalisasi[:-hari_diprediksi]
        return self.data_normalisasi
    
    def polaData(self):
        panjang_array = len(self.data_normalisasi) #menghitung banyaknya data masukan
        banyak_baris = panjang_array-self.data_input #berdasarkan perhitungan banyaknya baris pada pola latih adalah panjang array - data input yang diinginkan
        banyak_kolom = self.data_input+1 #banyaknya data input yang dinginkan ditambahkan dengan kolom target
        #membuat dataset sesuai input yang diinginkan
        print('Banyak Baris ',banyak_baris)
        print('Banyak Panjang Normalisasi ',self.data_normalisasi)
        self.pola_data = numpy.zeros((banyak_baris,banyak_kolom))
        for baris in range(banyak_baris):
            #print(baris)
            for kolom in range(banyak_kolom):
                #pola data berantai
                self.pola_data[baris][kolom]=self.data_normalisasi[kolom+baris]
        return self.pola_data
    
    def splitPolaData(self):
        jumlah_baris,jumlah_kolom = numpy.shape(self.pola_data)
        
        self.data_input_latih = self.pola_data[:,:self.data_input]  
        self.data_target_latih = self.pola_data[:,-1]
        self.data_output_latih = numpy.zeros((numpy.shape(self.data_target_latih)))
        
        return self.data_input_latih,self.data_target_latih,self.data_output_latih
        
    def transformNormalisasi(self):
        #inisialisasi transform kembali ke data awal
        self.transform_output_latih = numpy.zeros((numpy.shape(self.data_output_latih)))
        self.transform_target_latih = numpy.zeros((numpy.shape(self.data_target_latih)))
        self.transform_prediksi = numpy.zeros((numpy.shape(self.normalisasi_prediksi)))
        
        if self.tipe_normalisasi == 'maks-min':
            #transform output latih
            for index in range(len(self.data_output_latih)):
                self.transform_output_latih[index]=((self.data_output_latih[index]-0.1)/0.8)*(self.max_data-self.min_data)+self.min_data
            #transform target latih
            for index in range(len(self.data_target_latih)):
                self.transform_target_latih[index]=((self.data_target_latih[index]-0.1)/0.8)*(self.max_data-self.min_data)+self.min_data
            #transform Prediksi
            for index in range(len(self.normalisasi_prediksi)):
                self.transform_prediksi[index]=((self.transform_prediksi[index]-0.1)/0.8)*(self.max_data-self.min_data)+self.min_data   
            
    
        elif self.tipe_normalisasi == 'desimal':
            #transform output latih
            for index in range(len(self.data_output_latih)):
                self.transform_output_latih[index]=self.data_output_latih[index]*self.pembagi
            #transform target latih
            for index in range(len(self.data_target_latih)):
                self.transform_target_latih[index]=self.data_target_latih[index]*self.pembagi
            #transform Prediksi
            for index in range(len(self.normalisasi_prediksi)):
                self.transform_prediksi[index]=self.transform_prediksi[index]*self.pembagi
            
        elif self.tipe_normalisasi == 'z-score-biner':
            #transform output latih
            for index in range(len(self.data_output_latih)):
                hasil=FungsiAktivasi.transform_sigmoid_biner(self.data_output_latih[index])
                self.transform_output_latih[index]=hasil*self.stdev_data+self.mean_data
            #transform target latih
            for index in range(len(self.data_target_latih)):
                hasil=FungsiAktivasi.transform_sigmoid_biner(self.data_target_latih[index])
                self.transform_target_latih[index]=hasil*self.stdev_data+self.mean_data
            #transform Prediksi
            for index in range(len(self.normalisasi_prediksi)):
                hasil=FungsiAktivasi.transform_sigmoid_biner(self.normalisasi_prediksi[index])
                self.transform_prediksi[index]=hasil*self.stdev_data+self.mean_data

        elif self.tipe_normalisasi == 'z-score-bipolar':
            #transform output latih
            for index in range(len(self.data_output_latih)):
                hasil=FungsiAktivasi.transform_sigmoid_bipolar(self.data_output_latih[index])
                self.transform_output_latih[index]=hasil*self.stdev_data+self.mean_data
            #transform target latih
            for index in range(len(self.data_target_latih)):
                hasil=FungsiAktivasi.transform_sigmoid_bipolar(self.data_target_latih[index])
                self.transform_target_latih[index]=hasil*self.stdev_data+self.mean_data
            #transform Prediksi
            for index in range(len(self.normalisasi_prediksi)):
                hasil=FungsiAktivasi.transform_sigmoid_bipolar(self.normalisasi_prediksi[index])
                self.transform_prediksi[index]=hasil*self.stdev_data+self.mean_data
            
        elif self.tipe_normalisasi == 'z-score-tanh':
            #transform output latih
            for index in range(len(self.data_output_latih)):
                hasil=FungsiAktivasi.transform_tanh(self.data_output_latih[index])
                self.transform_output_latih[index]=hasil*self.stdev_data+self.mean_data
            #transform target latih
            for index in range(len(self.data_target_latih)):
                hasil=FungsiAktivasi.transform_tanh(self.data_target_latih[index])
                self.transform_target_latih[index]=hasil*self.stdev_data+self.mean_data
            #transform Prediksi
            for index in range(len(self.normalisasi_prediksi)):
                hasil=FungsiAktivasi.transform_tanh(self.normalisasi_prediksi[index])
                self.transform_prediksi[index]=hasil*self.stdev_data+self.mean_data
        
        