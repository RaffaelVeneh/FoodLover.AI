# IMPLEMENTASI LENGKAP: FoodLover.AI dengan Windows Forms C++/CLI

## LANGKAH 1: Buat Project Baru Windows Forms

1. **Buka Visual Studio 2022**
2. **File ? New ? Project**
3. **Pilih "CLR Empty Project (.NET Framework)"**
4. **Nama:** FoodLoverGUI
5. **Location:** C:\Users\PC\source\repos\algoritma\uas\
6. **Solution:** Add to solution (sama dengan CashierApp)

## LANGKAH 2: Configure Project untuk Windows Forms

### 2.1. Project Properties
Right-click pada project FoodLoverGUI ? Properties:

- **Configuration Properties ? General**
  - Common Language Runtime Support: `/clr`
  - Target Framework: `.NET Framework 4.8`
  
- **C/C++ ? General**
  - Additional Include Directories: `..\CashierApp`

- **Linker ? General**
  - Additional Library Directories: `$(OutDir)`

### 2.2. Add References
Right-click pada project ? Add ? References:
- Add reference to `System.Windows.Forms`
- Add reference to `System.Drawing`
- Add reference to `System` (jika belum ada)

### 2.3. Add Project Dependency
Right-click solution ? Project Dependencies:
- Select FoodLoverGUI
- Check CashierApp

---

## LANGKAH 3: File-File yang Harus Dibuat

### File 1: FoodLoverWrapper.h
**Location:** FoodLoverGUI\FoodLoverWrapper.h

**Purpose:** Bridge antara native C++ dan managed C++/CLI

```cpp
#pragma once

#include <msclr\marshal_cppstd.h>
#include "..\CashierApp\Menu.h"
#include "..\CashierApp\DatabaseMenu.h"
#include "..\CashierApp\MesinRekomendasi.h"

using namespace System;
using namespace System::Collections::Generic;
using namespace msclr::interop;

namespace FoodLoverGUI {

    // Wrapper untuk HasilRekomendasi
    public ref class HasilRekomendasiManaged {
    public:
        String^ NamaMenu;
        double Score;

        HasilRekomendasiManaged(String^ nama, double score) {
            NamaMenu = nama;
            Score = score;
        }
    };

    // Wrapper untuk Engine
    public ref class FoodLoverEngine {
    private:
        DatabaseMenu* db;
        MesinRekomendasi* mesin;
        String^ namaFileDB;

    public:
        FoodLoverEngine() {
            db = new DatabaseMenu();
            mesin = new MesinRekomendasi();
            namaFileDB = "foodlover.db";
        }

        ~FoodLoverEngine() {
            this->!FoodLoverEngine();
        }

        !FoodLoverEngine() {
            if (db) {
                delete db;
                db = nullptr;
            }
            if (mesin) {
                delete mesin;
                mesin = nullptr;
            }
        }

        // Load database
        void MuatDatabase() {
            std::string fileName = marshal_as<std::string>(namaFileDB);
            db->muatDariFile(fileName);
        }

        // Save database
        void SimpanDatabase() {
            std::string fileName = marshal_as<std::string>(namaFileDB);
            db->simpanKeFile(fileName);
        }

        // Tambah menu baru
        void TambahMenu(String^ nama, List<String^>^ bahan, List<String^>^ tags) {
            std::string stdNama = marshal_as<std::string>(nama);
            
            std::vector<std::string> stdBahan;
            for each (String^ b in bahan) {
                stdBahan.push_back(marshal_as<std::string>(b));
            }

            std::vector<std::string> stdTags;
            for each (String^ t in tags) {
                stdTags.push_back(marshal_as<std::string>(t));
            }

            Menu menuBaru(stdNama, stdBahan, stdTags);
            db->tambahMenu(menuBaru);
            SimpanDatabase();
        }

        // Cari rekomendasi
        List<HasilRekomendasiManaged^>^ CariRekomendasi(List<String^>^ bahan, List<String^>^ tags) {
            std::vector<std::string> stdBahan;
            for each (String^ b in bahan) {
                stdBahan.push_back(marshal_as<std::string>(b));
            }

            std::vector<std::string> stdTags;
            for each (String^ t in tags) {
                stdTags.push_back(marshal_as<std::string>(t));
            }

            std::vector<HasilRekomendasi> hasil = mesin->berikanRekomendasi(
                db->getDaftarMenu(), stdBahan, stdTags
            );

            List<HasilRekomendasiManaged^>^ hasilManaged = gcnew List<HasilRekomendasiManaged^>();
            for (const auto& h : hasil) {
                String^ nama = gcnew String(h.namaMenu.c_str());
                hasilManaged->Add(gcnew HasilRekomendasiManaged(nama, h.score));
            }

            return hasilManaged;
        }

        // Get jumlah menu
        int GetJumlahMenu() {
            return static_cast<int>(db->getDaftarMenu().size());
        }
    };
}
```

