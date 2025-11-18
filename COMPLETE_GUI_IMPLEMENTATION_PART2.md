# IMPLEMENTASI LENGKAP PART 2: SearchForm & AddMenuForm

## File 3: SearchForm.h
**Location:** FoodLoverGUI\SearchForm.h

```cpp
#pragma once

#include "FoodLoverWrapper.h"

namespace FoodLoverGUI {

    using namespace System;
    using namespace System::ComponentModel;
    using namespace System::Collections;
    using namespace System::Collections::Generic;
    using namespace System::Windows::Forms;
    using namespace System::Data;
    using namespace System::Drawing;

    public ref class SearchForm : public System::Windows::Forms::Form
    {
    public:
        SearchForm(FoodLoverEngine^ eng)
        {
            InitializeComponent();
            engine = eng;
            bahanList = gcnew List<String^>();
            tagsList = gcnew List<String^>();
        }

    protected:
        ~SearchForm()
        {
            if (components)
            {
                delete components;
            }
        }

    private:
        FoodLoverEngine^ engine;
        List<String^>^ bahanList;
        List<String^>^ tagsList;

        System::Windows::Forms::GroupBox^ groupBahan;
        System::Windows::Forms::GroupBox^ groupTags;
        System::Windows::Forms::GroupBox^ groupResults;
        System::Windows::Forms::TextBox^ txtBahan;
        System::Windows::Forms::TextBox^ txtTags;
        System::Windows::Forms::Button^ btnAddBahan;
        System::Windows::Forms::Button^ btnAddTags;
        System::Windows::Forms::Button^ btnRemoveBahan;
        System::Windows::Forms::Button^ btnRemoveTags;
        System::Windows::Forms::Button^ btnSearch;
        System::Windows::Forms::Button^ btnClear;
        System::Windows::Forms::ListBox^ listBahan;
        System::Windows::Forms::ListBox^ listTags;
        System::Windows::Forms::DataGridView^ dataGridResults;
        System::Windows::Forms::Label^ lblInfo;
        System::ComponentModel::Container^ components;

#pragma region Windows Form Designer generated code
        void InitializeComponent(void)
        {
            this->groupBahan = (gcnew System::Windows::Forms::GroupBox());
            this->btnRemoveBahan = (gcnew System::Windows::Forms::Button());
            this->listBahan = (gcnew System::Windows::Forms::ListBox());
            this->btnAddBahan = (gcnew System::Windows::Forms::Button());
            this->txtBahan = (gcnew System::Windows::Forms::TextBox());
            this->groupTags = (gcnew System::Windows::Forms::GroupBox());
            this->btnRemoveTags = (gcnew System::Windows::Forms::Button());
            this->listTags = (gcnew System::Windows::Forms::ListBox());
            this->btnAddTags = (gcnew System::Windows::Forms::Button());
            this->txtTags = (gcnew System::Windows::Forms::TextBox());
            this->groupResults = (gcnew System::Windows::Forms::GroupBox());
            this->dataGridResults = (gcnew System::Windows::Forms::DataGridView());
            this->btnSearch = (gcnew System::Windows::Forms::Button());
            this->btnClear = (gcnew System::Windows::Forms::Button());
            this->lblInfo = (gcnew System::Windows::Forms::Label());
            this->groupBahan->SuspendLayout();
            this->groupTags->SuspendLayout();
            this->groupResults->SuspendLayout();
            (cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->dataGridResults))->BeginInit();
            this->SuspendLayout();
            // 
            // groupBahan
            // 
            this->groupBahan->Controls->Add(this->btnRemoveBahan);
            this->groupBahan->Controls->Add(this->listBahan);
            this->groupBahan->Controls->Add(this->btnAddBahan);
            this->groupBahan->Controls->Add(this->txtBahan);
            this->groupBahan->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->groupBahan->Location = System::Drawing::Point(20, 60);
            this->groupBahan->Name = L"groupBahan";
            this->groupBahan->Size = System::Drawing::Size(350, 300);
            this->groupBahan->TabIndex = 0;
            this->groupBahan->TabStop = false;
            this->groupBahan->Text = L"Bahan yang Anda Miliki";
            // 
            // btnRemoveBahan
            // 
            this->btnRemoveBahan->Location = System::Drawing::Point(190, 260);
            this->btnRemoveBahan->Name = L"btnRemoveBahan";
            this->btnRemoveBahan->Size = System::Drawing::Size(140, 30);
            this->btnRemoveBahan->TabIndex = 3;
            this->btnRemoveBahan->Text = L"Hapus";
            this->btnRemoveBahan->UseVisualStyleBackColor = true;
            this->btnRemoveBahan->Click += gcnew System::EventHandler(this, &SearchForm::btnRemoveBahan_Click);
            // 
            // listBahan
            // 
            this->listBahan->FormattingEnabled = true;
            this->listBahan->ItemHeight = 20;
            this->listBahan->Location = System::Drawing::Point(20, 90);
            this->listBahan->Name = L"listBahan";
            this->listBahan->Size = System::Drawing::Size(310, 164);
            this->listBahan->TabIndex = 2;
            // 
            // btnAddBahan
            // 
            this->btnAddBahan->Location = System::Drawing::Point(240, 40);
            this->btnAddBahan->Name = L"btnAddBahan";
            this->btnAddBahan->Size = System::Drawing::Size(90, 35);
            this->btnAddBahan->TabIndex = 1;
            this->btnAddBahan->Text = L"Tambah";
            this->btnAddBahan->UseVisualStyleBackColor = true;
            this->btnAddBahan->Click += gcnew System::EventHandler(this, &SearchForm::btnAddBahan_Click);
            // 
            // txtBahan
            // 
            this->txtBahan->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->txtBahan->Location = System::Drawing::Point(20, 40);
            this->txtBahan->Name = L"txtBahan";
            this->txtBahan->Size = System::Drawing::Size(210, 29);
            this->txtBahan->TabIndex = 0;
            // 
            // groupTags
            // 
            this->groupTags->Controls->Add(this->btnRemoveTags);
            this->groupTags->Controls->Add(this->listTags);
            this->groupTags->Controls->Add(this->btnAddTags);
            this->groupTags->Controls->Add(this->txtTags);
            this->groupTags->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->groupTags->Location = System::Drawing::Point(390, 60);
            this->groupTags->Name = L"groupTags";
            this->groupTags->Size = System::Drawing::Size(350, 300);
            this->groupTags->TabIndex = 1;
            this->groupTags->TabStop = false;
            this->groupTags->Text = L"Preferensi Rasa / Tags";
            // 
            // btnRemoveTags
            // 
            this->btnRemoveTags->Location = System::Drawing::Point(190, 260);
            this->btnRemoveTags->Name = L"btnRemoveTags";
            this->btnRemoveTags->Size = System::Drawing::Size(140, 30);
            this->btnRemoveTags->TabIndex = 3;
            this->btnRemoveTags->Text = L"Hapus";
            this->btnRemoveTags->UseVisualStyleBackColor = true;
            this->btnRemoveTags->Click += gcnew System::EventHandler(this, &SearchForm::btnRemoveTags_Click);
            // 
            // listTags
            // 
            this->listTags->FormattingEnabled = true;
            this->listTags->ItemHeight = 20;
            this->listTags->Location = System::Drawing::Point(20, 90);
            this->listTags->Name = L"listTags";
            this->listTags->Size = System::Drawing::Size(310, 164);
            this->listTags->TabIndex = 2;
            // 
            // btnAddTags
            // 
            this->btnAddTags->Location = System::Drawing::Point(240, 40);
            this->btnAddTags->Name = L"btnAddTags";
            this->btnAddTags->Size = System::Drawing::Size(90, 35);
            this->btnAddTags->TabIndex = 1;
            this->btnAddTags->Text = L"Tambah";
            this->btnAddTags->UseVisualStyleBackColor = true;
            this->btnAddTags->Click += gcnew System::EventHandler(this, &SearchForm::btnAddTags_Click);
            // 
            // txtTags
            // 
            this->txtTags->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->txtTags->Location = System::Drawing::Point(20, 40);
            this->txtTags->Name = L"txtTags";
            this->txtTags->Size = System::Drawing::Size(210, 29);
            this->txtTags->TabIndex = 0;
            // 
            // groupResults
            // 
            this->groupResults->Controls->Add(this->dataGridResults);
            this->groupResults->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->groupResults->Location = System::Drawing::Point(20, 410);
            this->groupResults->Name = L"groupResults";
            this->groupResults->Size = System::Drawing::Size(720, 250);
            this->groupResults->TabIndex = 2;
            this->groupResults->TabStop = false;
            this->groupResults->Text = L"Hasil Rekomendasi AI";
            // 
            // dataGridResults
            // 
            this->dataGridResults->AllowUserToAddRows = false;
            this->dataGridResults->AllowUserToDeleteRows = false;
            this->dataGridResults->AutoSizeColumnsMode = System::Windows::Forms::DataGridViewAutoSizeColumnsMode::Fill;
            this->dataGridResults->ColumnHeadersHeightSizeMode = System::Windows::Forms::DataGridViewColumnHeadersHeightSizeMode::AutoSize;
            this->dataGridResults->Dock = System::Windows::Forms::DockStyle::Fill;
            this->dataGridResults->Location = System::Drawing::Point(3, 23);
            this->dataGridResults->Name = L"dataGridResults";
            this->dataGridResults->ReadOnly = true;
            this->dataGridResults->Size = System::Drawing::Size(714, 224);
            this->dataGridResults->TabIndex = 0;
            // 
            // btnSearch
            // 
            this->btnSearch->BackColor = System::Drawing::Color::FromArgb(0, 123, 255);
            this->btnSearch->Cursor = System::Windows::Forms::Cursors::Hand;
            this->btnSearch->FlatStyle = System::Windows::Forms::FlatStyle::Flat;
            this->btnSearch->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12, System::Drawing::FontStyle::Bold));
            this->btnSearch->ForeColor = System::Drawing::Color::White;
            this->btnSearch->Location = System::Drawing::Point(190, 370);
            this->btnSearch->Name = L"btnSearch";
            this->btnSearch->Size = System::Drawing::Size(180, 40);
            this->btnSearch->TabIndex = 3;
            this->btnSearch->Text = L"?? Cari Rekomendasi";
            this->btnSearch->UseVisualStyleBackColor = false;
            this->btnSearch->Click += gcnew System::EventHandler(this, &SearchForm::btnSearch_Click);
            // 
            // btnClear
            // 
            this->btnClear->BackColor = System::Drawing::Color::FromArgb(108, 117, 125);
            this->btnClear->Cursor = System::Windows::Forms::Cursors::Hand;
            this->btnClear->FlatStyle = System::Windows::Forms::FlatStyle::Flat;
            this->btnClear->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->btnClear->ForeColor = System::Drawing::Color::White;
            this->btnClear->Location = System::Drawing::Point(390, 370);
            this->btnClear->Name = L"btnClear";
            this->btnClear->Size = System::Drawing::Size(150, 40);
            this->btnClear->TabIndex = 4;
            this->btnClear->Text = L"??? Clear Semua";
            this->btnClear->UseVisualStyleBackColor = false;
            this->btnClear->Click += gcnew System::EventHandler(this, &SearchForm::btnClear_Click);
            // 
            // lblInfo
            // 
            this->lblInfo->Font = (gcnew System::Drawing::Font(L"Segoe UI", 14, System::Drawing::FontStyle::Bold));
            this->lblInfo->Location = System::Drawing::Point(20, 15);
            this->lblInfo->Name = L"lblInfo";
            this->lblInfo->Size = System::Drawing::Size(720, 35);
            this->lblInfo->TabIndex = 5;
            this->lblInfo->Text = L"?? Cari Rekomendasi Makanan dengan AI";
            this->lblInfo->TextAlign = System::Drawing::ContentAlignment::MiddleCenter;
            // 
            // SearchForm
            // 
            this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
            this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
            this->ClientSize = System::Drawing::Size(760, 680);
            this->Controls->Add(this->lblInfo);
            this->Controls->Add(this->btnClear);
            this->Controls->Add(this->btnSearch);
            this->Controls->Add(this->groupResults);
            this->Controls->Add(this->groupTags);
            this->Controls->Add(this->groupBahan);
            this->FormBorderStyle = System::Windows::Forms::FormBorderStyle::FixedDialog;
            this->MaximizeBox = false;
            this->Name = L"SearchForm";
            this->StartPosition = System::Windows::Forms::FormStartPosition::CenterParent;
            this->Text = L"Cari Rekomendasi - FoodLover.AI";
            this->groupBahan->ResumeLayout(false);
            this->groupBahan->PerformLayout();
            this->groupTags->ResumeLayout(false);
            this->groupTags->PerformLayout();
            this->groupResults->ResumeLayout(false);
            (cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->dataGridResults))->EndInit();
            this->ResumeLayout(false);
        }
#pragma endregion

    private: 
        System::Void btnAddBahan_Click(System::Object^ sender, System::EventArgs^ e) {
            if (!String::IsNullOrWhiteSpace(txtBahan->Text)) {
                bahanList->Add(txtBahan->Text->Trim());
                listBahan->Items->Add(txtBahan->Text->Trim());
                txtBahan->Clear();
                txtBahan->Focus();
            }
        }

        System::Void btnAddTags_Click(System::Object^ sender, System::EventArgs^ e) {
            if (!String::IsNullOrWhiteSpace(txtTags->Text)) {
                tagsList->Add(txtTags->Text->Trim());
                listTags->Items->Add(txtTags->Text->Trim());
                txtTags->Clear();
                txtTags->Focus();
            }
        }

        System::Void btnRemoveBahan_Click(System::Object^ sender, System::EventArgs^ e) {
            if (listBahan->SelectedIndex >= 0) {
                int idx = listBahan->SelectedIndex;
                bahanList->RemoveAt(idx);
                listBahan->Items->RemoveAt(idx);
            }
        }

        System::Void btnRemoveTags_Click(System::Object^ sender, System::EventArgs^ e) {
            if (listTags->SelectedIndex >= 0) {
                int idx = listTags->SelectedIndex;
                tagsList->RemoveAt(idx);
                listTags->Items->RemoveAt(idx);
            }
        }

        System::Void btnSearch_Click(System::Object^ sender, System::EventArgs^ e) {
            if (bahanList->Count == 0 && tagsList->Count == 0) {
                MessageBox::Show("Mohon masukkan minimal 1 bahan atau tag!", 
                    "Info", MessageBoxButtons::OK, MessageBoxIcon::Information);
                return;
            }

            try {
                auto hasil = engine->CariRekomendasi(bahanList, tagsList);
                
                // Clear previous results
                dataGridResults->Columns->Clear();
                dataGridResults->Rows->Clear();

                // Setup columns
                dataGridResults->Columns->Add("No", "No");
                dataGridResults->Columns->Add("NamaMenu", "Nama Menu");
                dataGridResults->Columns->Add("Score", "Skor Similarity");
                
                dataGridResults->Columns[0]->Width = 50;
                dataGridResults->Columns[1]->Width = 400;
                dataGridResults->Columns[2]->Width = 150;

                // Add results
                if (hasil->Count == 0) {
                    MessageBox::Show("Tidak ada hasil yang cocok dengan input Anda.", 
                        "Hasil Pencarian", MessageBoxButtons::OK, MessageBoxIcon::Information);
                } else {
                    for (int i = 0; i < hasil->Count; i++) {
                        dataGridResults->Rows->Add(
                            (i + 1).ToString(),
                            hasil[i]->NamaMenu,
                            hasil[i]->Score.ToString("F4")
                        );
                    }
                }
            }
            catch (Exception^ ex) {
                MessageBox::Show("Error: " + ex->Message, "Error", 
                    MessageBoxButtons::OK, MessageBoxIcon::Error);
            }
        }

        System::Void btnClear_Click(System::Object^ sender, System::EventArgs^ e) {
            bahanList->Clear();
            tagsList->Clear();
            listBahan->Items->Clear();
            listTags->Items->Clear();
            dataGridResults->Rows->Clear();
            txtBahan->Clear();
            txtTags->Clear();
        }
    };
}
```

