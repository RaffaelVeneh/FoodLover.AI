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

# --- 1. GENERATOR DATA LATIHAN (MOCK DATA) ---
def generate_dataset_palsu(jumlah_data=1000):
    print(f"[INFO] Sedang men-generate {jumlah_data} data latihan sintetis...")
    
    with open(FILE_RESEP, 'r') as f:
        database_resep = json.load(f)
    
    dataset = []
    
    # Kita akan mensimulasikan user yang 'masuk akal'
    for _ in range(jumlah_data):
        # 1. Pilih satu resep target secara acak (Misal: Bubur Ayam)
        target_resep = random.choice(database_resep)
        
        # 2. Ambil bahan-bahannya
        bahan_asli = target_resep['bahan']
        
        # 3. Simulasi Input User (Tidak selalu lengkap)
        # User kadang cuma input 50-100% dari bahan yang diperlukan
        jumlah_bahan_input = random.randint(1, len(bahan_asli))
        input_user = random.sample(bahan_asli, jumlah_bahan_input)
        
        # 4. Tambahkan Konteks Waktu (Berdasarkan Metadata Resep)
        # Jika resepnya 'pagi', kita set waktu simulasi ke 'pagi'
        meta_waktu = target_resep.get('metadata', {}).get('waktu', ['kapanpun'])
        waktu_simulasi = random.choice(meta_waktu)
        if waktu_simulasi == 'kapanpun':
            waktu_simulasi = random.choice(['pagi', 'siang', 'malam'])
            
        # 5. Simpan ke dataset
        # Input: Bahan + Waktu
        # Output (Label): Nama Resep
        dataset.append({
            "bahan_input": input_user,
            "waktu": waktu_simulasi,
            "target_nama": target_resep['nama'] # AI harus menebak ini
        })
        
    return pd.DataFrame(dataset)

# --- 2. PELATIHA MODEL (TRAINING) ---
def latih_otak(): 
    # A. Persiapkan Data
    df = generate_dataset_palsu(2000) # Buat 2000 contoh kasus
    
    print("[INFO] Melakukan Vectorization (Teks -> Angka)...")
    
    # B. Vectorization Bahan (One-Hot Encoding)
    # Mengubah ["nasi", "telur"] menjadi [1, 0, 1, 0, ...]
    mlb = MultiLabelBinarizer()
    X_bahan = mlb.fit_transform(df['bahan_input'])
    
    # C. Vectorization Waktu
    # Kita ubah Pagi=0, Siang=1, Malam=2, Sore=3 (Manual Encoding sederhana)
    map_waktu = {'pagi': 0, 'siang': 1, 'sore': 2, 'malam': 3}
    # Default ke 1 (siang) jika tidak dikenali
    X_waktu = df['waktu'].map(map_waktu).fillna(1).values.reshape(-1, 1) 
    
    # D. Gabungkan Input (Bahan + Waktu)
    # Ini adalah vektor final yang masuk ke otak AI
    import numpy as np
    X_final = np.hstack((X_bahan, X_waktu))
    
    # E. Target (Jawaban Benar)
    y = df['target_nama']
    
    # F. Buat Neural Network (MLPClassifier)
    # Hidden Layer: 100 neuron di layer 1, 50 di layer 2
    print("[INFO] Sedang melatih Neural Network...")
    model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    
    # Latih!
    model.fit(X_final, y)
    
    print(f"[SUKSES] Model selesai dilatih! Akurasi pada data latihan: {model.score(X_final, y)*100:.2f}%")
    
    # G. Simpan Otak & Encoder agar bisa dipakai di server.py
    joblib.dump(model, FILE_MODEL)
    joblib.dump(mlb, FILE_ENCODER)
    print("[INFO] Model dan Encoder berhasil disimpan.")

if __name__ == "__main__":
    latih_otak()