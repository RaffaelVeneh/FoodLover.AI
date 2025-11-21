import json
import os
import re
import datetime
import joblib
import numpy as np
import random
from flask import Flask, request, jsonify
from collections import Counter
from thefuzz import fuzz

app = Flask(__name__)

NAMA_FILE_DB = 'resep.json'
NAMA_FILE_KAMUS = 'kamus.json'
NAMA_FILE_LOG = 'history.json'
NAMA_FILE_MODEL = 'model_cerdas.pkl'
NAMA_FILE_ENCODER = 'encoder_bahan.pkl'

# --- CONFIG & KAMUS ALAY ---
KAMUS_ALAY = {
    '4': 'a', '@': 'a',
    '3': 'e',
    '1': 'i', '!': 'i',
    '0': 'o',
    '5': 's', '$': 's',
    '2': 'z',
    '6': 'b',
    '8': 'b',
    '9': 'g',
    'g4k': 'tidak', 'gak': 'tidak', 'ga': 'tidak' # Tambahan slang umum
}

BAHAN_POKOK = {
    'nasi', 'beras', 
    'mie', 'mi', 'bakmi', 'indomie',
    'bihun', 'soun', 'kwetiau',
    'spaghetti', 'pasta', 'macaroni', 'fettucini',
    'lontong', 'ketupat',
    'roti', 'bubur'
}

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

CACHE_KAMUS = muat_json(NAMA_FILE_KAMUS)

# Load Model AI (Gunakan try-except agar server tetap jalan meski model belum ada)
try:
    OTAK_AI = joblib.load(NAMA_FILE_MODEL)
    ENCODER_AI = joblib.load(NAMA_FILE_ENCODER)
    # Ambil daftar kata yang dipelajari AI untuk validasi input
    VOCAB_AI = set(ENCODER_AI.classes_) 
    print("[INFO] Otak AI & Encoder berhasil dimuat!")
except Exception as e:
    print(f"[WARNING] Gagal memuat AI: {e}. Fitur prediksi akan dimatikan.")
    OTAK_AI = None
    ENCODER_AI = None
    VOCAB_AI = set()

def simpan_database(data):
    with open(NAMA_FILE_DB, 'w') as f:
        json.dump(data, f, indent=2)

def normalisasi_alay(teks):
    if not teks: return ""
    teks_bersih = teks.lower()
    for alay, normal in KAMUS_ALAY.items():
        teks_bersih = teks_bersih.replace(alay, normal)
    teks_bersih = re.sub(r'(.)\1+', r'\1', teks_bersih)
    return teks_bersih

# --- FUNGSI PREDIKSI AI ---
def tanya_ai(list_bahan, waktu_sekarang_str):
    if OTAK_AI is None or ENCODER_AI is None:
        return None

    # 1. Filter bahan: AI hanya mengerti bahan yang pernah dia pelajari
    bahan_valid = [b for b in list_bahan if b in VOCAB_AI]
    
    if not bahan_valid:
        return None # Tidak ada bahan yang dikenali AI

    # 2. Vectorization Bahan (Encode)
    # Mengubah ["nasi", "telur"] menjadi [[1, 0, 1, ...]]
    X_bahan = ENCODER_AI.transform([bahan_valid])

    # 3. Vectorization Waktu
    map_waktu = {'pagi': 0, 'siang': 1, 'sore': 2, 'malam': 3}
    kode_waktu = map_waktu.get(waktu_sekarang_str, 1) # Default siang (1)
    X_waktu = np.array([[kode_waktu]])

    # 4. Gabungkan (Stack)
    X_final = np.hstack((X_bahan, X_waktu))

    # 5. Prediksi!
    try:
        hasil_prediksi = OTAK_AI.predict(X_final)[0]
        # Cek tingkat keyakinan (Probability)
        proba = np.max(OTAK_AI.predict_proba(X_final))
        
        if proba > 0.4: # Hanya sarankan jika AI yakin > 40%
            return f"{hasil_prediksi} (AI Confidence: {int(proba*100)}%)"
    except:
        pass
        
    return None

# --- LOGIKA PENCARIAN CERDAS ---
def cek_kemiripan(bahan_user, bahan_resep):
    bahan_user = normalisasi_alay(bahan_user)
    bahan_user = CACHE_KAMUS.get(bahan_user, bahan_user)
    
    if bahan_user == bahan_resep: return True
    
    kata_kunci_resep = re.split(r'[,\.\s]+', bahan_resep)
    if bahan_user in kata_kunci_resep: return True
        
    skor = fuzz.token_sort_ratio(bahan_user, bahan_resep)
    if skor >= 80: return True
        
    if len(bahan_user) > 3 and bahan_user in bahan_resep: return True
        
    return False

