from flask import render_template,url_for,request,redirect,flash,jsonify,session,send_file
from siharpa import app
from siharpa.models.Dummy import Dummy
from siharpa.models.Komoditas import Komoditas
from siharpa.models.Provinsi import Provinsi
from siharpa.models.Kabupaten import Kabupaten
from siharpa.models.Pasar import Pasar
from siharpa.models.Prediksi import Prediksi
from siharpa.models.User import User
from siharpa import db
from siharpa.actions.PrediksiUmum import PrediksiUmum
from siharpa.actions.KonfigurasiPrediksi import KonfigurasiPrediksi
from siharpa.actions.PrediksiNasional import PrediksiNasional
from siharpa.actions.PrediksiDaerah import PrediksiDaerah
from siharpa.actions.PrediksiImport import PrediksiImport
from datetime import date,datetime
import pandas as pd
import re
from siharpa.actions.IndonesiaScrap import IndonesiaScrap
from siharpa.actions.PasarScrap import PasarScrap
from datetime import date,timedelta
import time
import csv
import json

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/prediksi_nasional')
def prediksi_nasional():
    komoditas = Komoditas.all()
    return render_template('prediksi_nasional.html',comodities=komoditas)

@app.route('/prediksi_import')
def prediksi_import():
    return render_template('prediksi_import.html')

@app.route('/prediksi_daerah')
def prediksi_daerah():
    komoditas = Komoditas.all()
    provinsi = Provinsi.all()
    # kabupaten = Kabupaten.all()
    # pasar = Pasar.all()
    return render_template('prediksi_daerah.html',comodities=komoditas,provincies=provinsi)

@app.route('/get_option_kabupaten/<kode_provinsi>')
def get_option_kabupaten(kode_provinsi):
    objKab = Kabupaten();
    modelKab = objKab.get_option(kode_provinsi)
    # kabupaten = Kabupaten.all()
    # pasar = Pasar.all()
    kabupatens = []
    for kabupaten in modelKab:
        kabupatens.append({'id_kabupaten':kabupaten.id_kabupaten,'kode_kabupaten':kabupaten.kode_kabupaten,'nama_kabupaten':kabupaten.nama_kabupaten})
    return jsonify(kabupaten=kabupatens)

@app.route('/get_option_pasar/<kode_kabupaten>')
def get_option_pasar(kode_kabupaten):
    objPasar = Pasar();
    modelPasar = objPasar.get_option(kode_kabupaten)
    # kabupaten = Kabupaten.all()
    # pasar = Pasar.all()
    pasars = []
    for pasar in modelPasar:
        pasars.append({'id_pasar':pasar.id_pasar,'kode_pasar':pasar.kode_pasar,'nama_pasar':pasar.nama_pasar})
    return jsonify(pasar=pasars)


@app.route('/cara_penggunaan')
def cara_penggunaan():
    return 'cara Penggunaan'

@app.route('/ganti_password')
def ganti_password():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    return render_template('ganti_password.html')

@app.route('/ganti_password',methods=['POST'])
def ganti_password_post():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    print(request.form)
    if(request.form['password'] != request.form['re_password']):
        flash('Password baru tidak sama','danger')
    else:
        objUser = User()
        currUser  = objUser.where(session.get('id_user'))
        if(request.form['old_password']!=currUser.password):
            flash('Password lama tidak sama','danger')
        else:
            objUser.password = request.form['password']
            objUser.update(currUser)
            flash('Sukses ganti password','success')
    return redirect(url_for('ganti_password'))

@app.route('/prediksi_demo')
def prediksi_demo():
    komoditas = Komoditas.all()
    return render_template('index.html',comodities=komoditas)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    print(session['id_user'])
    session.pop('id_user', None)
    return redirect(url_for('index'))

