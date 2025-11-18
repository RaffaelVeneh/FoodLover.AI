# PANDUAN: Membuat FoodLover.AI dengan GUI Modern

## Opsi 1: Menggunakan Qt Framework (RECOMMENDED - Cross-platform & Modern)

### Langkah 1: Install Qt
1. Download Qt Online Installer dari https://www.qt.io/download-qt-installer
2. Install Qt 6.x dengan MSVC 2022 compiler
3. Install Qt Creator IDE

### Langkah 2: Buat Project Qt Widgets Application
1. File -> New Project -> Qt Widgets Application
2. Nama: FoodLoverAI_GUI
3. Base class: QMainWindow

### Langkah 3: Copy kode existing
Copy file-file berikut ke project baru:
- Menu.h / Menu.cpp
- DatabaseMenu.h / DatabaseMenu.cpp
- MesinRekomendasi.h / MesinRekomendasi.cpp

### Langkah 4: Buat UI dengan Qt Designer
Buat 3 form utama:
- MainWindow.ui - Form utama dengan sidebar
- SearchDialog.ui - Dialog pencarian
- AddMenuDialog.ui - Dialog tambah menu

---

## Opsi 2: Menggunakan Dear ImGui (Modern, Lightweight)

### Langkah 1: Setup Dear ImGui
1. Download ImGui dari https://github.com/ocornut/imgui
2. Extract ke folder project Anda
3. Add files berikut ke project:
   - imgui.cpp, imgui_draw.cpp, imgui_tables.cpp, imgui_widgets.cpp
   - imgui_impl_win32.cpp, imgui_impl_dx11.cpp

### Langkah 2: Struktur Project
```
CashierApp/
??? imgui/                  (ImGui library)
??? Menu.h/cpp             (existing)
??? DatabaseMenu.h/cpp     (existing)
??? MesinRekomendasi.h/cpp (existing)
??? MainApp.cpp            (new - main GUI loop)
??? UIComponents.h         (new - UI helper functions)
```

---

## Opsi 3: Windows Forms dengan C++/CLI (Paling Mudah untuk Windows)

### Langkah 1: Buat Project Baru
1. Visual Studio -> Create New Project
2. Pilih "CLR Empty Project (.NET Framework)"
3. Nama: FoodLoverAI_GUI

### Langkah 2: Ubah ke Windows Forms
1. Right-click project -> Properties
2. Configuration Properties -> General
3. Change "Common Language Runtime Support" ke "/clr"

### Langkah 3: Add Windows Forms
1. Right-click project -> Add -> New Item
2. Pilih "Windows Form"
3. Nama: MainForm.h

### Struktur yang akan dibuat:
```
FoodLoverAI_GUI/
??? MainForm.h/.cpp       (Main window)
??? SearchForm.h/.cpp     (Search dialog)
??? AddMenuForm.h/.cpp    (Add menu dialog)
??? NativeWrapper.h       (Bridge between C++/CLI and native)
??? [Copy existing files]
```

---

## REKOMENDASI SAYA: Gunakan Opsi 3 (Windows Forms)

Karena Anda sudah menggunakan Visual Studio, ini adalah cara tercepat.

### File-file yang perlu dibuat:

#### 1. FoodLoverWrapper.h (Bridge antara Native C++ dan Managed C++)
```cpp
// File ini menghubungkan kode native C++ Anda dengan Windows Forms
#pragma once

#include <msclr\marshal_cppstd.h>
#include "Menu.h"
#include "DatabaseMenu.h"
#include "MesinRekomendasi.h"

using namespace System;
using namespace System::Collections::Generic;

namespace FoodLoverAI {
    public ref class MenuManaged {
    public:
        String^ Nama;
        List<String^>^ Bahan;
        List<String^>^ Tags;
    };

    public ref class HasilRekomendasiManaged {
    public:
        String^ NamaMenu;
        double Score;
    };

    public ref class FoodLoverEngine {
    private:
        DatabaseMenu* db;
        MesinRekomendasi* mesin;
    
    public:
        FoodLoverEngine();
        ~FoodLoverEngine();
        
        void MuatDatabase();
        void SimpanDatabase();
        void TambahMenu(String^ nama, List<String^>^ bahan, List<String^>^ tags);
        List<HasilRekomendasiManaged^>^ CariRekomendasi(List<String^>^ bahan, List<String^>^ tags);
        int GetJumlahMenu();
    };
}
```

#### 2. MainForm.h (Main Window)
- Sidebar dengan menu navigasi
- Panel konten dinamis
- Styling modern dengan flat design

#### 3. SearchForm.h (Search Dialog)
- TextBox untuk input bahan
- ListBox untuk display bahan yang diinput
- Button untuk tambah/hapus bahan
- DataGridView untuk hasil rekomendasi

#### 4. AddMenuForm.h (Add Menu Dialog)
- TextBox untuk nama menu
- ListBox untuk bahan dan tags
- Button untuk simpan

---

## Cara Implementasi Cepat:

### A. Jika ingin saya buatkan file lengkap:
Saya bisa buatkan semua file yang dibutuhkan dalam format text yang bisa Anda copy-paste.

### B. Atau kita bisa modifikasi project existing:
1. Tambah project baru (GUI) ke solution yang sama
2. Reference native library dari project GUI
3. Build dua project: Core (native) + GUI (managed)

---

Mana yang Anda pilih? Saya recommend:
1. **Paling Cepat**: Opsi 3 - Windows Forms C++/CLI
2. **Paling Modern**: Opsi 1 - Qt Framework
3. **Paling Fleksibel**: Opsi 2 - Dear ImGui

Beri tahu saya pilihan Anda dan saya akan membantu implementasinya!
