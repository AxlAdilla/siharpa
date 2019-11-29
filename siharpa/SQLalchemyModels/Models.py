from siharpa import db

class Komoditas(db.Model):
    id_komoditas = db.Column(db.Integer,primary_key=True)
    kode_komoditas = db.Column(db.String(10),nullable=False)   
    nama_komoditas = db.Column(db.String(50),nullable=False)   

    def __repr__(self):
        return f"Dummy('{self.id_komoditas}','{self.kode_komoditas}','{self.nama_komoditas}')"

class User(db.Model):
    id_user = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),nullable=False)   
    password = db.Column(db.String(50),nullable=False)   

    def __repr__(self):
        return f"User('{self.id_user}','{self.email}','{self.password}')"

class Provinsi(db.Model):
    id_provinsi = db.Column(db.Integer,primary_key=True)
    kode_provinsi = db.Column(db.String(10),nullable=False)   
    nama_provinsi = db.Column(db.String(50),nullable=False)   
    kabupatens = db.relationship('Kabupaten',backref='parent')
    def __repr__(self):
        return f"Dummy('{self.id_provinsi}','{self.kode_provinsi}','{self.nama_provinsi}')"

class Kabupaten(db.Model):
    id_kabupaten = db.Column(db.Integer,primary_key=True)
    kode_kabupaten = db.Column(db.String(10),nullable=False)   
    nama_kabupaten = db.Column(db.String(50),nullable=False)   
    kode_provinsi = db.Column(db.Integer,db.ForeignKey('provinsi.kode_provinsi'))
    pasars = db.relationship('Pasar',backref='parent')
    def __repr__(self):
        return f"Dummy('{self.id_kabupaten}','{self.kode_kabupaten}','{self.nama_kabupaten}')"

class Pasar(db.Model):
    id_pasar = db.Column(db.Integer,primary_key=True)
    kode_pasar = db.Column(db.String(10),nullable=False)   
    nama_pasar = db.Column(db.String(50),nullable=False)   
    kode_kabupaten = db.Column(db.Integer,db.ForeignKey('kabupaten.kode_kabupaten'))
    def __repr__(self):
        return f"Dummy('{self.id_pasar}','{self.kode_pasar}','{self.nama_pasar}')"

class Prediksi(db.Model):
    id_prediksi = db.Column(db.Integer,primary_key=True)
    epoh = db.Column(db.Integer,nullable=False)   
    learn_rate = db.Column(db.Float,nullable=False)   
    normalisasi = db.Column(db.String(50),nullable=False)   
    neuron_input = db.Column(db.Integer,nullable=False)   
    neuron_hidden = db.Column(db.Integer,nullable=False)   
    hidden_layer = db.Column(db.Integer,nullable=False)   
    tanggal_update = db.Column(db.DateTime,nullable=False)   
    def __repr__(self):
        return f"Prediksi('{self.id_prediksi}','{self.epoh}','{self.learn_rate}','{self.normalisasi}','{self.neuron_input}','{self.neuron_hidden}','{self.hidden_layer}','{self.tanggal_update}')"