#pragma once
#include "DataModels.h"
#include "FeedbackForm.h"
using namespace System::IO;
using namespace System::Net;
using namespace System::Text;

namespace FoodLover {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Collections::Generic;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;

	

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
			MuatFeedbackDariFile();

			this->comboRasa->SelectedIndex = 0;
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
	private:
		void MuatFeedbackDariFile()
		{
			String^ namaFile = "feedback.txt";
			if (!File::Exists(namaFile)) {
				return;
			}

			array<String^>^ semuaBaris = File::ReadAllLines(namaFile);

			String^ menuBerikutnya = nullptr;
			String^ rasaBerikutnya = nullptr; // <-- Variabel baru
			String^ bahanBerikutnya = nullptr;

			for each (String ^ baris in semuaBaris)
			{
				if (baris->StartsWith("Nama Menu: ")) {
					menuBerikutnya = baris->Substring(11)->Trim();
				}
				else if (baris->StartsWith("Rasa: ")) { // <-- Logika baru
					rasaBerikutnya = baris->Substring(6)->Trim();
				}
				else if (baris->StartsWith("Bahan: ")) { // <-- Logika baru
					bahanBerikutnya = baris->Substring(7)->Trim();
				}

				// Cek jika SEMUA data sudah terkumpul
				if (menuBerikutnya != nullptr && rasaBerikutnya != nullptr && bahanBerikutnya != nullptr)
				{
					// Parser bahan sekarang JAUH lebih sederhana!
					// Kita hanya perlu split berdasarkan koma.
					List<String^>^ listBahan = gcnew List<String^>();
					array<String^>^ bahanArray = bahanBerikutnya->Split(',');

					for each (String ^ b in bahanArray) {
						// Kita tetap 'Trim' untuk jaga-jaga
						listBahan->Add(b->Trim());
					}

					// Tambahkan ke database
					databaseMenu->Add(gcnew FoodLover::Menu(menuBerikutnya,
						rasaBerikutnya, // <-- Gunakan rasa baru
						listBahan));

					// Reset untuk mencari menu berikutnya
					menuBerikutnya = nullptr;
					rasaBerikutnya = nullptr;
					bahanBerikutnya = nullptr;
				}
			}
		}
	private: System::Windows::Forms::Label^ labelRasa;
	protected:

	private: System::Windows::Forms::ComboBox^ comboRasa;

	private: System::Windows::Forms::Button^ btnCari;
	private: System::Windows::Forms::ListBox^ listHasil;
	private: System::Windows::Forms::Label^ labelBahan;



	private: System::Windows::Forms::TextBox^ txtBahan;

