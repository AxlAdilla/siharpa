from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re
from datetime import date,timedelta

class IndonesiaScrap:
    def __init__(self,kode_komoditas,nama_komoditas,hari_diprediksi,start_date,end_date):
        self.hargaPangan = []
        self.tanggalPangan = []

        driver = webdriver.PhantomJS('/home/axl/Documents/TA/WebApp/Scrapping/lastattempt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

        url = "https://hargapangan.id/tabel-harga/pasar-tradisional/daerah"    
        driver.get(url)

        Select(driver.find_element_by_id('filter_commodity_ids')).select_by_value(kode_komoditas)

        start_date_element = driver.find_element_by_id('filter_start_date')
        end_date_element = driver.find_element_by_id('filter_end_date')
        javascriptCode = "arguments[0].value = arguments[1]"

        driver.execute_script(javascriptCode,start_date_element,start_date)
        driver.execute_script(javascriptCode,end_date_element,end_date)

        driver.find_element_by_id('btnReport').click()

        driver.implicitly_wait(5) # seconds
        tabel = driver.find_element_by_id('report').get_attribute('outerHTML')

        soup=BeautifulSoup(tabel,'html.parser')
        if(kode_komoditas == '10'):
            print(kode_komoditas)
            nama_komoditas = '''Telur Ayam Ras Segar
 (kg)'''
        dataHarga = soup.find_all('td',attrs={'data-original-title':nama_komoditas})
        dataTanggal = soup.find_all('th')
        
        for harga in dataHarga:
            self.hargaPangan.append(float(harga.text)*1000)
        
        for tanggal in dataTanggal:
            isTanggal = re.search(r"\d+/\d+/\d+", tanggal.text)
            if (isTanggal):   
                new_tanggal = re.sub('/+','-',tanggal.text)
                print(new_tanggal)
                self.tanggalPangan.append(new_tanggal)
        #Hari ini
        today = date.today()
        for index_hari_diprediksi in range(hari_diprediksi):
            #self.tanggalPangan.append(date(today.year,today.month,today.day+index_hari_diprediksi+1).strftime('%d/%m/%Y'))
            self.tanggalPangan.append((today+timedelta(days=index_hari_diprediksi+1)).strftime('%d-%m-%Y'))
            #print(date(today.year,today.month,today.day+index_hari_diprediksi+1).strftime('%d/%m/%Y'))
        print(self.tanggalPangan)
        driver.close()