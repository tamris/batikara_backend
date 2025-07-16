# model/batik_model.py

from tensorflow.keras.models import load_model

model = load_model('batik_model_8.h5')

label_kelas = ['Beras Mawur','Bukan Batik Tegalan', 'Cempaka Mulya', 'Cempaka Putih', 'Ciprat', 'Cungkilan',
    'Galaran', 'Grandil', 'Gribigan', 'Irengan', 'Jago Mogok', 'Kacangan',
    'Kangkung', 'Kawung', 'Kembang Pacar', 'Kuku Macan', 'Lompongan',
    'Megamendung', 'Parang', 'Pasiran', 'Poci Tahu Aci', 'Putri Mahkota',
    'Remekan', 'Salem', 'Sawatan', 'Sekar Jagad', 'Sidomukti', 'Sidomulyo',
    'Sisik Melik', 'Teripang', 'Watu Pecah']
