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
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

app = Flask(__name__)

NAMA_FILE_DB = 'resep.json'
NAMA_FILE_KAMUS = 'kamus.json'
NAMA_FILE_LOG = 'history.json'
NAMA_FILE_MODEL = 'model_cerdas.pkl'
NAMA_FILE_ENCODER = 'encoder_bahan.pkl'
NAMA_FILE_CONFIG_NLP = 'config_nlp.json'

def muat_json(nama_file):
    if not os.path.exists(nama_file): 
        # Return struktur kosong yang aman sesuai tipe file
        if nama_file == NAMA_FILE_CONFIG_NLP:
            return {"kamus_alay": {}, "stopwords": [], "bahan_pokok": [], "keywords_kategori": {}, "keywords_rasa": {}}
        return {} if nama_file == NAMA_FILE_KAMUS else []
        
    try:
        with open(nama_file, 'r') as f: return json.load(f)
    except: return {}

CONFIG_NLP = muat_json(NAMA_FILE_CONFIG_NLP)
KAMUS_ALAY = CONFIG_NLP.get('kamus_alay', {})
STOPWORDS = set(CONFIG_NLP.get('stopwords', []))
BAHAN_POKOK = set(CONFIG_NLP.get('bahan_pokok', []))
KEYWORDS_KATEGORI = CONFIG_NLP.get('keywords_kategori', {})
KEYWORDS_RASA = CONFIG_NLP.get('keywords_rasa', {})
CACHE_KAMUS = muat_json(NAMA_FILE_KAMUS)

# Load Model AI
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
    bahan_user = CACHE_KAMUS.get(bahan_user, bahan_user) # Misal: beras -> nasi
    
    bahan_resep_asli = bahan_resep
    bahan_resep = CACHE_KAMUS.get(bahan_resep, bahan_resep) # Misal: beras -> nasi
    
    if bahan_user == bahan_resep: return True
    
    # Cek Word Boundary (Pecah kata)
    kata_kunci_resep = re.split(r'[,\.\s]+', bahan_resep)
    if bahan_user in kata_kunci_resep: return True
    
    # Cek Fuzzy
    skor = fuzz.token_sort_ratio(bahan_user, bahan_resep)
    if skor >= 80: return True
    
    # Cek Partial (Khusus kata panjang)
    if len(bahan_user) > 3 and (bahan_user in bahan_resep or bahan_user in bahan_resep_asli): 
        return True
        
    return False