# --- LOGIKA REKOMENDASI RANDOM (FALLBACK) ---
def get_personalized_recommendations(database, limit=10):
    history = muat_json(NAMA_FILE_LOG)
    
    # Jika history kosong, kembali ke random biasa
    if not isinstance(history, list) or len(history) == 0:
        return get_random_fallback(database, limit, "Sepertinya kamu baru disini. Ini beberapa menu populer untukmu:")

    # 1. ANALISA MEMORI (Apa yang sering dipilih?)
    list_menu_dipilih = [h.get('menu_dipilih') for h in history if h.get('menu_dipilih')]
    # Hitung frekuensi: {'Nasi Goreng': 5, 'Teh Manis': 2}
    counter_menu = Counter(list_menu_dipilih)
    
    # Ambil Top 5 Menu Favorit
    top_menu_names = [m[0] for m in counter_menu.most_common(5)]
    
    hasil_personal = []
    nama_personal = set() # Untuk mencegah duplikasi

    # Cari detail resep dari database untuk menu favorit ini
    for menu in database:
        if menu['nama'] in top_menu_names:
            meta = menu.get('metadata', {})
            hasil_personal.append({
                "nama": menu['nama'],
                "rasa": menu.get('rasa', 'Umum'),
                "skor": 0, "relevansi": 1.0, "is_ai": True, # Kita anggap relevan karena user suka
                "bahan_lengkap": "|".join(menu.get('bahan', [])),
                "bahan_match": "(Favorit Kamu)", # Penanda visual
                "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
                "meta_kategori": meta.get('kategori', 'umum'),
                "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
                "label_ai": "YA", # Kita kasih bintang biar spesial
                "pesan_sistem": ""
            })
            nama_personal.add(menu['nama'])

    # 2. ISI SISANYA DENGAN RANDOM (Discovery)
    # Supaya user tidak bosan makan itu-itu saja
    sisa_slot = limit - len(hasil_personal)
    if sisa_slot > 0:
        # Filter database: Jangan masukkan menu yang sudah ada di list favorit
        db_sisa = [m for m in database if m['nama'] not in nama_personal]
        if db_sisa:
            tambahan_random = random.sample(db_sisa, min(len(db_sisa), sisa_slot))
            for menu in tambahan_random:
                meta = menu.get('metadata', {})
                hasil_personal.append({
                    "nama": menu['nama'],
                    "rasa": menu.get('rasa', 'Umum'),
                    "skor": 0, "relevansi": 0, "is_ai": False,
                    "bahan_lengkap": "|".join(menu.get('bahan', [])),
                    "bahan_match": "",
                    "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
                    "meta_kategori": meta.get('kategori', 'umum'),
                    "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
                    "label_ai": "TIDAK",
                    "pesan_sistem": ""
                })

    # Tambahkan pesan sistem di item pertama
    if hasil_personal:
        hasil_personal[0]['pesan_sistem'] = "Sepertinya kamu sedang bingung mencari apa. ini rekomendasi spesial & menu baru:"
        
    return hasil_personal

def get_random_fallback(database, limit, pesan):
    # Fungsi random murni (Backup)
    jumlah = min(len(database), limit)
    pilihan_acak = random.sample(database, jumlah)
    hasil = []
    for i, menu in enumerate(pilihan_acak):
        meta = menu.get('metadata', {})
        hasil.append({
            "nama": menu['nama'],
            "rasa": menu.get('rasa', 'Umum'),
            "skor": 0, "relevansi": 0, "is_ai": False,
            "bahan_lengkap": "|".join(menu.get('bahan', [])),
            "bahan_match": "",
            "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
            "meta_kategori": meta.get('kategori', 'umum'),
            "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
            "label_ai": "TIDAK",
            "pesan_sistem": pesan if i == 0 else ""
        })
    return hasil

