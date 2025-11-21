import json
import os
import re
from flask import Flask, request, jsonify
from thefuzz import fuzz

app = Flask(__name__)
NAMA_FILE_DB = 'resep.json'
NAMA_FILE_KAMUS = 'kamus.json'
NAMA_FILE_LOG = 'history.json'

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

def normalisasi_alay(teks):
    """
    Fungsi ini bertugas membersihkan 'sampah' input user
    sebelum dibaca oleh algoritma pencocokan.
    Contoh: 'n4siii' -> 'nasi'
    """
    if not teks: return ""
    
    teks_bersih = teks.lower()
    
    # TAHAP 1: Leet Speak (Angka jadi Huruf)
    # Kita ganti karakter alay satu per satu
    for alay, normal in KAMUS_ALAY.items():
        teks_bersih = teks_bersih.replace(alay, normal)
        
    # TAHAP 2: Hapus Huruf Berulang Berlebihan (Regex)
    # Contoh: "nasiii" -> "nasi", "bangeeet" -> "banget"
    # Logika: Jika ada huruf diulang lebih dari 2x, jadikan 1x (kecuali kasus khusus)
    # Pola (pattern) ini mencari karakter (.) yang muncul berulang (\1+)
    teks_bersih = re.sub(r'(.)\1+', r'\1', teks_bersih)
    
    return teks_bersih

CACHE_KAMUS = muat_json(NAMA_FILE_KAMUS)
print(f"[INFO] Kamus berhasil dimuat: {len(CACHE_KAMUS)} kata sinonim.")

# --- FUNGSI PENCARI CERDAS (FUZZY LOGIC) ---
# --- 2. LOGIKA PENCARIAN CERDAS (REVISI TOTAL) ---
def cek_kemiripan(bahan_user, bahan_resep):
    # A. Normalisasi ALAY dulu! (Langkah Baru)
    bahan_user_asli = bahan_user
    bahan_user = normalisasi_alay(bahan_user) 
    
    # B. Cek Kamus Sinonim (kamus.json)
    # Misal: user ketik "cabe" -> normal "cabe" -> kamus ubah jadi "cabai"
    bahan_user = CACHE_KAMUS.get(bahan_user, bahan_user)
    
    # C. Exact Match (Cek Langsung)
    if bahan_user == bahan_resep:
        return True

    # D. Word Boundary Check (Cek per Kata) 
    # Mencegah "mi" cocok dengan "minyak"
    kata_kunci_resep = re.split(r'[,\.\s]+', bahan_resep)
    if bahan_user in kata_kunci_resep:
        return True
        
    # E. Fuzzy Match (Typo Tolerance)
    # KITA TURUNKAN THRESHOLD KE 80
    # Alasannya: Setelah dinormalisasi, teks sudah lebih bersih.
    # "nsi" vs "nasi" itu rasionya 86. Kalau threshold 90 dia gagal.
    # "bwang" vs "bawang" rasionya 91.
    skor = fuzz.token_sort_ratio(bahan_user, bahan_resep)
    
    if skor >= 80: 
        return True
        
    # F. Partial Match Khusus Kata Panjang (>3 huruf)
    # Untuk menangani "stroberi" di dalam "selai stroberi"
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
                meta = menu.get('metadata', {})
                
                # Ambil data, jika list maka join pakai '|', jika string biarkan
                waktu_str = "|".join(meta.get('waktu', ['kapanpun']))
                kategori_str = meta.get('kategori', 'umum')
                sifat_str = "|".join(meta.get('sifat', ['umum']))

                hasil_sementara.append({
                    "nama": menu['nama'],
                    "rasa": menu.get('rasa', 'Umum'),
                    "skor": skor,
                    "bahan_lengkap": "|".join(semua_bahan_resep),
                    "bahan_match": "|".join(bahan_cocok_list),
                    
                    # Metadata
                    "meta_waktu": waktu_str,
                    "meta_kategori": kategori_str,
                    "meta_sifat": sifat_str
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
        "bahan": list_bahan_bersih,
        "metadata": {"waktu": ["kapanpun"], "kategori": "umum", "sifat": ["umum"]}
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

# --- 4. FITUR MEMORI (LOGGING) ---
NAMA_FILE_LOG = 'history.json' # Buku harian AI

@app.route('/catat-pilihan', methods=['POST'])
def catat_pilihan():
    data = request.get_json()
    
    # Data yang akan disimpan untuk pelatihan AI nanti
    record_baru = {
        "input_user": data.get('input_user'),
        "rasa_dipilih": data.get('rasa_input'),
        "menu_dipilih": data.get('menu_dipilih'),
        "waktu_akses": data.get('waktu_akses'), # Pagi/Siang/Malam
        "timestamp": data.get('timestamp')
    }
    
    # Simpan ke history.json
    history = muat_json(NAMA_FILE_LOG)
    if isinstance(history, list) == False: history = [] # Jaga-jaga kalau error
    
    history.append(record_baru)
    
    with open(NAMA_FILE_LOG, 'w') as f:
        json.dump(history, f, indent=2)
        
    print(f"[BELAJAR] User memilih: {record_baru['menu_dipilih']}")
    return jsonify({"status": "sukses", "pesan": "Pilihan dicatat!"})

if __name__ == '__main__':
    print("Server AI FoodAssistant Berjalan...")
    app.run(debug=True, port=5000)