# --- LOGIKA REKOMENDASI (PERSONALIZED) ---
def get_personalized_recommendations(database, limit=10, filter_kat="Semua", filter_rasa="Semua", pesan_khusus=""):
    # 1. FILTER DATABASE
    db_filtered = []
    for m in database:
        meta = m.get('metadata', {})
        kat_menu = meta.get('kategori', 'umum').lower()
        if filter_kat != "Semua":
            target = filter_kat.lower()
            if target == "makanan" and kat_menu == "minuman": continue
            elif target == "minuman" and kat_menu != "minuman": continue
            elif target == "camilan" and kat_menu != "camilan": continue
        
        if filter_rasa != "Semua" and m.get('rasa', '').lower() != filter_rasa.lower():
            continue
        db_filtered.append(m)

    # UBAH PESAN DISINI (Jika filter tidak menemukan hasil apapun)
    if not db_filtered:
        return [{
            "nama": "Maaf...", "rasa": "-", "skor": 0, "relevansi": 0, "is_ai": False,
            "bahan_lengkap": "-", "bahan_match": "", "meta_waktu": "-", "meta_kategori": "-", "meta_sifat": "-", 
            "label_ai": "TIDAK",
            "pesan_sistem": f"Menu yang kamu cari tidak ada untuk kategori '{filter_kat}' & rasa '{filter_rasa}'."
        }]

    history = muat_json(NAMA_FILE_LOG)
    hasil_personal = []
    nama_personal = set()

    # 2. AMBIL DARI HISTORY
    if isinstance(history, list) and len(history) > 0:
        list_menu_dipilih = [h.get('menu_dipilih') for h in history if h.get('menu_dipilih')]
        counter_menu = Counter(list_menu_dipilih)
        top_menu_names = [m[0] for m in counter_menu.most_common(10)]
        
        for menu in db_filtered:
            if menu['nama'] in top_menu_names:
                meta = menu.get('metadata', {})
                hasil_personal.append({
                    "nama": menu['nama'], "rasa": menu.get('rasa', 'Umum'),
                    "skor": 0, "relevansi": 1.0, "is_ai": True,
                    "bahan_lengkap": "|".join(menu.get('bahan', [])),
                    "bahan_match": "(Sesuai Selera)",
                    "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
                    "meta_kategori": meta.get('kategori', 'umum'),
                    "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
                    "label_ai": "YA", "pesan_sistem": ""
                })
                nama_personal.add(menu['nama'])
                if len(hasil_personal) >= 5: break

    # 3. ISI SISA DENGAN RANDOM
    sisa_slot = limit - len(hasil_personal)
    if sisa_slot > 0:
        db_sisa = [m for m in db_filtered if m['nama'] not in nama_personal]
        if db_sisa:
            tambahan_random = random.sample(db_sisa, min(len(db_sisa), sisa_slot))
            for menu in tambahan_random:
                meta = menu.get('metadata', {})
                hasil_personal.append({
                    "nama": menu['nama'], "rasa": menu.get('rasa', 'Umum'),
                    "skor": 0, "relevansi": 0, "is_ai": False,
                    "bahan_lengkap": "|".join(menu.get('bahan', [])),
                    "bahan_match": "",
                    "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
                    "meta_kategori": meta.get('kategori', 'umum'),
                    "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
                    "label_ai": "TIDAK", "pesan_sistem": ""
                })

    # 4. SET PESAN SISTEM (UBAH PESAN GIBBERISH DISINI)
    if hasil_personal:
        if pesan_khusus:
            # Ini yang diganti (saat input gibberish/ngawur)
            hasil_personal[0]['pesan_sistem'] = "Menu yang kamu cari tidak ada. Berikut rekomendasi makanan/minuman untukmu:"
        else:
            kategori_msg = filter_kat if filter_kat != "Semua" else "makanan/minuman"
            hasil_personal[0]['pesan_sistem'] = f"Rekomendasi {kategori_msg} pilihan untukmu:"
        
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

# --- LOGIKA ACTIVE LEARNING ---
def generate_base_knowledge(database, jumlah=500):
    # Fungsi ini membuat "Pengetahuan Dasar" agar AI tidak lupa resep lain
    # saat terlalu fokus belajar dari history user.
    dataset = []
    for _ in range(jumlah):
        target_resep = random.choice(database)
        bahan_asli = target_resep['bahan']
        # Simulasi input user (ambil sebagian bahan acak)
        if not bahan_asli: continue
        jumlah_input = random.randint(1, len(bahan_asli))
        input_user = random.sample(bahan_asli, jumlah_input)
        
        meta_waktu = target_resep.get('metadata', {}).get('waktu', ['kapanpun'])
        waktu_sim = random.choice(meta_waktu)
        if waktu_sim == 'kapanpun': waktu_sim = random.choice(['pagi', 'siang', 'malam'])
        
        dataset.append({
            "bahan_input": input_user,
            "waktu": waktu_sim,
            "target_nama": target_resep['nama']
        })
    return pd.DataFrame(dataset)

