import json
import os
import re
import datetime
import joblib
import numpy as np
import pandas as pd
import random
from flask import Flask, request, jsonify
from collections import Counter
from thefuzz import fuzz
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from groq import Groq

app = Flask(__name__)


    
NAMA_FILE_DB = 'resep.json'
NAMA_FILE_KAMUS = 'kamus.json'
NAMA_FILE_LOG = 'history.json'
NAMA_FILE_MODEL = 'model_cerdas.pkl'
NAMA_FILE_ENCODER = 'encoder_bahan.pkl'
NAMA_FILE_CONFIG_NLP = 'config_nlp.json'
NAMA_FILE_CACHE_QUERY = 'cache_query.json'

def muat_json(nama_file):
    if not os.path.exists(nama_file): 
        # Return struktur kosong yang aman sesuai tipe file
        if nama_file == NAMA_FILE_CONFIG_NLP:
            return {"kamus_alay": {}, "stopwords": [], "bahan_pokok": [], "keywords_kategori": {}, "keywords_rasa": {}}
        return {} if nama_file == NAMA_FILE_KAMUS else []
        
    try:
        with open(nama_file, 'r') as f: return json.load(f)
    except: return {}

CACHE_QUERY = muat_json(NAMA_FILE_CACHE_QUERY)
if isinstance(CACHE_QUERY, list):
    CACHE_QUERY = {}

