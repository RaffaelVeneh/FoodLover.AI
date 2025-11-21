import json
import random
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

# KONFIGURASI FILE
FILE_RESEP = 'resep.json'
FILE_MODEL = 'model_cerdas.pkl'
FILE_ENCODER = 'encoder_bahan.pkl'

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
            
        dataset.append({
            "bahan_input": input_user,
            "waktu": waktu_simulasi,
            "target_nama": target_resep['nama']
        })
        
    return pd.DataFrame(dataset)

def latih_otak(): 
    df = generate_dataset_palsu(2000)
    
    print("[INFO] Melakukan Vectorization (Teks -> Angka)...")
    
    # Ingredient Vectorization (One-Hot Encoding)
    mlb = MultiLabelBinarizer()
    X_bahan = mlb.fit_transform(df['bahan_input'])
    
    # Time Vectorization
    map_waktu = {'pagi': 0, 'siang': 1, 'sore': 2, 'malam': 3}
    X_waktu = df['waktu'].map(map_waktu).fillna(1).values.reshape(-1, 1) 
    
    import numpy as np
    X_final = np.hstack((X_bahan, X_waktu))
    y = df['target_nama']
    
    # Neural Network (MLPClassifier)
    print("[INFO] Sedang melatih Neural Network...")
    model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    
    model.fit(X_final, y)
    
    print(f"[SUKSES] Model selesai dilatih! Akurasi pada data latihan: {model.score(X_final, y)*100:.2f}%")
    
    joblib.dump(model, FILE_MODEL)
    joblib.dump(mlb, FILE_ENCODER)
    print("[INFO] Model dan Encoder berhasil disimpan.")

if __name__ == "__main__":
    latih_otak()