---

### File 2: MainForm.h
**Location:** FoodLoverGUI\MainForm.h

```cpp
#pragma once

#include "FoodLoverWrapper.h"
#include "SearchForm.h"
#include "AddMenuForm.h"

namespace FoodLoverGUI {

    using namespace System;
    using namespace System::ComponentModel;
    using namespace System::Collections;
    using namespace System::Windows::Forms;
    using namespace System::Data;
    using namespace System::Drawing;

    public ref class MainForm : public System::Windows::Forms::Form
    {
    public:
        MainForm(void)
        {
            InitializeComponent();
            engine = gcnew FoodLoverEngine();
            engine->MuatDatabase();
            UpdateStatusBar();
        }

    protected:
        ~MainForm()
        {
            if (components)
            {
                delete components;
            }
            delete engine;
        }

    private:
        FoodLoverEngine^ engine;
        System::Windows::Forms::Panel^ panelSidebar;
        System::Windows::Forms::Panel^ panelMain;
        System::Windows::Forms::Button^ btnSearch;
        System::Windows::Forms::Button^ btnAddMenu;
        System::Windows::Forms::Button^ btnExit;
        System::Windows::Forms::Label^ lblTitle;
        System::Windows::Forms::Label^ lblWelcome;
        System::Windows::Forms::Label^ lblSubtitle;
        System::Windows::Forms::Label^ lblStatus;
        System::Windows::Forms::PictureBox^ pictureBox1;
        System::ComponentModel::Container^ components;

#pragma region Windows Form Designer generated code
        void InitializeComponent(void)
        {
            this->panelSidebar = (gcnew System::Windows::Forms::Panel());
            this->btnExit = (gcnew System::Windows::Forms::Button());
            this->btnAddMenu = (gcnew System::Windows::Forms::Button());
            this->btnSearch = (gcnew System::Windows::Forms::Button());
            this->lblTitle = (gcnew System::Windows::Forms::Label());
            this->panelMain = (gcnew System::Windows::Forms::Panel());
            this->lblStatus = (gcnew System::Windows::Forms::Label());
            this->lblSubtitle = (gcnew System::Windows::Forms::Label());
            this->pictureBox1 = (gcnew System::Windows::Forms::PictureBox());
            this->lblWelcome = (gcnew System::Windows::Forms::Label());
            this->panelSidebar->SuspendLayout();
            this->panelMain->SuspendLayout();
            (cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox1))->BeginInit();
            this->SuspendLayout();
            // 
            // panelSidebar
            // 
            this->panelSidebar->BackColor = System::Drawing::Color::FromArgb(41, 44, 51);
            this->panelSidebar->Controls->Add(this->btnExit);
            this->panelSidebar->Controls->Add(this->btnAddMenu);
            this->panelSidebar->Controls->Add(this->btnSearch);
            this->panelSidebar->Controls->Add(this->lblTitle);
            this->panelSidebar->Dock = System::Windows::Forms::DockStyle::Left;
            this->panelSidebar->Location = System::Drawing::Point(0, 0);
            this->panelSidebar->Name = L"panelSidebar";
            this->panelSidebar->Size = System::Drawing::Size(250, 561);
            this->panelSidebar->TabIndex = 0;
            // 
            // btnExit
            // 
            this->btnExit->Cursor = System::Windows::Forms::Cursors::Hand;
            this->btnExit->Dock = System::Windows::Forms::DockStyle::Bottom;
            this->btnExit->FlatAppearance->BorderSize = 0;
            this->btnExit->FlatStyle = System::Windows::Forms::FlatStyle::Flat;
            this->btnExit->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->btnExit->ForeColor = System::Drawing::Color::White;
            this->btnExit->Location = System::Drawing::Point(0, 511);
            this->btnExit->Name = L"btnExit";
            this->btnExit->Padding = System::Windows::Forms::Padding(10, 0, 0, 0);
            this->btnExit->Size = System::Drawing::Size(250, 50);
            this->btnExit->TabIndex = 3;
            this->btnExit->Text = L"?? Keluar";
            this->btnExit->TextAlign = System::Drawing::ContentAlignment::MiddleLeft;
            this->btnExit->UseVisualStyleBackColor = true;
            this->btnExit->Click += gcnew System::EventHandler(this, &MainForm::btnExit_Click);
            // 
            // btnAddMenu
            // 
            this->btnAddMenu->Cursor = System::Windows::Forms::Cursors::Hand;
            this->btnAddMenu->FlatAppearance->BorderSize = 0;
            this->btnAddMenu->FlatStyle = System::Windows::Forms::FlatStyle::Flat;
            this->btnAddMenu->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->btnAddMenu->ForeColor = System::Drawing::Color::White;
            this->btnAddMenu->Location = System::Drawing::Point(0, 200);
            this->btnAddMenu->Name = L"btnAddMenu";
            this->btnAddMenu->Padding = System::Windows::Forms::Padding(10, 0, 0, 0);
            this->btnAddMenu->Size = System::Drawing::Size(250, 50);
            this->btnAddMenu->TabIndex = 2;
            this->btnAddMenu->Text = L"?? Tambah Menu Baru";
            this->btnAddMenu->TextAlign = System::Drawing::ContentAlignment::MiddleLeft;
            this->btnAddMenu->UseVisualStyleBackColor = true;
            this->btnAddMenu->MouseEnter += gcnew System::EventHandler(this, &MainForm::btn_MouseEnter);
            this->btnAddMenu->MouseLeave += gcnew System::EventHandler(this, &MainForm::btn_MouseLeave);
            this->btnAddMenu->Click += gcnew System::EventHandler(this, &MainForm::btnAddMenu_Click);
            // 
            // btnSearch
            // 
            this->btnSearch->Cursor = System::Windows::Forms::Cursors::Hand;
            this->btnSearch->FlatAppearance->BorderSize = 0;
            this->btnSearch->FlatStyle = System::Windows::Forms::FlatStyle::Flat;
            this->btnSearch->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->btnSearch->ForeColor = System::Drawing::Color::White;
            this->btnSearch->Location = System::Drawing::Point(0, 150);
            this->btnSearch->Name = L"btnSearch";
            this->btnSearch->Padding = System::Windows::Forms::Padding(10, 0, 0, 0);
            this->btnSearch->Size = System::Drawing::Size(250, 50);
            this->btnSearch->TabIndex = 1;
            this->btnSearch->Text = L"?? Cari Rekomendasi";
            this->btnSearch->TextAlign = System::Drawing::ContentAlignment::MiddleLeft;
            this->btnSearch->UseVisualStyleBackColor = true;
            this->btnSearch->MouseEnter += gcnew System::EventHandler(this, &MainForm::btn_MouseEnter);
            this->btnSearch->MouseLeave += gcnew System::EventHandler(this, &MainForm::btn_MouseLeave);
            this->btnSearch->Click += gcnew System::EventHandler(this, &MainForm::btnSearch_Click);
            // 
            // lblTitle
            // 
            this->lblTitle->Dock = System::Windows::Forms::DockStyle::Top;
            this->lblTitle->Font = (gcnew System::Drawing::Font(L"Segoe UI", 20, System::Drawing::FontStyle::Bold));
            this->lblTitle->ForeColor = System::Drawing::Color::FromArgb(0, 173, 181);
            this->lblTitle->Location = System::Drawing::Point(0, 0);
            this->lblTitle->Name = L"lblTitle";
            this->lblTitle->Padding = System::Windows::Forms::Padding(10, 20, 0, 0);
            this->lblTitle->Size = System::Drawing::Size(250, 100);
            this->lblTitle->TabIndex = 0;
            this->lblTitle->Text = L"FoodLover.AI";
            // 
            // panelMain
            // 
            this->panelMain->BackColor = System::Drawing::Color::FromArgb(240, 242, 245);
            this->panelMain->Controls->Add(this->lblStatus);
            this->panelMain->Controls->Add(this->lblSubtitle);
            this->panelMain->Controls->Add(this->pictureBox1);
            this->panelMain->Controls->Add(this->lblWelcome);
            this->panelMain->Dock = System::Windows::Forms::DockStyle::Fill;
            this->panelMain->Location = System::Drawing::Point(250, 0);
            this->panelMain->Name = L"panelMain";
            this->panelMain->Size = System::Drawing::Size(834, 561);
            this->panelMain->TabIndex = 1;
            // 
            // lblStatus
            // 
            this->lblStatus->Anchor = System::Windows::Forms::AnchorStyles::Bottom;
            this->lblStatus->Font = (gcnew System::Drawing::Font(L"Segoe UI", 10));
            this->lblStatus->ForeColor = System::Drawing::Color::Gray;
            this->lblStatus->Location = System::Drawing::Point(200, 520);
            this->lblStatus->Name = L"lblStatus";
            this->lblStatus->Size = System::Drawing::Size(434, 25);
            this->lblStatus->TabIndex = 3;
            this->lblStatus->Text = L"Database: 0 menu";
            this->lblStatus->TextAlign = System::Drawing::ContentAlignment::TopCenter;
            // 
            // lblSubtitle
            // 
            this->lblSubtitle->Anchor = System::Windows::Forms::AnchorStyles::None;
            this->lblSubtitle->Font = (gcnew System::Drawing::Font(L"Segoe UI", 14));
            this->lblSubtitle->ForeColor = System::Drawing::Color::Gray;
            this->lblSubtitle->Location = System::Drawing::Point(150, 380);
            this->lblSubtitle->Name = L"lblSubtitle";
            this->lblSubtitle->Size = System::Drawing::Size(534, 80);
            this->lblSubtitle->TabIndex = 2;
            this->lblSubtitle->Text = L"Sistem Rekomendasi Makanan dengan Machine Learning\nMenggunakan Content-Based Fil" 
                L"tering & Cosine Similarity";
            this->lblSubtitle->TextAlign = System::Drawing::ContentAlignment::TopCenter;
            // 
            // pictureBox1
            // 
            this->pictureBox1->Anchor = System::Windows::Forms::AnchorStyles::None;
            this->pictureBox1->Location = System::Drawing::Point(317, 170);
            this->pictureBox1->Name = L"pictureBox1";
            this->pictureBox1->Size = System::Drawing::Size(200, 150);
            this->pictureBox1->TabIndex = 1;
            this->pictureBox1->TabStop = false;
            // 
            // lblWelcome
            // 
            this->lblWelcome->Anchor = System::Windows::Forms::AnchorStyles::None;
            this->lblWelcome->Font = (gcnew System::Drawing::Font(L"Segoe UI", 26, System::Drawing::FontStyle::Bold));
            this->lblWelcome->ForeColor = System::Drawing::Color::FromArgb(41, 44, 51);
            this->lblWelcome->Location = System::Drawing::Point(100, 100);
            this->lblWelcome->Name = L"lblWelcome";
            this->lblWelcome->Size = System::Drawing::Size(634, 60);
            this->lblWelcome->TabIndex = 0;
            this->lblWelcome->Text = L"Selamat Datang! ??";
            this->lblWelcome->TextAlign = System::Drawing::ContentAlignment::TopCenter;
            // 
            // MainForm
            // 
            this->AutoScaleDimensions = System::Drawing::SizeF(8, 16);
            this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
            this->ClientSize = System::Drawing::Size(1084, 561);
            this->Controls->Add(this->panelMain);
            this->Controls->Add(this->panelSidebar);
            this->MinimumSize = System::Drawing::Size(1100, 600);
            this->Name = L"MainForm";
            this->StartPosition = System::Windows::Forms::FormStartPosition::CenterScreen;
            this->Text = L"FoodLover.AI - Intelligent Food Recommendation System";
            this->panelSidebar->ResumeLayout(false);
            this->panelMain->ResumeLayout(false);
            (cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox1))->EndInit();
            this->ResumeLayout(false);
        }
#pragma endregion

    private: 
        System::Void btnSearch_Click(System::Object^ sender, System::EventArgs^ e) {
            SearchForm^ searchForm = gcnew SearchForm(engine);
            searchForm->ShowDialog();
        }
        
        System::Void btnAddMenu_Click(System::Object^ sender, System::EventArgs^ e) {
            AddMenuForm^ addForm = gcnew AddMenuForm(engine);
            if (addForm->ShowDialog() == System::Windows::Forms::DialogResult::OK) {
                UpdateStatusBar();
                MessageBox::Show("Menu berhasil ditambahkan!", "Sukses", 
                    MessageBoxButtons::OK, MessageBoxIcon::Information);
            }
        }
        
        System::Void btnExit_Click(System::Object^ sender, System::EventArgs^ e) {
            Application::Exit();
        }

        System::Void btn_MouseEnter(System::Object^ sender, System::EventArgs^ e) {
            Button^ btn = (Button^)sender;
            btn->BackColor = Color::FromArgb(52, 58, 64);
        }

        System::Void btn_MouseLeave(System::Object^ sender, System::EventArgs^ e) {
            Button^ btn = (Button^)sender;
            btn->BackColor = Color::Transparent;
        }

        void UpdateStatusBar() {
            int count = engine->GetJumlahMenu();
            lblStatus->Text = "Database: " + count + " menu tersimpan";
        }
    };
}
```

[CONTINUED IN NEXT MESSAGE - File terlalu panjang]

---

## LANGKAH 4: Compile & Run

1. Build CashierApp project dulu (native C++)
2. Build FoodLoverGUI project (managed C++/CLI)
3. Set FoodLoverGUI as StartUp Project
4. Run!

**APAKAH ANDA MAU SAYA LANJUTKAN dengan SearchForm.h dan AddMenuForm.h?**