@app.route('/login',methods=['POST'])
def login_post():
    print(request.form)
    user = User.isThereUser(request.form['email'],request.form['password'])
    print(user)
    if (user == None):
        flash('Email atau Password Salah','danger')
        return redirect(url_for('login'))
    session['id_user'] = user.id_user
    return redirect(url_for('index'))

@app.route('/daftar_baru')
def daftar_baru():
    return render_template('daftar_baru.html')

@app.route('/lupa_password')
def lupa_password():
    return render_template('lupa_password.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/dashboard')
def dashboard():
    print(session.get('id_user'))
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    provinsi = Provinsi.all()
    kabupaten = Kabupaten.all()
    prediksi = Prediksi.all()
    pasar = Pasar.all()
    komoditas = Komoditas.all()
    
    terakhir_update = datetime.strptime(str(prediksi[0].tanggal_update),'%Y-%m-%d').strftime('%d %B %Y')
    return render_template('dashboard.html',provinsi=len(provinsi),kabupaten=len(kabupaten),terakhir_update=terakhir_update,pasar=len(pasar),komoditas=len(komoditas))

@app.route('/provinsi')
def provinsi():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    provinsi = Provinsi.all()
    return render_template('provinsi.html',provincies=provinsi)

@app.route('/provinsi/post',methods=['POST'])
def provinsi_post():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    new_provinsi = Provinsi()
    if(new_provinsi.cekKode(request.form['kode_provinsi'])):
        new_provinsi.kode_provinsi=request.form['kode_provinsi']
        new_provinsi.nama_provinsi=request.form['nama_provinsi']
        new_provinsi.save()
        flash('Sukses Menambah','success')
    else:
        flash('Gagal Menambah Kode Sudah Ada','danger')
    return redirect(url_for('provinsi'))

@app.route('/provinsi/edit',methods=['POST'])
def provinsi_edit():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    print(session.get('id_user'))
    provinsi = Provinsi()
    if(provinsi.cekKode(request.form['kode_provinsi'])):
        provinsi.kode_provinsi=request.form['kode_provinsi']
        provinsi.nama_provinsi=request.form['nama_provinsi']
        picked_provinsi = provinsi.where(request.form['id_provinsi'])
        provinsi.update(picked_provinsi)
        flash('Sukses Merubah','success')
    else:
        picked_provinsi = provinsi.where(request.form['id_provinsi'])
        provinsi.nama_provinsi=request.form['nama_provinsi']
        provinsi.kode_provinsi=picked_provinsi.kode_provinsi
        provinsi.update(picked_provinsi)
        flash('Sukses Merubah','success')
    return redirect(url_for('provinsi'))

@app.route('/provinsi/delete/<id>')
def provinsi_delete(id):
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    provinsi = Provinsi()
    picked_provinsi = provinsi.where(id)
    provinsi.delete(picked_provinsi)
    flash('Sukses Menghapus','success')
    return redirect(url_for('provinsi'))

@app.route('/kabupaten')
def kabupaten():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    kabupatens = Kabupaten.all()
    provincies = Provinsi.all()
    return render_template('kabupaten.html',kabupatens=kabupatens,provincies=provincies)

@app.route('/kabupaten/post',methods=['POST'])
def kabupaten_post():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    # print(request.form)
    new_kabupaten = Kabupaten()
    if(new_kabupaten.cekKode(request.form['kode_kabupaten'])):
        new_kabupaten.kode_provinsi=request.form['kode_provinsi']
        new_kabupaten.kode_kabupaten=request.form['kode_kabupaten']
        new_kabupaten.nama_kabupaten=request.form['nama_kabupaten']
        new_kabupaten.save()
        flash('Sukses Menambah','success')
    else:
        flash('Gagal Menambah Kode Sudah Ada','danger')
    return redirect(url_for('kabupaten'))