	private: List<FoodLover::Menu^>^ databaseMenu;
	private: System::Windows::Forms::Button^ btnFeedback;


private: System::Windows::Forms::Button^ button3;
private: System::Windows::Forms::Label^ label1;

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
			this->btnFeedback = (gcnew System::Windows::Forms::Button());
			this->button3 = (gcnew System::Windows::Forms::Button());
			this->label1 = (gcnew System::Windows::Forms::Label());
			this->SuspendLayout();
			// 
			// labelRasa
			// 
			this->labelRasa->AutoSize = true;
			this->labelRasa->Location = System::Drawing::Point(18, 335);
			this->labelRasa->Margin = System::Windows::Forms::Padding(4, 0, 4, 0);
			this->labelRasa->Name = L"labelRasa";
			this->labelRasa->Size = System::Drawing::Size(285, 20);
			this->labelRasa->TabIndex = 0;
			this->labelRasa->Text = L"Preferensi Rasa/Rasa yang Diinginkan:";
			this->labelRasa->Click += gcnew System::EventHandler(this, &MainForm::label1_Click);
			// 
			// comboRasa
			// 
			this->comboRasa->FormattingEnabled = true;
			this->comboRasa->Items->AddRange(gcnew cli::array< System::Object^  >(4) { L"Semua", L"Pedas", L"Manis", L"Gurih" });
			this->comboRasa->Location = System::Drawing::Point(22, 369);
			this->comboRasa->Margin = System::Windows::Forms::Padding(4, 5, 4, 5);
			this->comboRasa->Name = L"comboRasa";
			this->comboRasa->Size = System::Drawing::Size(180, 28);
			this->comboRasa->TabIndex = 1;
			// 
			// btnCari
			// 
			this->btnCari->Location = System::Drawing::Point(226, 366);
			this->btnCari->Margin = System::Windows::Forms::Padding(4, 5, 4, 5);
			this->btnCari->Name = L"btnCari";
			this->btnCari->Size = System::Drawing::Size(162, 35);
			this->btnCari->TabIndex = 2;
			this->btnCari->Text = L"Cari Rekomendasi";
			this->btnCari->UseVisualStyleBackColor = true;
			this->btnCari->Click += gcnew System::EventHandler(this, &MainForm::btnCari_Click);
			// 
			// listHasil
			// 
			this->listHasil->FormattingEnabled = true;
			this->listHasil->ItemHeight = 20;
			this->listHasil->Location = System::Drawing::Point(22, 449);
			this->listHasil->Margin = System::Windows::Forms::Padding(4, 5, 4, 5);
			this->listHasil->Name = L"listHasil";
			this->listHasil->Size = System::Drawing::Size(671, 224);
			this->listHasil->TabIndex = 3;
			// 
			// labelBahan
			// 
			this->labelBahan->AutoSize = true;
			this->labelBahan->Location = System::Drawing::Point(18, 14);
			this->labelBahan->Margin = System::Windows::Forms::Padding(4, 0, 4, 0);
			this->labelBahan->Name = L"labelBahan";
			this->labelBahan->Size = System::Drawing::Size(284, 20);
			this->labelBahan->TabIndex = 4;
			this->labelBahan->Text = L"Masukkan bahan-bahan yang tersedia:";
			// 
			// txtBahan
			// 
			this->txtBahan->Location = System::Drawing::Point(22, 38);
			this->txtBahan->Margin = System::Windows::Forms::Padding(4, 5, 4, 5);
			this->txtBahan->Multiline = true;
			this->txtBahan->Name = L"txtBahan";
			this->txtBahan->Size = System::Drawing::Size(671, 272);
			this->txtBahan->TabIndex = 5;
			// 
			// btnFeedback
			// 
			this->btnFeedback->Location = System::Drawing::Point(22, 684);
			this->btnFeedback->Margin = System::Windows::Forms::Padding(4, 5, 4, 5);
			this->btnFeedback->Name = L"btnFeedback";
			this->btnFeedback->Size = System::Drawing::Size(193, 53);
			this->btnFeedback->TabIndex = 6;
			this->btnFeedback->Text = L"Menu Tidak Ditemukan\?";
			this->btnFeedback->UseVisualStyleBackColor = true;
			this->btnFeedback->Click += gcnew System::EventHandler(this, &MainForm::btnFeedback_Click);
			// 
			// button3
			// 
			this->button3->Location = System::Drawing::Point(226, 684);
			this->button3->Name = L"button3";
			this->button3->Size = System::Drawing::Size(162, 53);
			this->button3->TabIndex = 9;
			this->button3->Text = L"Selesai";
			this->button3->UseVisualStyleBackColor = true;
			this->button3->Click += gcnew System::EventHandler(this, &MainForm::button3_Click);
			// 
			// label1
			// 
			this->label1->AutoSize = true;
			this->label1->Location = System::Drawing::Point(18, 424);
			this->label1->Margin = System::Windows::Forms::Padding(4, 0, 4, 0);
			this->label1->Name = L"label1";
			this->label1->Size = System::Drawing::Size(221, 20);
			this->label1->TabIndex = 10;
			this->label1->Text = L"Rekomendasi Menu Makanan";
			// 
			// MainForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(9, 20);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(706, 767);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->button3);
			this->Controls->Add(this->btnFeedback);
			this->Controls->Add(this->txtBahan);
			this->Controls->Add(this->labelBahan);
			this->Controls->Add(this->listHasil);
			this->Controls->Add(this->btnCari);
			this->Controls->Add(this->comboRasa);
			this->Controls->Add(this->labelRasa);
			this->Margin = System::Windows::Forms::Padding(4, 5, 4, 5);
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