def latih_ulang_otak():
    global OTAK_AI, ENCODER_AI, VOCAB_AI
    
    print("[TRAINING] Memulai proses belajar ulang...")
    
    # 1. AMBIL DATA UMUM (BASE KNOWLEDGE)
    db_resep = muat_json(NAMA_FILE_DB)
    df_base = generate_base_knowledge(db_resep, jumlah=500)
    
    # 2. AMBIL DATA PENGALAMAN (HISTORY)
    history = muat_json(NAMA_FILE_LOG)
    df_history = pd.DataFrame()
    
    if isinstance(history, list) and len(history) > 0:
        data_hist = []
        for h in history:
            # Kita konversi format history agar sama dengan format training
            # Input user di history string "nasi, telur", harus diubah jadi list ['nasi', 'telur']
            raw_input = h.get('input_user', '')
            list_input = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', raw_input) if x]
            
            # Abaikan jika input kosong
            if not list_input: continue
                
            data_hist.append({
                "bahan_input": list_input,
                "waktu": h.get('waktu_akses', 'siang'), # Ambil konteks waktu asli user
                "target_nama": h.get('menu_dipilih')    # Ini kunci! AI belajar pilihan user
            })
        
        if data_hist:
            df_history = pd.DataFrame(data_hist)
            print(f"[TRAINING] Ditemukan {len(df_history)} data pengalaman baru dari user.")
    
    # 3. GABUNGKAN (Masa Lalu + Masa Kini)
    # Kita beri bobot lebih pada history? Untuk sekarang kita gabung biasa dulu.
    if not df_history.empty:
        df_final = pd.concat([df_base, df_history], ignore_index=True)
    else:
        df_final = df_base
        
    # 4. PROSES VECTORIZATION (Sama seperti otak_ai.py)
    mlb = MultiLabelBinarizer()
    X_bahan = mlb.fit_transform(df_final['bahan_input'])
    
    map_waktu = {'pagi': 0, 'siang': 1, 'sore': 2, 'malam': 3}
    # Handle data kotor/missing pada waktu
    X_waktu = df_final['waktu'].map(map_waktu).fillna(1).values.reshape(-1, 1)
    
    X_train = np.hstack((X_bahan, X_waktu))
    y_train = df_final['target_nama']
    
    # 5. LATIH NEURAL NETWORK
    # Kita gunakan parameter warm_start=False agar dia belajar dari nol gabungan data
    model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    model.fit(X_train, y_train)
    
    # 6. SIMPAN & UPDATE MEMORI AKTIF
    joblib.dump(model, NAMA_FILE_MODEL)
    joblib.dump(mlb, NAMA_FILE_ENCODER)
    
    # Update variabel global agar server langsung pintar tanpa restart
    OTAK_AI = model
    ENCODER_AI = mlb
    VOCAB_AI = set(mlb.classes_)
    
    return f"Berhasil dilatih dengan {len(df_final)} data (Base + History)."

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
    
    list_bahan_user = []
    user_staples = set()
    nlp_kategori = None
    nlp_rasa = None
    
    raw_split = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', input_bahan_raw) if x]
    
    for b in raw_split:
        b_bersih = normalisasi_alay(b)
        
        # Cek Stopwords
        if b_bersih in STOPWORDS: continue
        
        # Cek Keyword Kategori
        if b_bersih in KEYWORDS_KATEGORI:
            nlp_kategori = KEYWORDS_KATEGORI[b_bersih]; continue
        
        # Cek Keyword Rasa
        if b_bersih in KEYWORDS_RASA:
            nlp_rasa = KEYWORDS_RASA[b_bersih]; continue
            
        b_final = CACHE_KAMUS.get(b_bersih, b_bersih)
        list_bahan_user.append(b_final)
        if b_final in BAHAN_POKOK: user_staples.add(b_final)

    target_kategori = nlp_kategori if nlp_kategori else input_kategori
    target_rasa = nlp_rasa if nlp_rasa else input_rasa

    # KONDISI 1: INPUT MEMANG KOSONG (User cuma klik cari / main dropdown)
    # raw_split kosong artinya user tidak mengetik apa-apa
    if not raw_split:
        return jsonify(get_personalized_recommendations(database_menu, 10, target_kategori, target_rasa))

    # KONDISI 2: INPUT ADA, TAPI HABIS DIMAKAN STOPWORDS/KEYWORDS (User ketik "aku mau minum")
    # list_bahan_user kosong, tapi raw_split ada isinya
    if not list_bahan_user:
        return jsonify(get_personalized_recommendations(database_menu, 10, target_kategori, target_rasa))

    # --- PENCARIAN DIMULAI ---
    ai_suggestion = tanya_ai(list_bahan_user, waktu_server)
    hasil_sementara = []
    
    for menu in database_menu:
        # Filter Rasa
        if target_rasa != "Semua" and menu.get('rasa', '').lower() != target_rasa.lower(): continue
        
        # Filter Kategori
        meta = menu.get('metadata', {})
        menu_kat = meta.get('kategori', 'umum').lower()
        if target_kategori != "Semua":
            t = target_kategori.lower()
            if t == "makanan" and menu_kat == "minuman": continue
            elif t == "minuman" and menu_kat != "minuman": continue
            elif t == "camilan" and menu_kat != "camilan": continue

        # Strict Filter
        semua_bahan_resep = menu.get('bahan', [])
        if len(user_staples) > 0:
            present = False
            for b_r in semua_bahan_resep:
                for s in user_staples:
                    if cek_kemiripan(s, b_r.lower()): present = True; break
                if present: break
            if not present: continue 

        # Scoring
        skor = 0
        bahan_cocok_list = []
        for b_resep in semua_bahan_resep:
            br = b_resep.lower()
            for bu in list_bahan_user:
                if cek_kemiripan(bu, br): skor += 1; bahan_cocok_list.append(b_resep); break 
        
        if skor > 0:
            relevansi = skor / len(list_bahan_user)
            is_ai = (ai_suggestion and ai_suggestion.startswith(menu['nama']))
            hasil_sementara.append({
                "nama": menu['nama'], "rasa": menu.get('rasa', 'Umum'),
                "skor": skor, "relevansi": relevansi, "is_ai": is_ai,
                "bahan_lengkap": "|".join(semua_bahan_resep),
                "bahan_match": "|".join(bahan_cocok_list),
                "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
                "meta_kategori": meta.get('kategori', 'umum'),
                "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
                "label_ai": "YA" if is_ai else "TIDAK", "pesan_sistem": ""
            })

    # KONDISI 3: GIBBERISH / TIDAK ADA HASIL (Pencarian Gagal Total)
    if not hasil_sementara:
         pesan_bingung = "Menu yang kamu cari tidak ada. Berikut rekomendasi makanan/minuman lainnya untukmu:"
         return jsonify(get_personalized_recommendations(database_menu, 10, target_kategori, target_rasa, pesan_bingung))

    hasil_final = sorted(hasil_sementara, key=lambda x: (x['is_ai'], x['relevansi'], x['skor']), reverse=True)
    return jsonify(hasil_final[:15])

