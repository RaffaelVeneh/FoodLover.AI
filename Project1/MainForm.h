#pragma once
#include "DataModels.h"
#include "FeedbackForm.h"
using namespace System::IO;
using namespace System::Net;
using namespace System::Text;
using namespace System::Text::RegularExpressions;
using namespace System::Globalization;
using namespace Newtonsoft::Json;
using namespace Newtonsoft::Json::Linq;

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
			this->comboKategori->SelectedIndex = 0;
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
		// Malas hapus, ini inisialisasi database manual
		void InisialisasiDatabase()
		{
			databaseMenu = gcnew List<FoodLover::Menu^>();
			List<String^>^ bahanNasiGoreng = gcnew List<String^>();
			bahanNasiGoreng->Add("nasi");
			bahanNasiGoreng->Add("telur");
			bahanNasiGoreng->Add("kecap");
			bahanNasiGoreng->Add("cabai");
			databaseMenu->Add(gcnew FoodLover::Menu("Nasi Goreng Pedas", "Pedas", bahanNasiGoreng));

			List<String^>^ bahanTelurDadar = gcnew List<String^>();
			bahanTelurDadar->Add("telur");
			bahanTelurDadar->Add("garam");
			bahanTelurDadar->Add("daun bawang");
			databaseMenu->Add(gcnew FoodLover::Menu("Telur Dadar Gurih", "Gurih", bahanTelurDadar));

			List<String^>^ bahanPisangGoreng = gcnew List<String^>();
			bahanPisangGoreng->Add("pisang");
			bahanPisangGoreng->Add("tepung");
			bahanPisangGoreng->Add("gula");
			databaseMenu->Add(gcnew FoodLover::Menu("Pisang Goreng Manis", "Manis", bahanPisangGoreng));

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
			String^ rasaBerikutnya = nullptr;
			String^ bahanBerikutnya = nullptr;

			for each (String ^ baris in semuaBaris)
			{
				if (baris->StartsWith("Nama Menu: ")) {
					menuBerikutnya = baris->Substring(11)->Trim();
				}
				else if (baris->StartsWith("Rasa: ")) {
					rasaBerikutnya = baris->Substring(6)->Trim();
				}
				else if (baris->StartsWith("Bahan: ")) {
					bahanBerikutnya = baris->Substring(7)->Trim();
				}

				// Cek jika SEMUA data sudah terkumpul
				if (menuBerikutnya != nullptr && rasaBerikutnya != nullptr && bahanBerikutnya != nullptr)
				{
					List<String^>^ listBahan = gcnew List<String^>();
					array<String^>^ bahanArray = bahanBerikutnya->Split(',');

					for each (String ^ b in bahanArray) {
						// Kita tetap 'Trim' untuk jaga-jaga
						listBahan->Add(b->Trim());
					}

					databaseMenu->Add(gcnew FoodLover::Menu(menuBerikutnya,
						rasaBerikutnya, 
						listBahan));

					menuBerikutnya = nullptr;
					rasaBerikutnya = nullptr;
					bahanBerikutnya = nullptr;
				}
			}
		}
	private: 
		void OnTrainingSelesai(Object^ sender, DownloadStringCompletedEventArgs^ e) 
		{
			if (e->Error == nullptr) {
				// Sukses
				Console::WriteLine("Info: AI telah selesai dilatih ulang di background.");
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
private: System::Windows::Forms::ComboBox^ comboKategori;
private: System::Windows::Forms::Label^ labelKategori;

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
			this->comboKategori = (gcnew System::Windows::Forms::ComboBox());
			this->labelKategori = (gcnew System::Windows::Forms::Label());
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
			this->comboRasa->Items->AddRange(gcnew cli::array< System::Object^  >(8) {
				L"Semua", L"Pedas", L"Manis", L"Gurih", L"Asam",
					L"Segar", L"Pahit", L"Creamy"
			});
			this->comboRasa->Location = System::Drawing::Point(15, 234);
			this->comboRasa->Name = L"comboRasa";
			this->comboRasa->Size = System::Drawing::Size(121, 21);
			this->comboRasa->TabIndex = 1;
			// 
			// btnCari
			// 
			this->btnCari->Location = System::Drawing::Point(269, 234);
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
			this->txtBahan->Size = System::Drawing::Size(571, 178);
			this->txtBahan->TabIndex = 5;
			// 
			// btnFeedback
			// 
			this->btnFeedback->Location = System::Drawing::Point(15, 541);
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
			this->treeViewHasil->Size = System::Drawing::Size(571, 273);
			this->treeViewHasil->TabIndex = 7;
			this->treeViewHasil->NodeMouseDoubleClick += gcnew System::Windows::Forms::TreeNodeMouseClickEventHandler(this, &MainForm::treeViewHasil_NodeMouseDoubleClick);
			// 
			// comboKategori
			// 
			this->comboKategori->FormattingEnabled = true;
			this->comboKategori->Items->AddRange(gcnew cli::array< System::Object^  >(4) { L"Semua", L"Makanan", L"Minuman", L"Camilan" });
			this->comboKategori->Location = System::Drawing::Point(142, 234);
			this->comboKategori->Name = L"comboKategori";
			this->comboKategori->Size = System::Drawing::Size(121, 21);
			this->comboKategori->TabIndex = 8;
			// 
			// labelKategori
			// 
			this->labelKategori->AutoSize = true;
			this->labelKategori->Location = System::Drawing::Point(139, 218);
			this->labelKategori->Name = L"labelKategori";
			this->labelKategori->Size = System::Drawing::Size(49, 13);
			this->labelKategori->TabIndex = 9;
			this->labelKategori->Text = L"Kategori:";
			// 
			// MainForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(598, 606);
			this->Controls->Add(this->labelKategori);
			this->Controls->Add(this->comboKategori);
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
		try {
			String^ url = "http://127.0.0.1:5000/latih-ulang";
			WebClient^ client = gcnew WebClient();

			client->DownloadStringCompleted += gcnew DownloadStringCompletedEventHandler(this, &MainForm::OnTrainingSelesai);
			client->DownloadStringAsync(gcnew Uri(url));
		}
		catch (Exception^ ex) {
			Console::WriteLine("Gagal memicu auto-training: " + ex->Message);
		}
	}
	private: System::Void btnCari_Click(System::Object^ sender, System::EventArgs^ e) {

		this->treeViewHasil->Nodes->Clear();
		this->treeViewHasil->BeginUpdate();

		String^ rasaInput = this->comboRasa->Text;
		String^ bahanMentah = this->txtBahan->Text;
		String^ kategoriInput = this->comboKategori->Text;

		if (String::IsNullOrEmpty(rasaInput)) { this->treeViewHasil->EndUpdate(); return; }

		String^ bahanAman = bahanMentah->Replace("\r\n", " ")->Replace("\n", " ")->Replace("\"", "");
		String^ jsonKirim = "{ \"bahan\": \"" + bahanAman + "\", \"rasa\": \"" + rasaInput + "\", \"kategori\": \"" + kategoriInput + "\" }";

		String^ url = "http://127.0.0.1:5000/cari";
		String^ responseServer = "";

		try {
			WebClient^ client = gcnew WebClient();
			client->Headers->Add("Content-Type", "application/json");
			client->Encoding = System::Text::Encoding::UTF8;
			responseServer = client->UploadString(url, "POST", jsonKirim);
		}
		catch (Exception^ ex) {
			MessageBox::Show("Gagal terhubung ke server AI: " + ex->Message);
			this->treeViewHasil->EndUpdate();
			return;
		}

		try {
			JArray^ dataArray = JArray::Parse(responseServer);

			if (dataArray->Count == 0) {
				this->treeViewHasil->Nodes->Add("Tidak ada data.");
				this->treeViewHasil->EndUpdate();
				return;
			}

			bool pesanDitampilkan = false;

			for each (JObject ^ menu in dataArray) {

				String^ namaMenu = (String^)menu["nama"];
				String^ skor = menu["skor"]->ToString();
				String^ rasaMenu = (String^)menu["rasa"];
				String^ labelAi = (String^)menu["label_ai"];
				String^ pesanSistem = (String^)menu["pesan_sistem"];

				String^ bahanLengkapStr = (String^)menu["bahan_lengkap"];
				String^ bahanMatchStr = (String^)menu["bahan_match"];
				String^ metaWaktu = (String^)menu["meta_waktu"];
				String^ metaKategori = (String^)menu["meta_kategori"];
				String^ metaSifat = (String^)menu["meta_sifat"];

				// --- LOGIKA UI (Visualisasi) ---
				if (!pesanDitampilkan && !String::IsNullOrEmpty(pesanSistem)) {
					TreeNode^ nodePesan = gcnew TreeNode(pesanSistem);
					nodePesan->ForeColor = Color::Red;
					nodePesan->NodeFont = gcnew System::Drawing::Font(this->treeViewHasil->Font, FontStyle::Italic);
					this->treeViewHasil->Nodes->Add(nodePesan);
					pesanDitampilkan = true;
				}

				if (!String::IsNullOrEmpty(namaMenu)) {
					String^ labelNode = namaMenu;

					// Hanya tampilkan skor kecocokan jika bukan hasil random (skor > 0)
					if (skor != "0") {
						labelNode += " (" + skor + " Cocok";
						if (rasaInput == "Semua") labelNode += ", Rasa: " + rasaMenu;
						labelNode += ")";
					}
					else {
						labelNode += " (" + rasaMenu + ")";
					}

					TreeNode^ parentNode = gcnew TreeNode();

					// Cek apakah ini Rekomendasi AI (Hybrid)
					if (labelAi == "YA") {
						parentNode->Text = "[REKOMENDASI AI] " + labelNode;
						parentNode->ForeColor = Color::DarkViolet;
						parentNode->NodeFont = gcnew System::Drawing::Font(this->treeViewHasil->Font, FontStyle::Bold);
						// Auto expand rekomendasi AI agar user langsung lihat
						parentNode->Expand();
					}
					else {
						parentNode->Text = labelNode;
						parentNode->ForeColor = Color::DarkBlue;
						parentNode->NodeFont = gcnew System::Drawing::Font(this->treeViewHasil->Font, FontStyle::Bold);
					}

					TreeNode^ metaNode = gcnew TreeNode("Info & Konteks");
					metaNode->ForeColor = Color::DarkMagenta;

					metaNode->Nodes->Add("Kategori: " + metaKategori);
					metaNode->Nodes->Add("Waktu: " + (metaWaktu != nullptr ? metaWaktu->Replace("|", ", ") : "-"));
					metaNode->Nodes->Add("Sifat: " + (metaSifat != nullptr ? metaSifat->Replace("|", ", ") : "-"));
					parentNode->Nodes->Add(metaNode);

					TreeNode^ bahanNode = gcnew TreeNode("Rincian Bahan");

					if (!String::IsNullOrEmpty(bahanLengkapStr)) {
						array<String^>^ listBahan = bahanLengkapStr->Split('|');
						for each (String ^ bahan in listBahan) {
							TreeNode^ childNode = gcnew TreeNode();

							// Highlight bahan yang user miliki (Match)
							// Kita cek apakah string bahanMatchStr mengandung bahan ini
							if (bahanMatchStr != nullptr && bahanMatchStr->Contains(bahan) && skor != "0") {
								childNode->Text = "v " + bahan;
								childNode->ForeColor = Color::Green;
								childNode->NodeFont = gcnew System::Drawing::Font(this->treeViewHasil->Font, FontStyle::Bold);
							}
							else {
								childNode->Text = "- " + bahan;
								childNode->ForeColor = Color::Gray;
							}
							bahanNode->Nodes->Add(childNode);
						}
					}
					parentNode->Nodes->Add(bahanNode);

					// Masukkan ke TreeView Utama
					this->treeViewHasil->Nodes->Add(parentNode);
				}
			}
		}
		catch (Exception^ ex) {
			MessageBox::Show("Error saat membaca data dari AI: " + ex->Message, "Parsing Error");
		}

		this->treeViewHasil->EndUpdate();
	}
	private: System::Void btnFeedback_Click(System::Object^ sender, System::EventArgs^ e) {
		FeedbackForm^ form = gcnew FeedbackForm();

		form->ShowDialog();
	}
	private: System::Void treeViewHasil_NodeMouseDoubleClick(System::Object^ sender, System::Windows::Forms::TreeNodeMouseClickEventArgs^ e) {
		// Parent node levelnya 0. Child node levelnya 1.
		if (e->Node->Level != 0) return;

		// Ambil nama menu dari teks node. 
		String^ teksNode = e->Node->Text;
		int indexKurung = teksNode->IndexOf("(");
		if (indexKurung < 0) return;

		String^ namaMenuFix = teksNode->Substring(0, indexKurung)->Trim();
		String^ inputBahan = this->txtBahan->Text->Replace("\n", " ")->Replace("\"", "");
		String^ rasaInput = this->comboRasa->Text;

		int jam = DateTime::Now.Hour;
		String^ waktuSekarang = "malam";
		if (jam >= 5 && jam < 11) waktuSekarang = "pagi";
		else if (jam >= 11 && jam < 15) waktuSekarang = "siang";
		else if (jam >= 15 && jam < 19) waktuSekarang = "sore";

		String^ jsonLog = String::Format(
			"{{"
			"\"input_user\": \"{0}\", "
			"\"rasa_input\": \"{1}\", "
			"\"menu_dipilih\": \"{2}\", "
			"\"waktu_akses\": \"{3}\", "
			"\"timestamp\": \"{4}\""
			"}}",
			inputBahan, rasaInput, namaMenuFix, waktuSekarang, DateTime::Now.ToString("yyyy-MM-dd HH:mm:ss")
		);

		try {
			String^ url = "http://127.0.0.1:5000/catat-pilihan";
			WebClient^ client = gcnew WebClient();
			client->Headers->Add("Content-Type", "application/json");
			client->UploadStringAsync(gcnew Uri(url), "POST", jsonLog);

			Console::WriteLine("Log terkirim untuk: " + namaMenuFix);
		}
		catch (Exception^ ex) {
			Console::WriteLine("Gagal log: " + ex->Message);
		}
	}
};
}