@app.route('/kabupaten/edit',methods=['POST'])
def kabupaten_edit():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    new_kabupaten = Kabupaten()
    if(new_kabupaten.cekKode(request.form['kode_kabupaten'])):
        new_kabupaten.kode_provinsi=request.form['kode_provinsi']
        new_kabupaten.kode_kabupaten=request.form['kode_kabupaten']
        new_kabupaten.nama_kabupaten=request.form['nama_kabupaten']
        picked_kabupaten = new_kabupaten.where(request.form['id_kabupaten'])
        new_kabupaten.update(picked_kabupaten)
        flash('Sukses Merubah','success')
    else:
        picked_kabupaten = new_kabupaten.where(request.form['id_kabupaten'])
        new_kabupaten.kode_provinsi=request.form['kode_provinsi']
        new_kabupaten.kode_kabupaten=picked_kabupaten.kode_kabupaten
        new_kabupaten.nama_kabupaten=request.form['nama_kabupaten']
        new_kabupaten.update(picked_kabupaten)
        flash('Sukses Merubah','success')
    return redirect(url_for('kabupaten'))

@app.route('/kabupaten/delete/<id>')
def kabupaten_delete(id):
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    kabupaten = Kabupaten()
    picked_kabupaten = kabupaten.where(id)
    kabupaten.delete(picked_kabupaten)
    flash('Sukses Menghapus','success')
    return redirect(url_for('kabupaten'))

@app.route('/pasar')
def pasar():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    pasars = Pasar.all()
    kabupatens = Kabupaten.all()
    return render_template('pasar.html',pasars=pasars,kabupatens=kabupatens)

@app.route('/pasar/post',methods=['POST'])
def pasar_post():
    # print(request.form)
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    new_pasar = Pasar()
    if(new_pasar.cekKode(request.form['kode_pasar'])):
        new_pasar.kode_pasar=request.form['kode_pasar']
        new_pasar.nama_pasar=request.form['nama_pasar']
        new_pasar.kode_kabupaten=request.form['kode_kabupaten']
        new_pasar.save()
        flash('Sukses Menambah','success')
    else:
        flash('Gagal Menambah Kode Sudah Ada','danger')
    return redirect(url_for('pasar'))

@app.route('/pasar/edit',methods=['POST'])
def pasar_edit():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    new_pasar = Pasar()
    if(new_pasar.cekKode(request.form['kode_pasar'])):
        new_pasar.kode_kabupaten=request.form['kode_kabupaten']
        new_pasar.kode_pasar=request.form['kode_pasar']
        new_pasar.nama_pasar=request.form['nama_pasar']
        picked_pasar = new_pasar.where(request.form['id_pasar'])
        new_pasar.update(picked_pasar)
        flash('Sukses Merubah','success')
    else:
        picked_pasar = new_pasar.where(request.form['id_pasar'])
        new_pasar.kode_kabupaten=request.form['kode_kabupaten']
        new_pasar.kode_pasar=picked_pasar.kode_pasar
        new_pasar.nama_pasar=request.form['nama_pasar']
        new_pasar.update(picked_pasar)
        flash('Sukses Merubah','success')
    return redirect(url_for('pasar'))

@app.route('/pasar/delete/<id>')
def pasar_delete(id):
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    pasar = Pasar()
    picked_pasar = pasar.where(id)
    pasar.delete(picked_pasar)
    flash('Sukses Menghapus','success')
    return redirect(url_for('pasar'))

@app.route('/komoditas')
def komoditas():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    comodities = Komoditas.all()
    return render_template('komoditas.html',comodities=comodities)

@app.route('/komoditas/post',methods=['POST'])
def komoditas_post():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    # print(request.form)
    new_komoditas = Komoditas()
    if(new_komoditas.cekKode(request.form['kode_komoditas'])):
        new_komoditas.kode_komoditas=request.form['kode_komoditas']
        new_komoditas.nama_komoditas=request.form['nama_komoditas']
        new_komoditas.save()
        flash('Sukses Menambah','success')
    else:
        flash('Gagal Menambah Kode Sudah Ada','danger')
    return redirect(url_for('komoditas'))

