import json

# Config Default Metadata
METADATA_DEFAULT = {
    "waktu": ["kapanpun"],      # pagi, siang, malam, kapanpun
    "kategori": "berat",        # berat, ringan, camilan, minuman
    "sifat": ["umum"]           # kuah, goreng, pedas, hangat, dingin
}

def update_json():
    try:
        # Baca file lama
        with open('resep.json', 'r') as f:
            data = json.load(f)
        
        jumlah_update = 0
        
        # Loop setiap resep
        for menu in data:
            # Cek apakah sudah punya metadata? Jika belum, tambahkan.
            if "metadata" not in menu:
                menu["metadata"] = METADATA_DEFAULT.copy()
                
                # LOGIKA PINTAR SEDERHANA UNTUK DEFAULT VALUE
                # Biar kita gak manual banget ngeditnya nanti
                nama = menu['nama'].lower()
                
                # Cek Waktu (Sarapan)
                if "bubur" in nama or "nasi uduk" in nama:
                    menu["metadata"]["waktu"] = ["pagi"]
                
                # Cek Kategori (Minuman/Camilan)
                if "es " in nama or "jus " in nama or "teh " in nama:
                    menu["metadata"]["kategori"] = "minuman"
                    menu["metadata"]["sifat"] = ["dingin"]
                elif "pisang" in nama or "roti" in nama or "martabak" in nama:
                    menu["metadata"]["kategori"] = "camilan"
                
                jumlah_update += 1
        
        # Simpan kembali
        with open('resep.json', 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Sukses! {jumlah_update} resep telah diperbarui dengan metadata.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_json()