@app.route('/latih-ulang', methods=['GET', 'POST'])
def trigger_training():
    try:
        pesan = latih_ulang_otak()
        return jsonify({"status": "sukses", "pesan": pesan})
    except Exception as e:
        return jsonify({"status": "error", "pesan": str(e)}), 500
    
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
    
    # Ambil data dasar
    nama_baru = data_masuk.get('nama')
    rasa_baru = data_masuk.get('rasa')
    bahan_raw = data_masuk.get('bahan')
    
    # Ambil data Metadata (BARU)
    # Jika user tidak kirim (misal pakai aplikasi versi lama), pakai default
    kategori_baru = data_masuk.get('kategori', 'makanan') 
    waktu_baru = data_masuk.get('waktu', 'kapanpun').lower()
    
    if not nama_baru or not bahan_raw: 
        return jsonify({"status": "gagal", "pesan": "Data nama/bahan kosong"}), 400
    
    # Bersihkan bahan
    list_bahan_bersih = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', bahan_raw) if x]
    
    # Bentuk struktur data lengkap
    menu_baru = {
        "nama": nama_baru,
        "rasa": rasa_baru,
        "bahan": list_bahan_bersih,
        "metadata": {
            # Waktu kita simpan sebagai list (sesuai standar json kita)
            "waktu": [waktu_baru], 
            "kategori": kategori_baru,
            "sifat": ["umum"] # Sifat biarkan umum dulu karena belum ada inputnya
        }
    }
    
    db = muat_json(NAMA_FILE_DB)
    db.append(menu_baru)
    simpan_database(db)
    
    # OPSI TAMBAHAN: Latih ulang otak otomatis agar resep baru langsung dikenali?
    # latih_ulang_otak() 
    
    return jsonify({"status": "sukses"})

if __name__ == '__main__':
    print("Server AI FoodAssistant (Neural Network Activated) Berjalan...")
    app.run(debug=True, port=5000)