---

## File 4: AddMenuForm.h
**Location:** FoodLoverGUI\AddMenuForm.h

```cpp
#pragma once

#include "FoodLoverWrapper.h"

namespace FoodLoverGUI {

    using namespace System;
    using namespace System::ComponentModel;
    using namespace System::Collections;
    using namespace System::Collections::Generic;
    using namespace System::Windows::Forms;
    using namespace System::Data;
    using namespace System::Drawing;

    public ref class AddMenuForm : public System::Windows::Forms::Form
    {
    public:
        AddMenuForm(FoodLoverEngine^ eng)
        {
            InitializeComponent();
            engine = eng;
            bahanList = gcnew List<String^>();
            tagsList = gcnew List<String^>();
        }

    protected:
        ~AddMenuForm()
        {
            if (components)
            {
                delete components;
            }
        }

    private:
        FoodLoverEngine^ engine;
        List<String^>^ bahanList;
        List<String^>^ tagsList;

        System::Windows::Forms::Label^ lblTitle;
        System::Windows::Forms::Label^ lblNama;
        System::Windows::Forms::Label^ lblBahan;
        System::Windows::Forms::Label^ lblTags;
        System::Windows::Forms::TextBox^ txtNama;
        System::Windows::Forms::TextBox^ txtBahan;
        System::Windows::Forms::TextBox^ txtTags;
        System::Windows::Forms::Button^ btnAddBahan;
        System::Windows::Forms::Button^ btnAddTags;
        System::Windows::Forms::Button^ btnRemoveBahan;
        System::Windows::Forms::Button^ btnRemoveTags;
        System::Windows::Forms::ListBox^ listBahan;
        System::Windows::Forms::ListBox^ listTags;
        System::Windows::Forms::Button^ btnSave;
        System::Windows::Forms::Button^ btnCancel;
        System::ComponentModel::Container^ components;

#pragma region Windows Form Designer generated code
        void InitializeComponent(void)
        {
            this->lblTitle = (gcnew System::Windows::Forms::Label());
            this->lblNama = (gcnew System::Windows::Forms::Label());
            this->lblBahan = (gcnew System::Windows::Forms::Label());
            this->lblTags = (gcnew System::Windows::Forms::Label());
            this->txtNama = (gcnew System::Windows::Forms::TextBox());
            this->txtBahan = (gcnew System::Windows::Forms::TextBox());
            this->txtTags = (gcnew System::Windows::Forms::TextBox());
            this->btnAddBahan = (gcnew System::Windows::Forms::Button());
            this->btnAddTags = (gcnew System::Windows::Forms::Button());
            this->btnRemoveBahan = (gcnew System::Windows::Forms::Button());
            this->btnRemoveTags = (gcnew System::Windows::Forms::Button());
            this->listBahan = (gcnew System::Windows::Forms::ListBox());
            this->listTags = (gcnew System::Windows::Forms::ListBox());
            this->btnSave = (gcnew System::Windows::Forms::Button());
            this->btnCancel = (gcnew System::Windows::Forms::Button());
            this->SuspendLayout();
            // 
            // lblTitle
            // 
            this->lblTitle->Font = (gcnew System::Drawing::Font(L"Segoe UI", 16, System::Drawing::FontStyle::Bold));
            this->lblTitle->Location = System::Drawing::Point(20, 20);
            this->lblTitle->Name = L"lblTitle";
            this->lblTitle->Size = System::Drawing::Size(560, 40);
            this->lblTitle->TabIndex = 0;
            this->lblTitle->Text = L"?? Tambah Menu Baru - Ajari AI";
            this->lblTitle->TextAlign = System::Drawing::ContentAlignment::MiddleCenter;
            // 
            // lblNama
            // 
            this->lblNama->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->lblNama->Location = System::Drawing::Point(20, 80);
            this->lblNama->Name = L"lblNama";
            this->lblNama->Size = System::Drawing::Size(120, 25);
            this->lblNama->TabIndex = 1;
            this->lblNama->Text = L"Nama Menu:";
            // 
            // lblBahan
            // 
            this->lblBahan->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->lblBahan->Location = System::Drawing::Point(20, 140);
            this->lblBahan->Name = L"lblBahan";
            this->lblBahan->Size = System::Drawing::Size(260, 25);
            this->lblBahan->TabIndex = 2;
            this->lblBahan->Text = L"Bahan-bahan:";
            // 
            // lblTags
            // 
            this->lblTags->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->lblTags->Location = System::Drawing::Point(320, 140);
            this->lblTags->Name = L"lblTags";
            this->lblTags->Size = System::Drawing::Size(260, 25);
            this->lblTags->TabIndex = 3;
            this->lblTags->Text = L"Tags / Preferensi:";
            // 
            // txtNama
            // 
            this->txtNama->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->txtNama->Location = System::Drawing::Point(140, 80);
            this->txtNama->Name = L"txtNama";
            this->txtNama->Size = System::Drawing::Size(440, 29);
            this->txtNama->TabIndex = 4;
            // 
            // txtBahan
            // 
            this->txtBahan->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->txtBahan->Location = System::Drawing::Point(20, 170);
            this->txtBahan->Name = L"txtBahan";
            this->txtBahan->Size = System::Drawing::Size(180, 27);
            this->txtBahan->TabIndex = 5;
            // 
            // txtTags
            // 
            this->txtTags->Font = (gcnew System::Drawing::Font(L"Segoe UI", 11));
            this->txtTags->Location = System::Drawing::Point(320, 170);
            this->txtTags->Name = L"txtTags";
            this->txtTags->Size = System::Drawing::Size(180, 27);
            this->txtTags->TabIndex = 6;
            // 
            // btnAddBahan
            // 
            this->btnAddBahan->Location = System::Drawing::Point(210, 170);
            this->btnAddBahan->Name = L"btnAddBahan";
            this->btnAddBahan->Size = System::Drawing::Size(70, 27);
            this->btnAddBahan->TabIndex = 7;
            this->btnAddBahan->Text = L"Tambah";
            this->btnAddBahan->UseVisualStyleBackColor = true;
            this->btnAddBahan->Click += gcnew System::EventHandler(this, &AddMenuForm::btnAddBahan_Click);
            // 
            // btnAddTags
            // 
            this->btnAddTags->Location = System::Drawing::Point(510, 170);
            this->btnAddTags->Name = L"btnAddTags";
            this->btnAddTags->Size = System::Drawing::Size(70, 27);
            this->btnAddTags->TabIndex = 8;
            this->btnAddTags->Text = L"Tambah";
            this->btnAddTags->UseVisualStyleBackColor = true;
            this->btnAddTags->Click += gcnew System::EventHandler(this, &AddMenuForm::btnAddTags_Click);
            // 
            // btnRemoveBahan
            // 
            this->btnRemoveBahan->Location = System::Drawing::Point(20, 380);
            this->btnRemoveBahan->Name = L"btnRemoveBahan";
            this->btnRemoveBahan->Size = System::Drawing::Size(260, 30);
            this->btnRemoveBahan->TabIndex = 9;
            this->btnRemoveBahan->Text = L"Hapus Bahan Terpilih";
            this->btnRemoveBahan->UseVisualStyleBackColor = true;
            this->btnRemoveBahan->Click += gcnew System::EventHandler(this, &AddMenuForm::btnRemoveBahan_Click);
            // 
            // btnRemoveTags
            // 
            this->btnRemoveTags->Location = System::Drawing::Point(320, 380);
            this->btnRemoveTags->Name = L"btnRemoveTags";
            this->btnRemoveTags->Size = System::Drawing::Size(260, 30);
            this->btnRemoveTags->TabIndex = 10;
            this->btnRemoveTags->Text = L"Hapus Tag Terpilih";
            this->btnRemoveTags->UseVisualStyleBackColor = true;
            this->btnRemoveTags->Click += gcnew System::EventHandler(this, &AddMenuForm::btnRemoveTags_Click);
            // 
            // listBahan
            // 
            this->listBahan->Font = (gcnew System::Drawing::Font(L"Segoe UI", 10));
            this->listBahan->FormattingEnabled = true;
            this->listBahan->ItemHeight = 17;
            this->listBahan->Location = System::Drawing::Point(20, 210);
            this->listBahan->Name = L"listBahan";
            this->listBahan->Size = System::Drawing::Size(260, 157);
            this->listBahan->TabIndex = 11;
            // 
            // listTags
            // 
            this->listTags->Font = (gcnew System::Drawing::Font(L"Segoe UI", 10));
            this->listTags->FormattingEnabled = true;
            this->listTags->ItemHeight = 17;
            this->listTags->Location = System::Drawing::Point(320, 210);
            this->listTags->Name = L"listTags";
            this->listTags->Size = System::Drawing::Size(260, 157);
            this->listTags->TabIndex = 12;
            // 
            // btnSave
            // 
            this->btnSave->BackColor = System::Drawing::Color::FromArgb(40, 167, 69);
            this->btnSave->Cursor = System::Windows::Forms::Cursors::Hand;
            this->btnSave->FlatStyle = System::Windows::Forms::FlatStyle::Flat;
            this->btnSave->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12, System::Drawing::FontStyle::Bold));
            this->btnSave->ForeColor = System::Drawing::Color::White;
            this->btnSave->Location = System::Drawing::Point(150, 430);
            this->btnSave->Name = L"btnSave";
            this->btnSave->Size = System::Drawing::Size(150, 45);
            this->btnSave->TabIndex = 13;
            this->btnSave->Text = L"?? Simpan";
            this->btnSave->UseVisualStyleBackColor = false;
            this->btnSave->Click += gcnew System::EventHandler(this, &AddMenuForm::btnSave_Click);
            // 
            // btnCancel
            // 
            this->btnCancel->BackColor = System::Drawing::Color::FromArgb(220, 53, 69);
            this->btnCancel->Cursor = System::Windows::Forms::Cursors::Hand;
            this->btnCancel->DialogResult = System::Windows::Forms::DialogResult::Cancel;
            this->btnCancel->FlatStyle = System::Windows::Forms::FlatStyle::Flat;
            this->btnCancel->Font = (gcnew System::Drawing::Font(L"Segoe UI", 12));
            this->btnCancel->ForeColor = System::Drawing::Color::White;
            this->btnCancel->Location = System::Drawing::Point(310, 430);
            this->btnCancel->Name = L"btnCancel";
            this->btnCancel->Size = System::Drawing::Size(150, 45);
            this->btnCancel->TabIndex = 14;
            this->btnCancel->Text = L"? Batal";
            this->btnCancel->UseVisualStyleBackColor = false;
            // 
            // AddMenuForm
            // 
            this->AcceptButton = this->btnSave;
            this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
            this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
            this->CancelButton = this->btnCancel;
            this->ClientSize = System::Drawing::Size(604, 491);
            this->Controls->Add(this->btnCancel);
            this->Controls->Add(this->btnSave);
            this->Controls->Add(this->listTags);
            this->Controls->Add(this->listBahan);
            this->Controls->Add(this->btnRemoveTags);
            this->Controls->Add(this->btnRemoveBahan);
            this->Controls->Add(this->btnAddTags);
            this->Controls->Add(this->btnAddBahan);
            this->Controls->Add(this->txtTags);
            this->Controls->Add(this->txtBahan);
            this->Controls->Add(this->txtNama);
            this->Controls->Add(this->lblTags);
            this->Controls->Add(this->lblBahan);
            this->Controls->Add(this->lblNama);
            this->Controls->Add(this->lblTitle);
            this->FormBorderStyle = System::Windows::Forms::FormBorderStyle::FixedDialog;
            this->MaximizeBox = false;
            this->MinimizeBox = false;
            this->Name = L"AddMenuForm";
            this->StartPosition = System::Windows::Forms::FormStartPosition::CenterParent;
            this->Text = L"Tambah Menu - FoodLover.AI";
            this->ResumeLayout(false);
            this->PerformLayout();
        }
#pragma endregion

    private: 
        System::Void btnAddBahan_Click(System::Object^ sender, System::EventArgs^ e) {
            if (!String::IsNullOrWhiteSpace(txtBahan->Text)) {
                bahanList->Add(txtBahan->Text->Trim());
                listBahan->Items->Add(txtBahan->Text->Trim());
                txtBahan->Clear();
                txtBahan->Focus();
            }
        }

        System::Void btnAddTags_Click(System::Object^ sender, System::EventArgs^ e) {
            if (!String::IsNullOrWhiteSpace(txtTags->Text)) {
                tagsList->Add(txtTags->Text->Trim());
                listTags->Items->Add(txtTags->Text->Trim());
                txtTags->Clear();
                txtTags->Focus();
            }
        }

        System::Void btnRemoveBahan_Click(System::Object^ sender, System::EventArgs^ e) {
            if (listBahan->SelectedIndex >= 0) {
                int idx = listBahan->SelectedIndex;
                bahanList->RemoveAt(idx);
                listBahan->Items->RemoveAt(idx);
            }
        }

        System::Void btnRemoveTags_Click(System::Object^ sender, System::EventArgs^ e) {
            if (listTags->SelectedIndex >= 0) {
                int idx = listTags->SelectedIndex;
                tagsList->RemoveAt(idx);
                listTags->Items->RemoveAt(idx);
            }
        }

        System::Void btnSave_Click(System::Object^ sender, System::EventArgs^ e) {
            // Validasi input
            if (String::IsNullOrWhiteSpace(txtNama->Text)) {
                MessageBox::Show("Nama menu tidak boleh kosong!", "Validasi", 
                    MessageBoxButtons::OK, MessageBoxIcon::Warning);
                txtNama->Focus();
                return;
            }

            if (bahanList->Count == 0) {
                MessageBox::Show("Mohon masukkan minimal 1 bahan!", "Validasi", 
                    MessageBoxButtons::OK, MessageBoxIcon::Warning);
                return;
            }

            try {
                engine->TambahMenu(txtNama->Text->Trim(), bahanList, tagsList);
                this->DialogResult = System::Windows::Forms::DialogResult::OK;
                this->Close();
            }
            catch (Exception^ ex) {
                MessageBox::Show("Error saat menyimpan: " + ex->Message, "Error", 
                    MessageBoxButtons::OK, MessageBoxIcon::Error);
            }
        }
    };
}
```

