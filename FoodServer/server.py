import json
import os
import re
from flask import Flask, request, jsonify
from thefuzz import fuzz

app = Flask(__name__)
NAMA_FILE_DB = 'resep.json'
NAMA_FILE_KAMUS = 'kamus.json'

def muat_json(nama_file):
    # Fungsi serbaguna untuk membaca file JSON
    if not os.path.exists(nama_file):
        print(f"[INFO] File {nama_file} tidak ditemukan, membuat baru/kosong.")
        return {} if nama_file == NAMA_FILE_KAMUS else []
    try:
        with open(nama_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Gagal membaca {nama_file}: {e}")
        return {} if nama_file == NAMA_FILE_KAMUS else []

def simpan_database(data):
    with open(NAMA_FILE_DB, 'w') as f:
        json.dump(data, f, indent=2)

CACHE_KAMUS = muat_json(NAMA_FILE_KAMUS)
print(f"[INFO] Kamus berhasil dimuat: {len(CACHE_KAMUS)} kata sinonim.")

# --- FUNGSI PENCARI CERDAS (FUZZY LOGIC) ---
# --- 2. LOGIKA PENCARIAN CERDAS (REVISI TOTAL) ---
def cek_kemiripan(bahan_user, bahan_resep):
    # A. Cek Sinonim dari File kamus.json
    # Pastikan "mi" diubah jadi "mie" (atau standar database Anda)
    bahan_user = CACHE_KAMUS.get(bahan_user, bahan_user)
    bahan_resep_asli = bahan_resep # Simpan nama asli
    
    # B. Exact Match (Cepat & Pasti)
    if bahan_user == bahan_resep:
        return True

    # C. Word Boundary Check (Cek per Kata) - SOLUSI MASALAH "MI" vs "MINYAK"
    # Kita pecah "minyak goreng" menjadi ["minyak", "goreng"]
    # Kita cek apakah "mi" ada di list itu? Jawabannya TIDAK.
    # Tapi jika "ayam" vs "daging ayam", "ayam" ada di list.
    kata_kunci_resep = re.split(r'[,\.\s]+', bahan_resep) # Split jadi list kata
    if bahan_user in kata_kunci_resep:
        return True
        
    # D. Fuzzy Match (Typo Tolerance) - Dengan Logika Lebih Ketat
    # token_sort_ratio: Mengabaikan urutan kata (bawang merah == merah bawang)
    # tapi TIDAK mencocokkan "mi" dengan "minyak".
    skor = fuzz.token_sort_ratio(bahan_user, bahan_resep)
    
    # Kita pasang standar tinggi (90) agar tidak sembarangan mencocokkan
    if skor >= 90: 
        return True
        
    # E. Khusus Kata Panjang (Partial Match hanya untuk kata > 3 huruf)
    # Ini untuk menangani kasus "stroberi" vs "selai stroberi" 
    # Tanpa memicu "mi" vs "minyak"
    if len(bahan_user) > 3 and bahan_user in bahan_resep:
        return True
        
    return False

@app.route('/cari', methods=['POST'])
def cari_resep():
    data_masuk = request.get_json()
    input_bahan_raw = data_masuk.get('bahan', '')
    input_rasa = data_masuk.get('rasa', 'Semua')
    
    database_menu = muat_json(NAMA_FILE_DB) # Muat ulang DB agar update realtime
    
    # Bersihkan input user
    list_bahan_user = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', input_bahan_raw) if x]
    
    hasil_sementara = []
    
    for menu in database_menu:
        # Filter Rasa
        rasa_cocok = False
        if input_rasa == "Semua":
            rasa_cocok = True
        elif menu.get('rasa', '').lower() == input_rasa.lower():
            rasa_cocok = True
            
        if rasa_cocok:
            skor = 0
            bahan_cocok_list = []
            semua_bahan_resep = menu.get('bahan', [])
            
            # Cek Bahan
            for b_resep in semua_bahan_resep:
                b_resep_kecil = b_resep.lower()
                for b_user in list_bahan_user:
                    if cek_kemiripan(b_user, b_resep_kecil):
                        skor += 1
                        bahan_cocok_list.append(b_resep)
                        break 
            
            if skor > 0:
                hasil_sementara.append({
                    "nama": menu['nama'],
                    "rasa": menu.get('rasa', 'Umum'),
                    "skor": skor,
                    "bahan_lengkap": "|".join(semua_bahan_resep),
                    "bahan_match": "|".join(bahan_cocok_list)
                })

    hasil_final = sorted(hasil_sementara, key=lambda x: x['skor'], reverse=True)
    return jsonify(hasil_final)

@app.route('/tambah', methods=['POST'])
def tambah_resep():
    data_masuk = request.get_json()
    nama_baru = data_masuk.get('nama')
    rasa_baru = data_masuk.get('rasa')
    bahan_raw = data_masuk.get('bahan')
    
    if not nama_baru or not bahan_raw:
        return jsonify({"status": "gagal", "pesan": "Data tidak lengkap"}), 400
        
    list_bahan_bersih = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', bahan_raw) if x]
    
    menu_baru = {
        "nama": nama_baru,
        "rasa": rasa_baru,
        "bahan": list_bahan_bersih
    }
    
    db_sekarang = muat_json(NAMA_FILE_DB)
    db_sekarang.append(menu_baru)
    simpan_database(db_sekarang)
    
    return jsonify({"status": "sukses", "pesan": "Resep disimpan!"})

# Fitur Tambahan: Reload Kamus tanpa restart server
@app.route('/reload-kamus', methods=['GET'])
def reload_kamus():
    global CACHE_KAMUS
    CACHE_KAMUS = muat_json(NAMA_FILE_KAMUS)
    return jsonify({"status": "sukses", "pesan": "Kamus sinonim telah diperbarui!", "jumlah_kata": len(CACHE_KAMUS)})

if __name__ == '__main__':
    print("Server AI FoodAssistant Berjalan...")
    app.run(debug=True, port=5000)