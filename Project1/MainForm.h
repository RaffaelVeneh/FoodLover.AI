#pragma once
#include "DataModels.h"
#include "FeedbackForm.h"
using namespace System::IO;
using namespace System::Net;
using namespace System::Text;
using namespace System::Text::RegularExpressions;

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

	private: System::Windows::Forms::Label^ labelBahan;



	private: System::Windows::Forms::TextBox^ txtBahan;

	private: List<FoodLover::Menu^>^ databaseMenu;
	private: System::Windows::Forms::Button^ btnFeedback;
private: System::Windows::Forms::TreeView^ treeViewHasil;

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
			this->labelBahan = (gcnew System::Windows::Forms::Label());
			this->txtBahan = (gcnew System::Windows::Forms::TextBox());
			this->btnFeedback = (gcnew System::Windows::Forms::Button());
			this->treeViewHasil = (gcnew System::Windows::Forms::TreeView());
			this->SuspendLayout();
			// 
			// labelRasa
			// 
			this->labelRasa->AutoSize = true;
			this->labelRasa->Location = System::Drawing::Point(12, 218);
			this->labelRasa->Name = L"labelRasa";
			this->labelRasa->Size = System::Drawing::Size(85, 13);
			this->labelRasa->TabIndex = 0;
			this->labelRasa->Text = L"Preferensi Rasa:";
			this->labelRasa->Click += gcnew System::EventHandler(this, &MainForm::label1_Click);
			// 
			// comboRasa
			// 
			this->comboRasa->FormattingEnabled = true;
			this->comboRasa->Items->AddRange(gcnew cli::array< System::Object^  >(4) { L"Semua", L"Pedas", L"Manis", L"Gurih" });
			this->comboRasa->Location = System::Drawing::Point(15, 234);
			this->comboRasa->Name = L"comboRasa";
			this->comboRasa->Size = System::Drawing::Size(121, 21);
			this->comboRasa->TabIndex = 1;
			// 
			// btnCari
			// 
			this->btnCari->Location = System::Drawing::Point(151, 232);
			this->btnCari->Name = L"btnCari";
			this->btnCari->Size = System::Drawing::Size(108, 23);
			this->btnCari->TabIndex = 2;
			this->btnCari->Text = L"Cari Rekomendasi";
			this->btnCari->UseVisualStyleBackColor = true;
			this->btnCari->Click += gcnew System::EventHandler(this, &MainForm::btnCari_Click);
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
			this->txtBahan->Size = System::Drawing::Size(472, 178);
			this->txtBahan->TabIndex = 5;
			// 
			// btnFeedback
			// 
			this->btnFeedback->Location = System::Drawing::Point(15, 414);
			this->btnFeedback->Name = L"btnFeedback";
			this->btnFeedback->Size = System::Drawing::Size(141, 29);
			this->btnFeedback->TabIndex = 6;
			this->btnFeedback->Text = L"Menu Tidak Ditemukan\?";
			this->btnFeedback->UseVisualStyleBackColor = true;
			this->btnFeedback->Click += gcnew System::EventHandler(this, &MainForm::btnFeedback_Click);
			// 
			// treeViewHasil
			// 
			this->treeViewHasil->Font = (gcnew System::Drawing::Font(L"Microsoft Sans Serif", 9));
			this->treeViewHasil->Location = System::Drawing::Point(15, 262);
			this->treeViewHasil->Name = L"treeViewHasil";
			this->treeViewHasil->Size = System::Drawing::Size(472, 146);
			this->treeViewHasil->TabIndex = 7;
			// 
			// MainForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(499, 503);
			this->Controls->Add(this->treeViewHasil);
			this->Controls->Add(this->btnFeedback);
			this->Controls->Add(this->txtBahan);
			this->Controls->Add(this->labelBahan);
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

		// 1. PERSIAPAN UI & DATA
		this->treeViewHasil->Nodes->Clear();
		this->treeViewHasil->BeginUpdate();

		String^ rasaInput = this->comboRasa->Text;
		String^ bahanMentah = this->txtBahan->Text;

		if (String::IsNullOrEmpty(rasaInput)) {
			this->treeViewHasil->EndUpdate();
			return;
		}

		// Sanitasi input bahan (Hapus Enter dan kutip)
		String^ bahanAman = bahanMentah->Replace("\r\n", " ")->Replace("\n", " ")->Replace("\"", "");
		String^ jsonKirim = "{ \"bahan\": \"" + bahanAman + "\", \"rasa\": \"" + rasaInput + "\" }";

		// 2. REQUEST KE SERVER
		String^ url = "http://127.0.0.1:5000/cari";
		String^ responseServer = "";

		try {
			WebClient^ client = gcnew WebClient();
			client->Headers->Add("Content-Type", "application/json");
			client->Encoding = System::Text::Encoding::UTF8;
			responseServer = client->UploadString(url, "POST", jsonKirim);
		}
		catch (Exception^ ex) {
			MessageBox::Show("Server Error: " + ex->Message);
			this->treeViewHasil->EndUpdate();
			return;
		}

		// 3. PARSING JSON TANGGUH (REGEX VERSION)
		// Server Flask (Debug Mode) mengirim JSON dengan banyak spasi dan Enter (\n).
		// Contoh: "}, \n  {". Kita harus membersihkannya dulu.

		// A. Hapus semua Baris Baru (Enter) agar string menjadi satu baris panjang
		String^ satuBaris = responseServer->Replace("\r", "")->Replace("\n", "");

		// B. Hapus kurung siku pembungkus array [ ... ]
		satuBaris = satuBaris->Trim();
		if (satuBaris->StartsWith("[") && satuBaris->EndsWith("]")) {
			satuBaris = satuBaris->Substring(1, satuBaris->Length - 2);
		}

		// Jika kosong (tidak ada hasil), berhenti
		if (String::IsNullOrWhiteSpace(satuBaris)) {
			this->treeViewHasil->Nodes->Add("Tidak ada resep yang cocok.");
			this->treeViewHasil->EndUpdate();
			return;
		}

		// C. GUNAKAN REGEX untuk memisahkan objek
		// Pola: Mencari "}" diikuti spasi berapapun, lalu koma, lalu spasi berapapun, lalu "{"
		// Kita ubah pola tersebut menjadi tanda pemisah unik "|BATAS|"
		String^ dataTerpisah = Regex::Replace(satuBaris, "\\}\\s*,\\s*\\{", "}|BATAS|{");

		// D. Split string berdasarkan tanda unik tadi
		array<String^>^ listMenuRaw = dataTerpisah->Split(gcnew array<String^>{"|BATAS|"}, StringSplitOptions::RemoveEmptyEntries);

		bool adaHasil = false;

		for each(String ^ menuString in listMenuRaw) {
			// Bersihkan karakter JSON ({, }, ") yang tersisa
			String^ menuBersih = menuString->Replace("{", "")->Replace("}", "")->Replace("\"", "");

			// Split properti berdasarkan koma
			array<String^>^ properti = menuBersih->Split(',');

			String^ namaMenu = "";
			String^ skor = "";
			String^ rasaMenu = "";
			String^ bahanLengkapStr = "";
			String^ bahanMatchStr = "";

			for each(String ^ prop in properti) {
				String^ p = prop->Trim();
				if (p->StartsWith("nama:")) namaMenu = p->Substring(5)->Trim();
				else if (p->StartsWith("rasa:")) rasaMenu = p->Substring(5)->Trim();
				else if (p->StartsWith("skor:")) skor = p->Substring(5)->Trim();
				else if (p->StartsWith("bahan_lengkap:")) bahanLengkapStr = p->Substring(14)->Trim();
				else if (p->StartsWith("bahan_match:")) bahanMatchStr = p->Substring(12)->Trim();
			}

			// 4. RENDER HASIL
			if (namaMenu != "" && skor != "0") {
				adaHasil = true;

				// Format Label dengan Info Rasa (Sesuai Request)
				String^ labelNode = namaMenu + " (" + skor + " Cocok";
				if (rasaInput == "Semua") {
					labelNode += ", Rasa: " + rasaMenu;
				}
				labelNode += ")";

				TreeNode^ parentNode = gcnew TreeNode(labelNode);
				parentNode->ForeColor = Color::DarkBlue;
				parentNode->NodeFont = gcnew System::Drawing::Font(this->treeViewHasil->Font, FontStyle::Bold);

				// Render Bahan
				array<String^>^ listBahan = bahanLengkapStr->Split('|');
				for each(String ^ bahan in listBahan) {
					TreeNode^ childNode = gcnew TreeNode();

					// Cek Match
					if (bahanMatchStr->Contains(bahan)) {
						childNode->Text = "v " + bahan; // Checklist
						childNode->ForeColor = Color::Green;
						childNode->NodeFont = gcnew System::Drawing::Font(this->treeViewHasil->Font, FontStyle::Bold);
					}
					else {
						childNode->Text = "- " + bahan;
						childNode->ForeColor = Color::Gray;
					}
					parentNode->Nodes->Add(childNode);
				}

				this->treeViewHasil->Nodes->Add(parentNode);
			}
		}

		if (!adaHasil) {
			this->treeViewHasil->Nodes->Add("Tidak ada resep yang cocok.");
		}

		this->treeViewHasil->EndUpdate();
	}
	private: System::Void btnFeedback_Click(System::Object^ sender, System::EventArgs^ e) {
		FeedbackForm^ form = gcnew FeedbackForm();

		form->ShowDialog();
	}
};
}