		// 1. AMBIL INPUT
		String^ rasaInput = this->comboRasa->Text;
		String^ bahanMentah = this->txtBahan->Text;
		this->listHasil->Items->Clear();

		if (String::IsNullOrEmpty(rasaInput)) return;

		String^ bahanAman = bahanMentah
			->Replace("\r\n", " ")  // Ganti Enter (Windows) jadi spasi
			->Replace("\n", " ")    // Ganti Enter (Linux/Mac) jadi spasi
			->Replace("\"", "");    // Hapus tanda kutip ganda (") agar tidak merusak format JSON

		// 2. SIAPKAN DATA JSON (MANUAL)
		// Gunakan 'bahanAman', BUKAN 'bahanMentah' atau 'bahanInput'
		String^ jsonKirim = "{ \"bahan\": \"" + bahanAman + "\", \"rasa\": \"" + rasaInput + "\" }";

		// 3. KIRIM KE SERVER (POST REQUEST)
		String^ url = "http://127.0.0.1:5000/cari";
		String^ responseServer = "";

		try {
			WebClient^ client = gcnew WebClient();
			// Kita harus memberi tahu server bahwa kita mengirim JSON
			client->Headers->Add("Content-Type", "application/json");

			// Lakukan pengiriman (UploadString)
			// Ini akan menunggu sampai server membalas...
			responseServer = client->UploadString(url, "POST", jsonKirim);
		}
		catch (Exception^ ex) {
			MessageBox::Show("Gagal terhubung ke server Python!\nPastikan server.py sudah berjalan.\n\nError: " + ex->Message);
			return;
		}

		// 4. PARSING RESPON SERVER (CARA SEDERHANA)
		// Server membalas: [{"nama": "Nasi Goreng", "rasa": "Pedas", "skor": 3}, {...}]

		// Langkah A: Hapus karakter yang membingungkan (kurung siku, kurung kurawal)
		String^ bersih = responseServer->Replace("[", "")->Replace("]", "")->Replace("{", "")->Replace("}", "")->Replace("\"", "");
		// Hasil 'bersih': nama: Nasi Goreng, rasa: Pedas, skor: 3, nama: ...

		// Langkah B: Pisahkan berdasarkan koma (pemisah antar properti)
		// TAPI hati-hati, antar objek juga dipisah koma. 
		// Karena format server kita konsisten, kita bisa split lalu cari kata kuncinya.
		array<String^>^ properti = bersih->Split(',');

		String^ namaSementara = "";
		String^ rasaSementara = "";
		String^ skorSementara = "";

		bool adaHasil = false;

		for each (String ^ prop in properti) {
			// prop isinya misal: "nama: Nasi Goreng" atau " skor: 3"
			String^ p = prop->Trim();

			if (p->StartsWith("nama:")) {
				namaSementara = p->Substring(5)->Trim(); // Ambil teks setelah "nama:"
			}
			else if (p->StartsWith("rasa:")) {
				rasaSementara = p->Substring(5)->Trim();
			}
			else if (p->StartsWith("skor:")) {
				skorSementara = p->Substring(5)->Trim();

				// 5. TAMPILKAN (Saat kita sudah menemukan skor, berarti 1 menu selesai dibaca)
				if (namaSementara != "" && skorSementara != "0") {
					String^ tampil = namaSementara + " (Kecocokan: " + skorSementara + " bahan";
					if (rasaInput == "Semua") {
						tampil += ", Rasa: " + rasaSementara;
					}
					tampil += ")";

					this->listHasil->Items->Add(tampil);
					adaHasil = true;
				}

				// Reset untuk menu berikutnya
				namaSementara = "";
				rasaSementara = "";
				skorSementara = "";
			}
		}

		if (!adaHasil) {
			this->listHasil->Items->Add("Tidak ada resep yang cocok (Kata Server).");
		}
	}
	private: System::Void btnFeedback_Click(System::Object^ sender, System::EventArgs^ e) {
		FeedbackForm^ form = gcnew FeedbackForm();

		form->ShowDialog();
	}
private: System::Void button3_Click(System::Object^ sender, System::EventArgs^ e) {
	this->Close();
}
};
}
