from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

class DaerahScrap:
    def __init__(self):
        #Inisialisasi Untuk Menghitung Waktu Proses Scrapping
        start_time = time.time()
        today = date.today()

        #inisialisasi ID
        komoditas = str('cat-8')
        provinsi = str(1) 
        kabupaten = str(1)
        pasar = str(2)

        #tanggal 1 bulan sebelum 
        start_date = date(today.year,today.month-1,today.day).strftime('%d-%m-%Y')
        #tanggal bulan ini 
        end_date = date.today().strftime('%d-%m-%Y')


        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)


        url = "https://hargapangan.id/tabel-harga/pasar-tradisional/daerah"    
        driver.get(url)

        Select(driver.find_element_by_id('filter_commodity_ids')).select_by_value(komoditas)
        Select(driver.find_element_by_id('filter_province_ids')).select_by_value(provinsi)
        driver.implicitly_wait(3) # seconds
        Select(driver.find_element_by_id('filter_regency_ids')).select_by_value(kabupaten)
        driver.implicitly_wait(3) # seconds        
        Select(driver.find_element_by_id('filter_market_ids')).select_by_value(pasar)
        driver.implicitly_wait(3) # seconds

        start_date_element = driver.find_element_by_id('filter_start_date')
        end_date_element = driver.find_element_by_id('filter_end_date')
        javascriptCode = "arguments[0].value = arguments[1]"

        driver.execute_script(javascriptCode,start_date_element,start_date)
        driver.execute_script(javascriptCode,end_date_element,end_date)

        driver.find_element_by_id('btnReport').click()

        driver.implicitly_wait(5) # seconds
        tabel = driver.find_element_by_id('report').get_attribute('outerHTML')

        soup=BeautifulSoup(tabel,'html.parser')
        dataHarga = soup.find_all('td',attrs={'data-original-title':'Cabai Rawit'})
        hargaPangan = []
        for harga in dataHarga:
            hargaPangan.append(harga.text)

        driver.close()
        print("--- %s seconds ---" % (time.time() - start_time))