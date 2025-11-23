import json
import random
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

FILE_RESEP = 'resep.json'
FILE_MODEL = 'model_cerdas.pkl'
FILE_ENCODER = 'encoder_bahan.pkl'
FILE_ENCODER_RASA = 'encoder_rasa.pkl'

def generate_dataset_palsu(jumlah_data=1000):
    print(f"[INFO] Sedang men-generate {jumlah_data} data latihan sintetis...")
    
    with open(FILE_RESEP, 'r') as f:
        database_resep = json.load(f)
    
    dataset = []
    
    for _ in range(jumlah_data):
        target_resep = random.choice(database_resep)
        
        bahan_asli = target_resep['bahan']
        
        jumlah_bahan_input = random.randint(1, len(bahan_asli))
        input_user = random.sample(bahan_asli, jumlah_bahan_input)
        
        meta_waktu = target_resep.get('metadata', {}).get('waktu', ['kapanpun'])
        waktu_simulasi = random.choice(meta_waktu)
        if waktu_simulasi == 'kapanpun':
            waktu_simulasi = random.choice(['pagi', 'siang', 'malam'])
            
        rasa_menu = target_resep.get('rasa', 'Umum')
            
        dataset.append({
            "bahan_input": input_user,
            "waktu": waktu_simulasi,
            "rasa_input": rasa_menu,
            "target_nama": target_resep['nama']
        })
        
    return pd.DataFrame(dataset)

def latih_otak(): 
    df = generate_dataset_palsu(2000)
    
    print("[INFO] Melakukan Vectorization (Teks -> Angka)...")
    
    # BAHAN (One-Hot)
    mlb = MultiLabelBinarizer()
    X_bahan = mlb.fit_transform(df['bahan_input'])
    
    # WAKTU (Mapping Manual)
    map_waktu = {'pagi': 0, 'siang': 1, 'sore': 2, 'malam': 3}
    X_waktu = df['waktu'].map(map_waktu).fillna(1).values.reshape(-1, 1) 
    
    # RASA (One-Hot)
    mlb_rasa = MultiLabelBinarizer()
    rasa_list = [[r] for r in df['rasa_input']]
    X_rasa = mlb_rasa.fit_transform(rasa_list)
    
    # GABUNG SEMUA FITUR
    print(f"[INFO] Dimensi Fitur: Bahan={X_bahan.shape[1]}, Waktu=1, Rasa={X_rasa.shape[1]}")
    X_final = np.hstack((X_bahan, X_waktu, X_rasa))
    y = df['target_nama']
    
    # Neural Network
    print("[INFO] Sedang melatih Neural Network (Flavor-Aware)...")
    model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    
    model.fit(X_final, y)
    
    print(f"[SUKSES] Model selesai dilatih! Akurasi pada data latihan: {model.score(X_final, y)*100:.2f}%")
    
    # SIMPAN SEMUA
    joblib.dump(model, FILE_MODEL)
    joblib.dump(mlb, FILE_ENCODER)
    joblib.dump(mlb_rasa, FILE_ENCODER_RASA) 
    print("[INFO] Model, Encoder Bahan, dan Encoder Rasa berhasil disimpan.")

if __name__ == "__main__":
    latih_otak()