def simpan_cache_query():
    try:
        with open(NAMA_FILE_CACHE_QUERY, 'w') as f:
            json.dump(CACHE_QUERY, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan cache: {e}")

API_KEY = muat_json('API_KEY.json')
GROQ_API_KEY = API_KEY.get("groq_api_key", "") 
try:
    if not GROQ_API_KEY:
        raise Exception("API Key tidak ditemukan di API_KEY.json")
        
    client_llm = Groq(api_key=GROQ_API_KEY)
    USE_LLM = True
    print("[INFO] LLM Activated (Groq/Llama-3.3-70b)")
except Exception as e:
    USE_LLM = False
    print(f"[WARNING] LLM Inactive: {e}")
    
CONFIG_NLP = muat_json(NAMA_FILE_CONFIG_NLP)
KAMUS_ALAY = CONFIG_NLP.get('kamus_alay', {})
STOPWORDS = set(CONFIG_NLP.get('stopwords', []))
BAHAN_POKOK = set(CONFIG_NLP.get('bahan_pokok', []))
KEYWORDS_KATEGORI = CONFIG_NLP.get('keywords_kategori', {})
KEYWORDS_RASA = CONFIG_NLP.get('keywords_rasa', {})
KEYWORDS_WAKTU = CONFIG_NLP.get('keywords_waktu', {})
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
        pattern = r'\b' + re.escape(alay) + r'\b'
        teks_bersih = re.sub(pattern, normal, teks_bersih)
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
def get_personalized_recommendations(database, limit=10, filter_kat="Semua", filter_rasa="Semua", pesan_khusus="", filter_waktu=None, exclude_rasa=None):
    # 1. FILTER DATABASE
    db_filtered = []
    
    target_kat = filter_kat.lower() if filter_kat else "semua"
    target_rasa = filter_rasa.lower() if filter_rasa else "semua"
    target_waktu = filter_waktu.lower() if filter_waktu else None
    ex_target = exclude_rasa.lower() if exclude_rasa else None
    
    for m in database:
        meta = m.get('metadata', {})
        
        kat_menu = meta.get('kategori', 'umum').lower()
        rasa_menu = m.get('rasa', '').lower()
        waktu_menu = [w.lower() for w in meta.get('waktu', ['kapanpun'])]
        nama_menu = m['nama'].lower()
        sifat_menu = [s.lower() for s in meta.get('sifat', [])]
        
        if ex_target:
            if ex_target in rasa_menu: continue
            if ex_target in nama_menu: continue
            if ex_target in sifat_menu: continue
        if target_kat != "semua":
            if target_kat == "makanan" and kat_menu == "minuman": continue
            elif target_kat == "minuman" and kat_menu != "minuman": continue
            elif target_kat == "camilan" and kat_menu != "camilan": continue
        
        if target_rasa != "semua" and rasa_menu != target_rasa:
            continue
        if target_waktu:
            if "kapanpun" not in waktu_menu and target_waktu not in waktu_menu:
                continue
        db_filtered.append(m)

    # UBAH PESAN DISINI (Jika filter tidak menemukan hasil apapun)
    if not db_filtered:
        msg_waktu = f" di waktu '{filter_waktu}'" if filter_waktu else ""
        msg_exclude = f" (tanpa '{exclude_rasa}')" if exclude_rasa else ""
        return [{
            "nama": "Maaf, Menu Tidak Ditemukan", 
            "rasa": "-", 
            "skor": 0, 
            "relevansi": 0, 
            "is_ai": False,
            "bahan_lengkap": "-", "bahan_match": "", 
            "meta_waktu": "-", "meta_kategori": "-", "meta_sifat": "-", 
            "label_ai": "TIDAK",
            "pesan_sistem": f"Tidak ada menu yang cocok untuk kategori '{filter_kat}', rasa '{filter_rasa}'{msg_waktu}{msg_exclude}. Coba ubah filter."
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
                    "bahan_match": "(Favoritmu)",
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
            hasil_personal[0]['pesan_sistem'] = pesan_khusus
        else:
            kategori_msg = filter_kat if filter_kat != "Semua" else "makanan/minuman"
            waktu_msg = f" ({filter_waktu})" if filter_waktu else ""
            ex_msg = f" [Tanpa {exclude_rasa}]" if exclude_rasa else ""
            hasil_personal[0]['pesan_sistem'] = f"Rekomendasi {kategori_msg}{waktu_msg}{ex_msg} pilihan untukmu:"
        
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
    
    data_hist = []
    
    if isinstance(history, list) and len(history) > 0:
        sekarang = datetime.now()
        for h in history:
            # Kita konversi format history agar sama dengan format training
            # Input user di history string "nasi, telur", harus diubah jadi list ['nasi', 'telur']
            raw_input = h.get('input_user', '')
            list_input = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', raw_input) if x]
            
            # Abaikan jika input kosong
            if not list_input: continue
                
            jumlah_ulangan = 1
            
            try:
                tgl_str = h.get('timestamp') # Contoh: "2025-11-21 09:24:47"
                if tgl_str:
                    waktu_akses = datetime.strptime(tgl_str, "%Y-%m-%d %H:%M:%S")
                    selisih_hari = (sekarang - waktu_akses).days
                    
                    if selisih_hari < 1:     # Data Hari Ini (Sangat Relevan)
                        jumlah_ulangan = 5   # Pelajari 5 kali!
                    elif selisih_hari < 3:   # Data 3 Hari Terakhir
                        jumlah_ulangan = 3   # Pelajari 3 kali
                    elif selisih_hari < 7:   # Data Seminggu Terakhir
                        jumlah_ulangan = 2   # Pelajari 2 kali
                    elif selisih_hari > 30:  # Data > Sebulan
                         jumlah_ulangan = 1
            except Exception as e:
                jumlah_ulangan = 1

            record = {
                "bahan_input": list_input,
                "waktu": h.get('waktu_akses', 'siang'),
                "target_nama": h.get('menu_dipilih')
            }
            
            for _ in range(jumlah_ulangan):
                data_hist.append(record)
        
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

def cek_gibberish(kata):
    if len(kata) > 20: return True
    if not re.search(r'[aeiouy]', kata): return True # Gak ada vokal
    if re.search(r'(.)\1{2,}', kata): return True # Ada huruf diulang 3x (aaapa)
    return False

def smart_filter_input(teks_raw):
    if not teks_raw: return "GIBBERISH", ""
    
    # Normalisasi
    teks = normalisasi_alay(teks_raw)
    kata_kata = [k.strip() for k in re.split(r'[,\.\s\n\?]+', teks) if k]

    # gabung semua knowledge base menjadi satu set besar
    vocab_known = set()
    vocab_known.update(KEYWORDS_RASA.keys())
    vocab_known.update(KEYWORDS_KATEGORI.keys()) 
    vocab_known.update(KEYWORDS_WAKTU.keys()) 
    vocab_known.update(CACHE_KAMUS.keys())  
    vocab_known.update(BAHAN_POKOK)      
    if VOCAB_AI: vocab_known.update(VOCAB_AI)    
    
    anchors_found = []      
    potential_context = []  
    
    for k in kata_kata:
        k_lower = k.lower()
        if k_lower in STOPWORDS: continue
        
        # Cek Anchor
        if k_lower in vocab_known or k_lower in KEYWORDS_RASA.values():
            anchors_found.append(k_lower)
        else:
            if not cek_gibberish(k_lower):
                potential_context.append(k_lower) 
    
    # --- DECISION LOGIC ---
    # SKENARIO 1: Anchor Dominant ("fhshdfd nasi")
    if anchors_found:
        input_bersih = " ".join(anchors_found)
        print(f"[SMART FILTER] Anchor ditemukan: '{input_bersih}'. Mengabaikan sampah/konteks lain.")
        return "LOCAL", input_bersih
        
    # SKENARIO 2: Context Only ("sakit flu", "diet")
    if potential_context:
        print(f"[SMART FILTER] Konteks terdeteksi tanpa anchor: {potential_context}. Pass ke LLM.")
        return "LLM", teks_raw
        
    # SKENARIO 3: Total Gibberish ("sjdjfoidsj")
    print(f"[SMART FILTER] Input sampah terdeteksi: '{teks_raw}'. Reject.")
    return "GIBBERISH", ""

def buat_fingerprint_semantik(teks_raw):
    teks = normalisasi_alay(teks_raw)
    
    kata_kata = [k.strip() for k in re.split(r'[,\.\s\n\?]+', teks) if k]
    vocab_known = set()
    vocab_known.update(KEYWORDS_RASA.keys())
    vocab_known.update(KEYWORDS_KATEGORI.keys())
    vocab_known.update(KEYWORDS_WAKTU.keys())
    vocab_known.update(CACHE_KAMUS.keys())
    vocab_known.update(BAHAN_POKOK)
    if VOCAB_AI: vocab_known.update(VOCAB_AI) 
    
    sampah_extra = {"kira-kira", "dong", "sih", "nih", "tuh", "ya", "apa", "enak", "enaknya", "rekomendasi", "pengen", "mau"}
    
    list_valid = []     
    list_potensial = [] 
    
    for k in kata_kata:
        k_lower = k.lower()
        if k_lower in STOPWORDS or k_lower in sampah_extra: continue
        
        if k_lower in vocab_known or k_lower in KEYWORDS_RASA.values() or k_lower in KEYWORDS_KATEGORI.values():
            if k_lower in KEYWORDS_WAKTU: final_word = KEYWORDS_WAKTU[k_lower]
            elif k_lower in KEYWORDS_RASA: final_word = KEYWORDS_RASA[k_lower]
            elif k_lower in KEYWORDS_KATEGORI: final_word = KEYWORDS_KATEGORI[k_lower]
            elif k_lower in CACHE_KAMUS: final_word = CACHE_KAMUS[k_lower]
            else: final_word = k_lower
            
            list_valid.append(final_word)
        else:
            if not cek_gibberish(k_lower):
                list_potensial.append(k_lower)
    
    # --- SMART FILTER ---
    # KONDISI 1: Ada Anchor (Kata Valid)
    # Contoh: "fhshdfd nasi" -> "nasi"
    # Jika kita menemukan minimal 1 kata valid, kita ABAIKAN semua kata potensial/asing.
    # Asumsinya: User typo atau ngetik sampah di sekitar kata kunci utama.
    if list_valid:
        return "|".join(sorted(set(list_valid)))
        
    # KONDISI 2: Tidak Ada Anchor, Tapi Ada Kata Potensial
    if list_potensial:
        return "|".join(sorted(set(list_potensial)))
        
    # KONDISI 3: Semua Sampah / Gibberish
    return None

def analisa_bahasa_natural(teks_user):
    if not USE_LLM: return None

    kunci_cache = buat_fingerprint_semantik(teks_user)
    if not kunci_cache:
        print(f"[AI] Terdeteksi input tidak bermakna/gibberish: '{teks_user}'. Skip LLM.")
        return None
    
    if kunci_cache in CACHE_QUERY:
        print(f"[CACHE] Menggunakan data: {CACHE_QUERY[kunci_cache]}")
        return CACHE_QUERY[kunci_cache]
    
    print(f"[AI] Konteks baru ('{kunci_cache}'), memanggil LLM...")
    
    # Prompt System: Menginstruksikan LLM cara bekerja
    system_prompt = f"""
    Kamu adalah asisten koki AI. Tugasmu adalah mengekstrak entitas dari input user menjadi format JSON.
    
    Database kami memiliki data:
    - Rasa: Pedas, Manis, Gurih, Asam, Segar
    - Kategori: Makanan, Minuman, Camilan
    - Bahan Pokok: {', '.join(list(BAHAN_POKOK))}
    
    Database resep memiliki metadata 'sifat': [kuah, goreng, bakar, tumis, basah, kering, hangat, dingin].

    Instruksi PENTING:
    1. Identifikasi 'bahan' (array string). Jika user menyebut 'flu' atau 'sakit', sarankan bahan seperti 'jahe', 'sup', 'ayam'.
    2. Identifikasi 'rasa' (string). Default 'Semua' jika tidak disebut.
    3. Identifikasi 'kategori'.
       - Jika ada kata "makan", "laper", "berat" -> kategori: "Makanan".
       - Jika ada kata "minum", "haus", "segar" -> kategori: "Minuman".
       - Jika ada kata "ngemil", "snack" -> kategori: "Camilan".
    4. Jika user meminta rekomendasi tanpa bahan (misal: "pengen yang anget"), cari bahan implisit yang cocok.
    5. Identifikasi 'sifat': Array string. Ambil dari konteks. 
       - Contoh: "sakit flu", "anget", "sup" -> sifat: ["kuah", "hangat"].
       - Contoh: "kriuk", "garing" -> sifat: ["goreng", "kering"].
    6. Identifikasi 'waktu': Pagi / Siang / Sore / Malam. (Ambil dari konteks seperti 'sarapan', 'dinner').
    7. CEK NEGASI: Jika user berkata "tidak pedas", "jangan manis", "no santan":
       - Masukkan "pedas"/"manis" ke field 'exclude_rasa'.
       - JANGAN masukkan ke field 'rasa'.
    
    Output HARUS JSON murni:
    {{
        "bahan": ["..."],
        "rasa": "...",
        "exclude_rasa": "...", 
        "kategori": "...",
        "waktu": "...",
        "sifat": ["..."]
    }}
    """

    try:
        chat_completion = client_llm.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": teks_user}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        hasil_raw = chat_completion.choices[0].message.content
        hasil_json = json.loads(hasil_raw)
        
        CACHE_QUERY[kunci_cache] = hasil_json
        simpan_cache_query()
        print(f"[CACHE] Disimpan ke ingatan baru.")
        
        return hasil_json
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return None
    
def cek_perlu_llm(teks_raw):
    """
    Menentukan apakah input user butuh pemahaman AI atau cukup keyword matching.
    True = Butuh LLM (Kompleks)
    False = Cukup Lokal (Simple)
    """
    if not teks_raw: return False
    
    teks_bersih = normalisasi_alay(teks_raw)
    kata_kata = [k.strip() for k in re.split(r'[,\.\s\n]+', teks_bersih) if k]
    KATA_NEGASI = {"tidak", "nggak", "gak", "g4k", "jangan", "bukan", "no", "anti", "ga", "stop", "tanpa"}
    
    db_menu = muat_json(NAMA_FILE_DB)
    vocab_bahan = set()
    for menu in db_menu:
        for b in menu.get('bahan', []):
            vocab_bahan.add(b.lower())
            
    vocab_rasa = set([k.lower() for k in KEYWORDS_RASA.keys()])
    vocab_kategori = set([k.lower() for k in KEYWORDS_KATEGORI.keys()])
    vocab_waktu = set([k.lower() for k in KEYWORDS_WAKTU.keys()])
    vocab_kamus = set([k.lower() for k in CACHE_KAMUS.keys()]) # kata asal (misal: 'endog')
    
    skor_asing = 0
    kata_asing = []
    
    for kata in kata_kata:
        if kata in STOPWORDS: continue
        
        # Cek apakah kata ini dikenali sebagai entity database?
        is_known = (
            kata in vocab_bahan or 
            kata in vocab_rasa or 
            kata in vocab_kategori or
            kata in vocab_waktu or
            kata in vocab_kamus or
            kata in BAHAN_POKOK or
            kata in KATA_NEGASI
        )
        
        if not is_known:
            # Jika kata tidak dikenal (misal: "flu", "anget", "diet", "malam"), hitung!
            # Pengecualian: angka/tanda baca
            if not kata.isdigit() and len(kata) > 1:
                skor_asing += 1
                kata_asing.append(kata)

    # Jika ada lebih dari 0 kata asing yang bermakna, gunakan LLM untuk memahaminya.
    # Contoh: "Ayam pedas" -> Asing 0 -> Local
    # Contoh: "Ayam buat orang sakit" -> Asing 2 (buat, sakit) -> LLM
    if skor_asing > 0:
        print(f"[ROUTER] Terdeteksi konteks kompleks ({kata_asing}) -> Switch to LLM.")
        return True
    else:
        print(f"[ROUTER] Input simple/to-the-point -> Switch to Local Logic.")
        return False
    
# --- ROUTES ---
@app.route('/cari', methods=['POST'])
def cari_resep():
    data_masuk = request.get_json()
    raw_input = data_masuk.get('bahan', '') 
    
    target_rasa = data_masuk.get('rasa', 'Semua')
    target_kategori = data_masuk.get('kategori', 'Semua')
    target_waktu = None
    target_sifat = []
    exclude_rasa = None
    list_bahan_user = []
    
    # --- PROSES LLM ---
    butuh_llm = cek_perlu_llm(raw_input)
    pake_llm_sukses = False
    
    aksi, data_bersih = smart_filter_input(raw_input)
    if aksi == "GIBBERISH":
        return jsonify(get_personalized_recommendations(
            muat_json(NAMA_FILE_DB), 10, target_kategori, target_rasa, 
            pesan_khusus="Maaf, saya tidak mengerti inputmu. Coba masukkan nama bahan makanan yang jelas."
        ))

    elif aksi == "LOCAL":
        raw_input = data_bersih 
        butuh_llm = False 
        
    elif aksi == "LLM":
        butuh_llm = True
        
    if butuh_llm:
        print(f"[AI] Menganalisa konteks: '{raw_input}'...")
        hasil_analisa = analisa_bahasa_natural(raw_input)
        
        if hasil_analisa:
            print(f"[AI] Hasil Pemahaman: {hasil_analisa}")
            pake_llm_sukses = True
            
            # Ambil Bahan
            if hasil_analisa.get('bahan'):
                list_bahan_user = [b.lower() for b in hasil_analisa['bahan']]
            
            # Ambil Rasa & Kategori
            if hasil_analisa.get('rasa') and hasil_analisa['rasa'] != "Semua":
                target_rasa = hasil_analisa['rasa']
            if hasil_analisa.get('kategori') and hasil_analisa['kategori'] != "Semua":
                target_kategori = hasil_analisa['kategori']
            if hasil_analisa.get('sifat'):
                target_sifat = [s.lower() for s in hasil_analisa['sifat']]
            if hasil_analisa.get('exclude_rasa'):
                exclude_rasa = hasil_analisa['exclude_rasa']
            if hasil_analisa.get('waktu'):
                waktu_llm = hasil_analisa['waktu'].lower()
                if waktu_llm == "semua":
                    target_waktu = None
                else:
                    target_waktu = waktu_llm

    # --- FALLBACK / KEYWORD MATCHING ---
    if not list_bahan_user and not pake_llm_sukses: 
        KATA_NEGATIF = {"tidak", "nggak", "gak", "g4k", "jangan", "bukan", "no", "anti", "ga"}
        raw_split = [x.strip().lower() for x in re.split(r'[,\.\s\n]+', raw_input) if x]
        skip_indices = set()
        
        for i in range(len(raw_split)):
            word = normalisasi_alay(raw_split[i])
            if word in KATA_NEGATIF:
                if i + 1 < len(raw_split):
                    next_word = normalisasi_alay(raw_split[i+1])
                    if next_word in KEYWORDS_RASA:
                        exclude_rasa = KEYWORDS_RASA[next_word]
                        skip_indices.add(i); skip_indices.add(i+1)
                        print(f"[LOGIC] Negasi Rasa terdeteksi: '{word} {next_word}' -> Exclude: {exclude_rasa}")
                    elif next_word in BAHAN_POKOK:
                         skip_indices.add(i)
                        
        for i, b in enumerate(raw_split):
            if i in skip_indices: continue
            
            b_bersih = normalisasi_alay(b)
            if b_bersih in STOPWORDS: continue
            
            # Deteksi Keyword Spesifik
            if b_bersih in KEYWORDS_KATEGORI:
                target_kategori = KEYWORDS_KATEGORI[b_bersih]; continue
            if b_bersih in KEYWORDS_RASA:
                rasa_ini = KEYWORDS_RASA[b_bersih]
                if exclude_rasa and rasa_ini.lower() == exclude_rasa.lower():
                    continue 
                target_rasa = rasa_ini
                continue
            if b_bersih in KEYWORDS_WAKTU:
                target_waktu = KEYWORDS_WAKTU[b_bersih]; continue
            
            b_final = CACHE_KAMUS.get(b_bersih, b_bersih)
            list_bahan_user.append(b_final)
    
    jam = datetime.datetime.now().hour
    waktu_server = "malam"
    if 5 <= jam < 11: waktu_server = "pagi"
    elif 11 <= jam < 15: waktu_server = "siang"
    elif 15 <= jam < 19: waktu_server = "sore"
    waktu_final = target_waktu if target_waktu else waktu_server
    
    database_menu = muat_json(NAMA_FILE_DB)
    if not list_bahan_user:
        return jsonify(get_personalized_recommendations(
            database_menu, 
            limit=10, 
            filter_kat=target_kategori, 
            filter_rasa=target_rasa, 
            filter_waktu=waktu_final,
            exclude_rasa=exclude_rasa
        ))
        
    user_staples = set()
    for b in list_bahan_user:
        if b in BAHAN_POKOK: user_staples.add(b)

    ai_suggestion = tanya_ai(list_bahan_user, waktu_server)
    hasil_sementara = []
    
    for menu in database_menu:
        meta = menu.get('metadata', {})
        
        # Filter Negatif (Exclude Rasa)
        if exclude_rasa:
            ex_target = exclude_rasa.lower()
            if ex_target in menu.get('rasa', '').lower(): 
                continue
            sifat_menu = [s.lower() for s in meta.get('sifat', [])]
            if ex_target in sifat_menu:
                continue
            if ex_target in menu['nama'].lower():
                continue
        
        # Filter Rasa
        if target_rasa != "Semua" and menu.get('rasa', '').lower() != target_rasa.lower(): 
            continue
        
        # Filter Kategori
        menu_kat = meta.get('kategori', 'umum').lower()
        if target_kategori != "Semua":
            t = target_kategori.lower()
            if t == "makanan" and menu_kat == "minuman": continue
            elif t == "minuman" and menu_kat != "minuman": continue
            elif t == "camilan" and menu_kat != "camilan": continue

        # Filter Sifat (Jika ada dari LLM)
        if target_sifat:
            menu_sifat_list = [s.lower() for s in meta.get('sifat', [])]
            ketemu_sifat = False
            for s_target in target_sifat:
                if s_target in menu_sifat_list:
                    ketemu_sifat = True; break
            if not ketemu_sifat: continue
        
        # Filter Waktu
        menu_waktu_list = [w.lower() for w in meta.get('waktu', ['kapanpun'])]
        if target_waktu and "kapanpun" not in menu_waktu_list:
             if waktu_final not in menu_waktu_list:
                 continue
            
        # Filter Bahan Pokok (Strict)
        semua_bahan_resep = menu.get('bahan', [])
        if len(user_staples) > 0:
            present = False
            for b_r in semua_bahan_resep:
                for s in user_staples:
                    if cek_kemiripan(s, b_r.lower()): present = True; break
                if present: break
            if not present: continue

        # Scoring Kecocokan Bahan
        skor = 0
        bahan_cocok_list = []
        for b_resep in semua_bahan_resep:
            br = b_resep.lower()
            for bu in list_bahan_user:
                if cek_kemiripan(bu, br): skor += 1; bahan_cocok_list.append(b_resep); break 
        
        isValid = False
        if skor > 0: isValid = True
        # Jika context search (tanpa bahan spesifik tapi sifat cocok), anggap valid
        elif target_sifat and not list_bahan_user: isValid = True
        
        if isValid:
            relevansi = skor / len(list_bahan_user) if list_bahan_user else 1.0
            is_ai = (ai_suggestion and ai_suggestion.startswith(menu['nama']))
            if target_sifat: relevansi += 0.5
            
            hasil_sementara.append({
                "nama": menu['nama'], 
                "rasa": menu.get('rasa', 'Umum'),
                "skor": skor,
                "relevansi": relevansi, 
                "is_ai": is_ai,
                "bahan_lengkap": "|".join(semua_bahan_resep),
                "bahan_match": "|".join(bahan_cocok_list),
                "meta_waktu": "|".join(meta.get('waktu', ['kapanpun'])),
                "meta_kategori": meta.get('kategori', 'umum'),
                "meta_sifat": "|".join(meta.get('sifat', ['umum'])),
                "label_ai": "YA" if is_ai else "TIDAK", 
                "pesan_sistem": ""
            })

    # KONDISI 3: GIBBERISH / TIDAK ADA HASIL (Pencarian Gagal Total)
    if not hasil_sementara:
        pesan_bingung = "Menu yang kamu cari tidak ada. Berikut rekomendasi makanan/minuman lainnya untukmu:"
        return jsonify(get_personalized_recommendations(
            database_menu, 
            10, 
            target_kategori, 
            target_rasa, 
            pesan_bingung,
            exclude_rasa=exclude_rasa
        ))

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
            "waktu": [waktu_baru], 
            "kategori": kategori_baru,
            "sifat": ["umum"] # Sifat biarkan umum dulu karena belum ada inputnya
        }
    }
    
    db = muat_json(NAMA_FILE_DB)
    db.append(menu_baru)
    simpan_database(db)
    
    return jsonify({"status": "sukses"})

if __name__ == '__main__':
    print("Server AI FoodAssistant (Neural Network Activated) Berjalan...")
    app.run(debug=True, port=5000)