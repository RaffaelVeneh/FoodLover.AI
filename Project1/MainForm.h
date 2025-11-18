#pragma once

namespace FoodLover {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Collections::Generic;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;

	public ref class Menu {
	public:
		String^ namaMenu;
		String^ preferensiRasa;
		List<String^>^ bahan; 

		Menu(String^ nama, String^ rasa, List<String^>^ listBahan) {
			namaMenu = nama;
			preferensiRasa = rasa;
			bahan = listBahan;
		}
	};

	public ref class HasilPencarian {
	public:
		String^ namaMenu;
		int skorKecocokan;

		HasilPencarian(String^ nama, int skor) {
			namaMenu = nama;
			skorKecocokan = skor;
		}
	};

	/// <summary>
	/// Summary for MainForm
	/// </summary>
	public ref class MainForm : public System::Windows::Forms::Form
	{
	public:
		MainForm(void)
		{
			InitializeComponent();
			//
			//TODO: Add the constructor code here
			//
			InisialisasiDatabase();
		}

	protected:
		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		~MainForm()
		{
			if (components)
			{
				delete components;
			}
		}
	private:
		void InisialisasiDatabase()
		{
			// Buat list-nya dulu
			databaseMenu = gcnew List<FoodLover::Menu^>();

			// ---- Mari kita tambahkan beberapa resep bohongan ----

			// 1. Nasi Goreng Pedas
			List<String^>^ bahanNasiGoreng = gcnew List<String^>();
			bahanNasiGoreng->Add("nasi");
			bahanNasiGoreng->Add("telur");
			bahanNasiGoreng->Add("kecap");
			bahanNasiGoreng->Add("cabai");
			databaseMenu->Add(gcnew FoodLover::Menu("Nasi Goreng Pedas", "Pedas", bahanNasiGoreng));

			// 2. Telur Dadar Gurih
			List<String^>^ bahanTelurDadar = gcnew List<String^>();
			bahanTelurDadar->Add("telur");
			bahanTelurDadar->Add("garam");
			bahanTelurDadar->Add("daun bawang");
			databaseMenu->Add(gcnew FoodLover::Menu("Telur Dadar Gurih", "Gurih", bahanTelurDadar));

			// 3. Pisang Goreng Manis
			List<String^>^ bahanPisangGoreng = gcnew List<String^>();
			bahanPisangGoreng->Add("pisang");
			bahanPisangGoreng->Add("tepung");
			bahanPisangGoreng->Add("gula");
			databaseMenu->Add(gcnew FoodLover::Menu("Pisang Goreng Manis", "Manis", bahanPisangGoreng));

			// 4. Ayam Rica-Rica (Contoh dari spek asli Anda)
			List<String^>^ bahanRica = gcnew List<String^>();
			bahanRica->Add("ayam");
			bahanRica->Add("cabai");
			bahanRica->Add("bawang");
			databaseMenu->Add(gcnew FoodLover::Menu("Ayam Rica-Rica", "Pedas", bahanRica));
		}
	private: System::Windows::Forms::Label^ labelRasa;
	protected:

	private: System::Windows::Forms::ComboBox^ comboRasa;

	private: System::Windows::Forms::Button^ btnCari;
	private: System::Windows::Forms::ListBox^ listHasil;
	private: System::Windows::Forms::Label^ labelBahan;



	private: System::Windows::Forms::TextBox^ txtBahan;

	private: List<FoodLover::Menu^>^ databaseMenu;

	protected:

	private:
		/// <summary>
		/// Required designer variable.
		/// </summary>
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		void InitializeComponent(void)
		{
			this->labelRasa = (gcnew System::Windows::Forms::Label());
			this->comboRasa = (gcnew System::Windows::Forms::ComboBox());
			this->btnCari = (gcnew System::Windows::Forms::Button());
			this->listHasil = (gcnew System::Windows::Forms::ListBox());
			this->labelBahan = (gcnew System::Windows::Forms::Label());
			this->txtBahan = (gcnew System::Windows::Forms::TextBox());
			this->SuspendLayout();
			// 
			// labelRasa
			// 
			this->labelRasa->AutoSize = true;
			this->labelRasa->Location = System::Drawing::Point(12, 160);
			this->labelRasa->Name = L"labelRasa";
			this->labelRasa->Size = System::Drawing::Size(85, 13);
			this->labelRasa->TabIndex = 0;
			this->labelRasa->Text = L"Preferensi Rasa:";
			this->labelRasa->Click += gcnew System::EventHandler(this, &MainForm::label1_Click);
			// 
			// comboRasa
			// 
			this->comboRasa->FormattingEnabled = true;
			this->comboRasa->Items->AddRange(gcnew cli::array< System::Object^  >(3) { L"Pedas", L"Manis", L"Gurih" });
			this->comboRasa->Location = System::Drawing::Point(15, 176);
			this->comboRasa->Name = L"comboRasa";
			this->comboRasa->Size = System::Drawing::Size(121, 21);
			this->comboRasa->TabIndex = 1;
			// 
			// btnCari
			// 
			this->btnCari->Location = System::Drawing::Point(151, 174);
			this->btnCari->Name = L"btnCari";
			this->btnCari->Size = System::Drawing::Size(108, 23);
			this->btnCari->TabIndex = 2;
			this->btnCari->Text = L"Cari Rekomendasi";
			this->btnCari->UseVisualStyleBackColor = true;
			this->btnCari->Click += gcnew System::EventHandler(this, &MainForm::btnCari_Click);
			// 
			// listHasil
			// 
			this->listHasil->FormattingEnabled = true;
			this->listHasil->Location = System::Drawing::Point(15, 203);
			this->listHasil->Name = L"listHasil";
			this->listHasil->Size = System::Drawing::Size(398, 121);
			this->listHasil->TabIndex = 3;
			// 
			// labelBahan
			// 
			this->labelBahan->AutoSize = true;
			this->labelBahan->Location = System::Drawing::Point(12, 9);
			this->labelBahan->Name = L"labelBahan";
			this->labelBahan->Size = System::Drawing::Size(126, 13);
			this->labelBahan->TabIndex = 4;
			this->labelBahan->Text = L"Masukkan bahan-bahan:";
			// 
			// txtBahan
			// 
			this->txtBahan->Location = System::Drawing::Point(15, 25);
			this->txtBahan->Multiline = true;
			this->txtBahan->Name = L"txtBahan";
			this->txtBahan->Size = System::Drawing::Size(398, 132);
			this->txtBahan->TabIndex = 5;
			// 
			// MainForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(425, 336);
			this->Controls->Add(this->txtBahan);
			this->Controls->Add(this->labelBahan);
			this->Controls->Add(this->listHasil);
			this->Controls->Add(this->btnCari);
			this->Controls->Add(this->comboRasa);
			this->Controls->Add(this->labelRasa);
			this->Name = L"MainForm";
			this->Text = L"MainForm";
			this->Load += gcnew System::EventHandler(this, &MainForm::MainForm_Load);
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion
	private: System::Void label1_Click(System::Object^ sender, System::EventArgs^ e) {
	}
	private: System::Void MainForm_Load(System::Object^ sender, System::EventArgs^ e) {
	}
private: System::Void btnCari_Click(System::Object^ sender, System::EventArgs^ e) {

	// 1. AMBIL & BERSIHKAN INPUT
	String^ rasaInput = this->comboRasa->Text;
	String^ bahanInput = this->txtBahan->Text;
	this->listHasil->Items->Clear();

	// Validasi: Pastikan pengguna memilih rasa
	if (String::IsNullOrEmpty(rasaInput)) {
		this->listHasil->Items->Add("Silakan pilih preferensi rasa terlebih dahulu.");
		return;
	}

	// 2. PROSES INPUT BAHAN PENGGUNA
	array<Char>^ delimiters = { ',', '.', '\r', '\n', ' ' };

	array<String^>^ bahanUser = bahanInput->Split(delimiters, StringSplitOptions::RemoveEmptyEntries);

	bool ditemukan = false;

	// 3. ITERASI DATABASE (BUKU RESEP)
	for each (FoodLover::Menu ^ resep in databaseMenu)
	{
		// 4. CEK KECOCOKAN RASA
		if (resep->preferensiRasa->Equals(rasaInput, StringComparison::OrdinalIgnoreCase))
		{
			// Rasa cocok, sekarang cek bahannya
			int skorKecocokan = 0;

			// 5. CEK KECOCOKAN BAHAN (SEQUENTIAL SEARCH)
			for each (String ^ bahanResep in resep->bahan)
			{
				for each (String ^ bahanDariUser in bahanUser)
				{
					if (bahanDariUser->Trim()->Equals(bahanResep, StringComparison::OrdinalIgnoreCase))
					{
						skorKecocokan++;
						break;
					}
				}
			}

			// 6. TAMPILKAN HASIL JIKA ADA BAHAN YANG COCOK
			if (skorKecocokan > 0)
			{
				this->listHasil->Items->Add(resep->namaMenu +
					" (Kecocokan: " + skorKecocokan + " bahan)");
				ditemukan = true;
			}
		}
	}

	// 7. CEK JIKA TIDAK ADA HASIL SAMA SEKALI
	if (!ditemukan)
	{
		this->listHasil->Items->Add("Tidak ada resep yang cocok dengan bahan & rasa itu.");
	}
}
};
}