# --- ROUTES ---
@app.route('/cari', methods=['POST'])
def cari_resep():
    data_masuk = request.get_json()
    input_bahan_raw = data_masuk.get('bahan', '')
    input_rasa = data_masuk.get('rasa', 'Semua')
    input_kategori = data_masuk.get('kategori', 'Semua')
    
    jam = datetime.datetime.now().hour
    waktu_server = "malam"
    if 5 <= jam < 11: waktu_server = "pagi"
    elif 11 <= jam < 15: waktu_server = "siang"
    elif 15 <= jam < 19: waktu_server = "sore"

    database_menu = muat_json(NAMA_FILE_DB)
    
    # Pre-processing
    list_bahan_user = []
    user_staples = set()
    filter_keyword_kategori = None 
    
    raw_split = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', input_bahan_raw) if x]
    
    for b in raw_split:
        b_bersih = normalisasi_alay(b)
        if b_bersih in ['minuman', 'minum']:
            filter_keyword_kategori = 'minuman'; continue 
        elif b_bersih in ['makanan', 'makan']:
            filter_keyword_kategori = 'makanan'; continue
            
        b_final = CACHE_KAMUS.get(b_bersih, b_bersih)
        list_bahan_user.append(b_final)
        if b_final in BAHAN_POKOK: user_staples.add(b_final)

    target_kategori = filter_keyword_kategori if filter_keyword_kategori else input_kategori

    # --- MODIFIKASI PENTING DI SINI ---
    # Jika input kosong -> Panggil PERSONALIZED recommendation
    if not list_bahan_user and not filter_keyword_kategori:
        return jsonify(get_personalized_recommendations(database_menu))

    ai_suggestion = tanya_ai(list_bahan_user, waktu_server)
    hasil_sementara = []
    
    for menu in database_menu:
        # 1. Filter Rasa
        if input_rasa != "Semua" and menu.get('rasa', '').lower() != input_rasa.lower(): continue
        
        # 2. Filter Kategori
        meta = menu.get('metadata', {})
        menu_kat = meta.get('kategori', 'umum').lower()
        if target_kategori != "Semua":
            t = target_kategori.lower()
            if t == "makanan" and menu_kat == "minuman": continue
            elif t == "minuman" and menu_kat != "minuman": continue
            elif t == "camilan" and menu_kat != "camilan": continue

        # 3. Strict Filter
        semua_bahan_resep = menu.get('bahan', [])
        if len(user_staples) > 0:
            present = False
            for b_r in semua_bahan_resep:
                for s in user_staples:
                    if cek_kemiripan(s, b_r.lower()): present = True; break
                if present: break
            if not present: continue 

        # 4. Scoring
        skor = 0
        bahan_cocok_list = []
        for b_resep in semua_bahan_resep:
            br = b_resep.lower()
            for bu in list_bahan_user:
                if cek_kemiripan(bu, br): skor += 1; bahan_cocok_list.append(b_resep); break 
        
        if not list_bahan_user and filter_keyword_kategori: skor = 1

        if skor > 0:
            relevansi = skor / len(list_bahan_user) if list_bahan_user else 1.0
            is_ai = (ai_suggestion and ai_suggestion.startswith(menu['nama']))
            hasil_sementara.append({
                "nama": menu['nama'],
                "rasa": menu.get('rasa', 'Umum'),
                "skor": skor, "relevansi": relevansi, "is_ai": is_ai,
                "bahan_lengkap": "|".join(semua_bahan_resep),
                "bahan_match": "|".join(bahan_cocok_list),
                "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
                "meta_kategori": meta.get('kategori', 'umum'),
                "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
                "label_ai": "YA" if is_ai else "TIDAK",
                "pesan_sistem": ""
            })

    # Jika hasil kosong setelah search -> Tetap pakai PERSONALIZED
    if not hasil_sementara:
         return jsonify(get_personalized_recommendations(database_menu))

    hasil_final = sorted(hasil_sementara, key=lambda x: (x['is_ai'], x['relevansi'], x['skor']), reverse=True)
    return jsonify(hasil_final[:15])

@app.route('/catat-pilihan', methods=['POST'])
def catat_pilihan():
    data = request.get_json()
    record_baru = {
        "input_user": data.get('input_user'),
        "rasa_dipilih": data.get('rasa_input'),
        "menu_dipilih": data.get('menu_dipilih'),
        "waktu_akses": data.get('waktu_akses'),
        "timestamp": data.get('timestamp')
    }
    
    history = muat_json(NAMA_FILE_LOG)
    if not isinstance(history, list): history = []
    
    history.append(record_baru)
    with open(NAMA_FILE_LOG, 'w') as f:
        json.dump(history, f, indent=2)
    return jsonify({"status": "sukses"})

@app.route('/tambah', methods=['POST'])
def tambah_resep():
    data_masuk = request.get_json()
    nama_baru = data_masuk.get('nama')
    rasa_baru = data_masuk.get('rasa')
    bahan_raw = data_masuk.get('bahan')
    
    if not nama_baru or not bahan_raw: return jsonify({"status": "gagal"}), 400
    
    list_bahan_bersih = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', bahan_raw) if x]
    menu_baru = {
        "nama": nama_baru,
        "rasa": rasa_baru,
        "bahan": list_bahan_bersih,
        "metadata": {"waktu": ["kapanpun"], "kategori": "umum", "sifat": ["umum"]}
    }
    
    db = muat_json(NAMA_FILE_DB)
    db.append(menu_baru)
    simpan_database(db)
    return jsonify({"status": "sukses"})

if __name__ == '__main__':
    print("Server AI FoodAssistant (Neural Network Activated) Berjalan...")
    app.run(debug=True, port=5000)