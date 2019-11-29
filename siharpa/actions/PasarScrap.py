from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re
from datetime import date,timedelta

class PasarScrap:
    def __init__(self,kode_komoditas,nama_komoditas,hari_diprediksi,start_date,end_date,kode_provinsi,kode_kabupaten,kode_pasar):
        self.hargaPangan = []
        self.tanggalPangan = []

        # driver = webdriver.PhantomJS('/home/axl/Documents/TA/WebApp/Scrapping/lastattempt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)

        url = "https://hargapangan.id/tabel-harga/pasar-tradisional/daerah"    
        driver.get(url)

        Select(driver.find_element_by_id('filter_commodity_ids')).select_by_value(kode_komoditas)

        start_date_element = driver.find_element_by_id('filter_start_date')
        end_date_element = driver.find_element_by_id('filter_end_date')
        province_element = driver.find_element_by_id('filter_province_ids')
        regency_element = driver.find_element_by_id('filter_regency_ids')
        market_element = driver.find_element_by_id('filter_market_ids')
        
        javascriptCode = "arguments[0].value = arguments[1]"
        print([kode_provinsi,kode_kabupaten,kode_pasar])
        driver.execute_script(javascriptCode,start_date_element,start_date)
        driver.execute_script(javascriptCode,end_date_element,end_date)
        # driver.execute_script(javascriptCode,province_element,kode_provinsi)
        # driver.implicitly_wait(5) # seconds
        # driver.execute_script(javascriptCode,regency_element,kode_kabupaten)
        # driver.implicitly_wait(5) # seconds
        # driver.execute_script(javascriptCode,market_element,kode_pasar)
        Select(driver.find_element_by_id('filter_province_ids')).select_by_value(kode_provinsi)
        driver.implicitly_wait(3) # seconds
        Select(driver.find_element_by_id('filter_regency_ids')).select_by_value(kode_kabupaten)
        driver.implicitly_wait(3) # seconds        
        Select(driver.find_element_by_id('filter_market_ids')).select_by_value(kode_pasar)
        driver.implicitly_wait(3) # seconds

        driver.find_element_by_id('btnReport').click()

        driver.implicitly_wait(5) # seconds
        allPage = driver.find_element_by_id('report-header').get_attribute('outerHTML')
        tabel = driver.find_element_by_id('report').get_attribute('outerHTML')
        print(allPage)
        #print(tabel)

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
                self.tanggalPangan.append(tanggal.text)
                
        #Hari ini
        today = date.today()

        for index_hari_diprediksi in range(hari_diprediksi):
            #self.tanggalPangan.append(date(today.year,today.month,today.day+index_hari_diprediksi+1).strftime('%d/%m/%Y'))
            self.tanggalPangan.append((today+timedelta(days=index_hari_diprediksi+1)).strftime('%d-%m-%Y'))
            #print(date(today.year,today.month,today.day+index_hari_diprediksi+1).strftime('%d/%m/%Y'))

        print(self.tanggalPangan)

        driver.close()