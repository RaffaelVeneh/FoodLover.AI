import json
import os
import re
from flask import Flask, request, jsonify

app = Flask(__name__)
NAMA_FILE_DB = 'resep.json'

# --- FUNGSI BANTUAN: BACA & TULIS FILE ---
def muat_database():
    # Jika file tidak ada, kembalikan list kosong
    if not os.path.exists(NAMA_FILE_DB):
        return []
    try:
        with open(NAMA_FILE_DB, 'r') as f:
            return json.load(f)
    except:
        return [] # Jika error/kosong

def simpan_database(data):
    with open(NAMA_FILE_DB, 'w') as f:
        json.dump(data, f, indent=2) # indent=2 agar rapi dibaca manusia

# --- ROUTE 1: PENCARIAN (YANG SUDAH ADA) ---
@app.route('/cari', methods=['POST'])
def cari_resep():
    data_masuk = request.get_json()
    input_bahan_raw = data_masuk.get('bahan', '')
    input_rasa = data_masuk.get('rasa', 'Semua')
    
    # Muat data segar dari file
    database_menu = muat_database()
    
    # Pre-processing (Regex Split)
    list_bahan_user = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', input_bahan_raw) if x]
    
    print(f"[CARI] Bahan: {list_bahan_user}, Rasa: {input_rasa}")
    
    hasil_sementara = []
    for menu in database_menu:
        # Logika Cek Rasa
        rasa_cocok = False
        if input_rasa == "Semua":
            rasa_cocok = True
        elif menu.get('rasa', '').lower() == input_rasa.lower():
            rasa_cocok = True
            
        if rasa_cocok:
            skor = 0
            # Logika Cek Bahan
            for b_menu in menu.get('bahan', []):
                for b_user in list_bahan_user:
                    # contains logic simple
                    if b_user == b_menu.lower():
                        skor += 1
                        break
            
            if skor > 0:
                hasil_sementara.append({
                    "nama": menu['nama'],
                    "rasa": menu.get('rasa', 'Umum'),
                    "skor": skor
                })

    # Sorting
    hasil_final = sorted(hasil_sementara, key=lambda x: x['skor'], reverse=True)
    return jsonify(hasil_final)

# --- ROUTE 2: TAMBAH RESEP (FITUR BARU!) ---
@app.route('/tambah', methods=['POST'])
def tambah_resep():
    data_masuk = request.get_json()
    
    nama_baru = data_masuk.get('nama')
    rasa_baru = data_masuk.get('rasa')
    bahan_raw = data_masuk.get('bahan') # String "ayam, kecap"
    
    if not nama_baru or not bahan_raw:
        return jsonify({"status": "gagal", "pesan": "Data tidak lengkap"}), 400
        
    # Bersihkan bahan menjadi list
    list_bahan_bersih = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', bahan_raw) if x]
    
    # Buat objek menu baru
    menu_baru = {
        "nama": nama_baru,
        "rasa": rasa_baru,
        "bahan": list_bahan_bersih
    }
    
    # 1. Baca database lama
    db_sekarang = muat_database()
    # 2. Tambahkan yang baru
    db_sekarang.append(menu_baru)
    # 3. Simpan kembali ke file
    simpan_database(db_sekarang)
    
    print(f"[TAMBAH] Berhasil menyimpan resep baru: {nama_baru}")
    return jsonify({"status": "sukses", "pesan": "Resep berhasil disimpan ke Server!"})

if __name__ == '__main__':
    print("Server FoodAssistant (Database File) Berjalan...")
    app.run(debug=True, port=5000)