@app.route('/komoditas/edit',methods=['POST'])
def komoditas_edit():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    new_komoditas = Komoditas()
    if(new_komoditas.cekKode(request.form['kode_komoditas'])):
        new_komoditas.kode_komoditas=request.form['kode_komoditas']
        new_komoditas.nama_komoditas=request.form['nama_komoditas']
        picked_komoditas = new_komoditas.where(request.form['id_komoditas'])
        new_komoditas.update(picked_komoditas)
        flash('Sukses Merubah','success')
    else:
        picked_komoditas = new_komoditas.where(request.form['id_komoditas'])
        new_komoditas.kode_komoditas=picked_komoditas.kode_komoditas
        new_komoditas.nama_komoditas=request.form['nama_komoditas']
        new_komoditas.update(picked_komoditas)
        flash('Sukses Merubah','success')
    return redirect(url_for('komoditas'))

@app.route('/komoditas/delete/<id>')
def komoditas_delete(id):
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    komoditas = Komoditas()
    picked_komoditas = komoditas.where(id)
    komoditas.delete(picked_komoditas)
    flash('Sukses Menghapus','success')

    return redirect(url_for('komoditas'))

@app.route('/prediksi')
def prediksi():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    comodities = Komoditas.all()
    prediksi = Prediksi.all()
    normalisasis = [{"val":"maks-min","text":"Max-Min"},{"val":"desimal","text":"Desimal"},{"val":"z-score-biner","text":"Z-Score & Sigmoid Biner"},{"val":"z-score-bipolar","text":"Z-Score & Sigmoid Bipolar"},{"val":"z-score-tanh","text":"Z-Score & Sigmoid Tangen Hiperbolik"}]
    return render_template('prediksi.html',comodities = comodities,prediksi=prediksi[0],normalisasis=normalisasis)

@app.route('/prediksi',methods=['POST'])
def prediksi_post():
    if (session.get('id_user') == None):
        return redirect(url_for('login'))
    print(request.form)
    prediksi = Prediksi();
    prediksi.epoh = request.form['epoh']
    prediksi.learn_rate = request.form['learn_rate']
    prediksi.normalisasi = request.form['normalisasi']
    prediksi.neuron_input = request.form['neuron_input']
    prediksi.neuron_hidden = request.form['neuron_hidden']
    prediksi.hidden_layer = request.form['hidden_layer']
    prediksi.save()
    return jsonify(message='success')

