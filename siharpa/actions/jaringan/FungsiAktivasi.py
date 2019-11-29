#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:32:51 2019

@author: axl
"""
import math
import numpy
class FungsiAktivasi:
    def sigmoid_biner(data):
        return (1/(1+(numpy.exp(-data))))
        
    def sigmoid_bipolar(data):
        return (2*(1/(1+(numpy.exp(-data))))-1)
        
    def tanh(data):
        return (2*(1/(1+(numpy.exp(-2*data))))-1)
    
    def turunan_sigmoid_biner(data):
        return (data*(1-data))
        
    def turunan_sigmoid_bipolar(data):
        return (1/2*(1+data)*(1-data))
        
    def turunan_tanh(data):
        return ((1+data)*(1-data))
    
    def transform_sigmoid_biner(data):
        hasil = (1-data)/data
        return math.log(hasil)*-1
        
    def transform_sigmoid_bipolar(data):
        hasil = (1-data)/(1+data)
        return math.log(hasil)*-1
    
    def transform_tanh(data):
        hasil = (1-data)/(1+data)
        return math.log(hasil)*-1/2    