---

## File 5: Main.cpp (Entry Point)
**Location:** FoodLoverGUI\Main.cpp

```cpp
#include "MainForm.h"

using namespace System;
using namespace System::Windows::Forms;

[STAThreadAttribute]
int main(array<String^>^ args)
{
    Application::EnableVisualStyles();
    Application::SetCompatibleTextRenderingDefault(false);
    Application::Run(gcnew FoodLoverGUI::MainForm());
    return 0;
}
```

---

## LANGKAH 5: Build Configuration

### 5.1. Edit CashierApp.vcxproj
Tambahkan di dalam `<PropertyGroup>`:
```xml
<ConfigurationType>StaticLibrary</ConfigurationType>
```

### 5.2. Set FoodLoverGUI as Startup Project
Right-click FoodLoverGUI project ? Set as Startup Project

---

## LANGKAH 6: Compile & Run!

1. **Build Solution** (Ctrl+Shift+B)
2. **Run** (F5)

Aplikasi GUI Anda siap! ??

---

## TROUBLESHOOTING

### Error: "Cannot open include file 'msclr\marshal_cppstd.h'"
**Solution:** Add reference to `msclr` in project properties

### Error: "LNK2019 unresolved external symbol"
**Solution:** Make sure CashierApp builds as static library

### Error: "CLR support /clr required"
**Solution:** Enable CLR in project properties

---

**Selamat! Anda sekarang punya aplikasi GUI Windows Forms lengkap dengan machine learning! ??**