@app.route('/api/predict/<jenis>',methods=['POST'])
def api_predict(jenis):
    if(jenis == 'nasional'):
        print(request.form)
        prediksi = Prediksi.all();
        print(prediksi)
        harga_pangan = []
        start_time = time.time()
        try:
            hari_diprediksi    = int(request.form['hari_prediksi'])              # inisialisasi banyak hari diprediksi
            komod_obj = Komoditas()
            komoditas = komod_obj.where(request.form['id_komoditas'])

            #Hari ini
            today = date.today()

            #End Date
            end_date = today.strftime('%d-%m-%Y')
            
            print('End Date ',end_date)

            if(today.month-1 == 0):
                #Start Date
                start_date = date(today.year-1,12,today.day).strftime('%d-%m-%Y')
            else:
                #Start Date
                start_date = date(today.year,today.month-1,today.day).strftime('%d-%m-%Y')
                
            print('Start Date ',start_date)
            print('End Date ',end_date)
            
            data = IndonesiaScrap(komoditas.kode_komoditas,komoditas.nama_komoditas,hari_diprediksi,start_date,end_date)
            #self.hargaPangan = self.data.hargaPangan
            #self.tanggalPangan = self.data.tanggalPangan
            
            harga_pangan = data.hargaPangan

            pred = PrediksiNasional(data,harga_pangan,request.form['id_komoditas'],request.form['hari_prediksi'],prediksi[0].neuron_input,prediksi[0].neuron_hidden,prediksi[0].epoh,prediksi[0].learn_rate,prediksi[0].hidden_layer,prediksi[0].normalisasi)
        except ZeroDivisionError:
            message = 'Harga pangan stabil pada Rp.'+str(int(harga_pangan[0]))+' tidak dapat melakukan prediksi'
            return jsonify(messages=message)
        except Exception as e:
            return jsonify(messages=str(e))
        else:
            waktu = (time.time() - start_time)
            return jsonify(messages='Success',data=pred.hargaPangan,tanggal=pred.tanggalPangan,prediksi=pred.hargaPrediksi,akurasi =  pred.akurasi,waktu = waktu)
        # data = PrediksiUmum(request.form['komoditas'],request.form['hari_diprediksi'])
    elif(jenis == 'daerah'):
        print(request.form)
        prediksi = Prediksi.all();
        print(prediksi)
        harga_pangan =[]
        start_time = time.time()
        try:
            hari_diprediksi    = int(request.form['hari_prediksi'])              # inisialisasi banyak hari diprediksi
            komod_obj = Komoditas()
            komoditas = komod_obj.where(request.form['id_komoditas'])

            #Hari ini
            today = date.today()

            #End Date
            end_date = today.strftime('%d-%m-%Y')
            
            if(today.month-1 == 0):
                #Start Date
                start_date = date(today.year-1,12,today.day).strftime('%d-%m-%Y')
            else:
                #Start Date
                start_date = date(today.year,today.month-1,today.day).strftime('%d-%m-%Y')

            print('Start Date ',start_date)
            print('End Date ',end_date)
            
            data = PasarScrap(komoditas.kode_komoditas,komoditas.nama_komoditas,hari_diprediksi,start_date,end_date,request.form['kode_provinsi'],request.form['kode_kabupaten'],request.form['kode_pasar'])

            harga_pangan = data.hargaPangan
            #self.hargaPangan = self.data.hargaPangan
            #self.tanggalPangan = self.data.tanggalPangan

            pred = PrediksiDaerah(data,harga_pangan,request.form['id_komoditas'],request.form['hari_prediksi'],prediksi[0].neuron_input,prediksi[0].neuron_hidden,prediksi[0].epoh,prediksi[0].learn_rate,prediksi[0].hidden_layer,prediksi[0].normalisasi,request.form['kode_provinsi'],request.form['kode_kabupaten'],request.form['kode_pasar'])
        except ZeroDivisionError:
            message = 'Harga pangan stabil pada Rp.'+str(int(harga_pangan[0]))+' tidak dapat melakukan prediksi'
            return jsonify(messages=message)
        except Exception as e:
            return jsonify(messages=str(e))
        else:
            waktu = (time.time() - start_time)
            return jsonify(messages='Success',data=pred.hargaPangan,tanggal=pred.tanggalPangan,prediksi=pred.hargaPrediksi,akurasi =  pred.akurasi,waktu = waktu)
            
    elif(jenis == 'import'):
        print(request.form)
        print(request.files['excel'])
        prediksi = Prediksi.all();
        print(prediksi)

        # data = PrediksiImport(request.form['hari_prediksi'],request.files['excel'],prediksi[0].neuron_input,prediksi[0].neuron_hidden,prediksi[0].epoh,prediksi[0].learn_rate,prediksi[0].hidden_layer,prediksi[0].normalisasi)
        harga_pangan=[]
        start_time = time.time()
        try:
            hari_diprediksi = int(request.form['hari_prediksi'])
            data = pd.read_excel(request.files['excel'],header=None) 
            df = pd.DataFrame(data)
            print(df)
            arrOfExcel = df.values.tolist()
            print(arrOfExcel)
            raw_harga_pangan = arrOfExcel[-1][2:]
            if(len(raw_harga_pangan) < 6):
                raise Exception("Data histori terlalu sedikit")
            print('raw harga pangan ',raw_harga_pangan)
            for harga in raw_harga_pangan:
                x = re.findall("\d+", str(harga))
                x=''.join(x)
                print(x)
                harga_pangan.append(int(x))
            print('harga pangan',harga_pangan)
            data = PrediksiImport(arrOfExcel,harga_pangan,request.form['hari_prediksi'],request.files['excel'],prediksi[0].neuron_input,prediksi[0].neuron_hidden,prediksi[0].epoh,prediksi[0].learn_rate,prediksi[0].hidden_layer,prediksi[0].normalisasi)
        except ZeroDivisionError:
            message = 'Harga pangan stabil pada Rp.'+str(int(harga_pangan[0]))+' tidak dapat melakukan prediksi'
            return jsonify(messages=message)
        except Exception as e:
            return jsonify(messages=str(e))
        else:
            waktu = (time.time() - start_time)
            return jsonify(messages='Success',data=data.hargaPangan,tanggal=data.tanggalPangan,prediksi=data.hargaPrediksi,akurasi =  data.akurasi,waktu = waktu)
        

    else:
        print(request.form)
        print('konfigurasi')
        harga_pangan=[]
        start_time = time.time()
        try:
            hari_diprediksi    = int(request.form['hari_prediksi'])              # inisialisasi banyak hari diprediksi
            komod_obj = Komoditas()
            komoditas = komod_obj.where(request.form['id_komoditas'])

            #Hari ini
            today = date.today()

            #tanggal start  
            #start_date = date(today.year,today.month-1,today.day-hari_diprediksi).strftime('%d-%m-%Y')
            #tanggal end 
                    #End Date
            end_date = today.strftime('%d-%m-%Y')
            
            #Start Date
            start_date = (today-timedelta(days=30+hari_diprediksi)).strftime('%d-%m-%Y')

            print('Start Date ',start_date)
            print('End Date ',end_date)
            
            data = IndonesiaScrap(komoditas.kode_komoditas,komoditas.nama_komoditas,0,start_date,end_date)
            #self.hargaPangan = self.data.hargaPangan
            #self.tanggalPangan = self.data.tanggalPangan
            harga_pangan = data.hargaPangan
            pred = KonfigurasiPrediksi(data,harga_pangan,request.form['id_komoditas'],request.form['hari_prediksi'],request.form['neuron_input'],request.form['neuron_hidden'],request.form['epoh'],request.form['learn_rate'],request.form['hidden_layer'],request.form['normalisasi'])
            
        except ZeroDivisionError:
            message = 'Harga pangan stabil pada Rp.'+str(int(harga_pangan[0]))+' tidak dapat melakukan prediksi'
            return jsonify(messages=message)
        except Exception as e:
            return jsonify(messages=str(e))
        else:
            waktu = (time.time() - start_time)
            return jsonify(messages='Success',data=pred.hargaPangan,tanggal=pred.tanggalPangan,prediksi=pred.hargaPrediksi,akurasi =  pred.akurasi,waktu = waktu)
    # return jsonify(data=data.data.hargaPangan,tanggal=data.data.tanggalPangan)

@app.route('/export/<tanggal>/<data>/<prediksi>/<akurasi>/<waktu>')
def export(tanggal,data,prediksi,akurasi,waktu):
    tanggal = json.loads(tanggal)
    harga_prediksi = json.loads(prediksi)
    harga_asli = json.loads(data)
    # akurasi = json.loads(akurasi)
    # waktu = json.loads(waktu)
    with open('export.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['tanggal']+tanggal)
        writer.writerow(['harga asli']+harga_asli)
        writer.writerow(['harga prediksi']+harga_prediksi)
        writer.writerow(['Akurasi',akurasi])
        writer.writerow(['Waktu',waktu])
    try:
        return send_file('../export.csv',mimetype='application/x-csv',attachment_filename='export.csv',as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/contoh_file')
def contoh_file():
    return send_file('../contoh.xls',mimetype='application/x-csv',attachment_filename='contoh.xls',as_attachment=True)
    



