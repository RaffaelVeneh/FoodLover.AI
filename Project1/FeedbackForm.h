#pragma once

namespace FoodLover {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace System::IO;
	using namespace System::Net;

	/// <summary>
	/// Summary for FeedbackForm
	/// </summary>
	public ref class FeedbackForm : public System::Windows::Forms::Form
	{
	public:
		FeedbackForm(void)
		{
			InitializeComponent();
			//
			//TODO: Add the constructor code here
			//
		}

	protected:
		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		~FeedbackForm()
		{
			if (components)
			{
				delete components;
			}
		}
	private: System::Windows::Forms::Label^ LabelMenuBaru;
	protected:
	private: System::Windows::Forms::TextBox^ txtNamaMenu;
	private: System::Windows::Forms::Label^ LabelBahan;
	private: System::Windows::Forms::TextBox^ txtBahanFeedback;
	private: System::Windows::Forms::Button^ btnKirim;
	private: System::Windows::Forms::Button^ btnBatal;
	private: System::Windows::Forms::Label^ LabelRasa;
	private: System::Windows::Forms::ComboBox^ comboRasaFeedback;
	private: System::Windows::Forms::ComboBox^ comboKategoriMenu;
	private: System::Windows::Forms::ComboBox^ comboWaktuMenu;


	private: System::Windows::Forms::Label^ label1;
	private: System::Windows::Forms::Label^ label2;
	private: System::Windows::Forms::Label^ label3;





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
			this->LabelMenuBaru = (gcnew System::Windows::Forms::Label());
			this->txtNamaMenu = (gcnew System::Windows::Forms::TextBox());
			this->LabelBahan = (gcnew System::Windows::Forms::Label());
			this->txtBahanFeedback = (gcnew System::Windows::Forms::TextBox());
			this->btnKirim = (gcnew System::Windows::Forms::Button());
			this->btnBatal = (gcnew System::Windows::Forms::Button());
			this->LabelRasa = (gcnew System::Windows::Forms::Label());
			this->comboRasaFeedback = (gcnew System::Windows::Forms::ComboBox());
			this->comboKategoriMenu = (gcnew System::Windows::Forms::ComboBox());
			this->comboWaktuMenu = (gcnew System::Windows::Forms::ComboBox());
			this->label1 = (gcnew System::Windows::Forms::Label());
			this->label2 = (gcnew System::Windows::Forms::Label());
			this->label3 = (gcnew System::Windows::Forms::Label());
			this->SuspendLayout();
			// 
			// LabelMenuBaru
			// 
			this->LabelMenuBaru->AutoSize = true;
			this->LabelMenuBaru->Location = System::Drawing::Point(13, 13);
			this->LabelMenuBaru->Name = L"LabelMenuBaru";
			this->LabelMenuBaru->Size = System::Drawing::Size(93, 13);
			this->LabelMenuBaru->TabIndex = 0;
			this->LabelMenuBaru->Text = L"Nama Menu Baru:";
			// 
			// txtNamaMenu
			// 
			this->txtNamaMenu->Location = System::Drawing::Point(16, 30);
			this->txtNamaMenu->Name = L"txtNamaMenu";
			this->txtNamaMenu->Size = System::Drawing::Size(463, 20);
			this->txtNamaMenu->TabIndex = 1;
			// 
			// LabelBahan
			// 
			this->LabelBahan->AutoSize = true;
			this->LabelBahan->Location = System::Drawing::Point(13, 74);
			this->LabelBahan->Name = L"LabelBahan";
			this->LabelBahan->Size = System::Drawing::Size(74, 13);
			this->LabelBahan->TabIndex = 2;
			this->LabelBahan->Text = L"Bahan-bahan:";
			// 
			// txtBahanFeedback
			// 
			this->txtBahanFeedback->Location = System::Drawing::Point(16, 90);
			this->txtBahanFeedback->Multiline = true;
			this->txtBahanFeedback->Name = L"txtBahanFeedback";
			this->txtBahanFeedback->Size = System::Drawing::Size(463, 185);
			this->txtBahanFeedback->TabIndex = 3;
			// 
			// btnKirim
			// 
			this->btnKirim->Location = System::Drawing::Point(16, 475);
			this->btnKirim->Name = L"btnKirim";
			this->btnKirim->Size = System::Drawing::Size(90, 28);
			this->btnKirim->TabIndex = 4;
			this->btnKirim->Text = L"Kirim";
			this->btnKirim->UseVisualStyleBackColor = true;
			this->btnKirim->Click += gcnew System::EventHandler(this, &FeedbackForm::btnKirim_Click);
			// 
			// btnBatal
			// 
			this->btnBatal->Location = System::Drawing::Point(112, 475);
			this->btnBatal->Name = L"btnBatal";
			this->btnBatal->Size = System::Drawing::Size(93, 28);
			this->btnBatal->TabIndex = 5;
			this->btnBatal->Text = L"batal";
			this->btnBatal->UseVisualStyleBackColor = true;
			this->btnBatal->Click += gcnew System::EventHandler(this, &FeedbackForm::btnBatal_Click);
			// 
			// LabelRasa
			// 
			this->LabelRasa->AutoSize = true;
			this->LabelRasa->Location = System::Drawing::Point(13, 289);
			this->LabelRasa->Name = L"LabelRasa";
			this->LabelRasa->Size = System::Drawing::Size(85, 13);
			this->LabelRasa->TabIndex = 6;
			this->LabelRasa->Text = L"Preferensi Rasa:";
			// 
			// comboRasaFeedback
			// 
			this->comboRasaFeedback->FormattingEnabled = true;
			this->comboRasaFeedback->Items->AddRange(gcnew cli::array< System::Object^  >(7) {
				L"Pedas", L"Manis", L"Gurih", L"Asam",
					L"Segar", L"Pahit", L"Creamy"
			});
			this->comboRasaFeedback->Location = System::Drawing::Point(16, 306);
			this->comboRasaFeedback->Name = L"comboRasaFeedback";
			this->comboRasaFeedback->Size = System::Drawing::Size(156, 21);
			this->comboRasaFeedback->TabIndex = 7;
			// 
			// comboKategoriMenu
			// 
			this->comboKategoriMenu->FormattingEnabled = true;
			this->comboKategoriMenu->Items->AddRange(gcnew cli::array< System::Object^  >(3) { L"Makanan", L"Minuman", L"Camilan" });
			this->comboKategoriMenu->Location = System::Drawing::Point(219, 306);
			this->comboKategoriMenu->Name = L"comboKategoriMenu";
			this->comboKategoriMenu->Size = System::Drawing::Size(140, 21);
			this->comboKategoriMenu->TabIndex = 8;
			// 
			// comboWaktuMenu
			// 
			this->comboWaktuMenu->FormattingEnabled = true;
			this->comboWaktuMenu->Items->AddRange(gcnew cli::array< System::Object^  >(4) { L"Pagi", L"Siang", L"Malam", L"Kapanpun" });
			this->comboWaktuMenu->Location = System::Drawing::Point(16, 381);
			this->comboWaktuMenu->Name = L"comboWaktuMenu";
			this->comboWaktuMenu->Size = System::Drawing::Size(156, 21);
			this->comboWaktuMenu->TabIndex = 9;
			// 
			// label1
			// 
			this->label1->AutoSize = true;
			this->label1->Location = System::Drawing::Point(216, 289);
			this->label1->Name = L"label1";
			this->label1->Size = System::Drawing::Size(79, 13);
			this->label1->TabIndex = 10;
			this->label1->Text = L"Kategori Menu:";
			// 
			// label2
			// 
			this->label2->AutoSize = true;
			this->label2->Location = System::Drawing::Point(13, 365);
			this->label2->Name = L"label2";
			this->label2->Size = System::Drawing::Size(140, 13);
			this->label2->TabIndex = 11;
			this->label2->Text = L"Rekomendasi Waktu Menu:";
			// 
			// label3
			// 
			this->label3->AutoSize = true;
			this->label3->Font = (gcnew System::Drawing::Font(L"Microsoft Sans Serif", 9));
			this->label3->Location = System::Drawing::Point(13, 415);
			this->label3->Name = L"label3";
			this->label3->Size = System::Drawing::Size(466, 45);
			this->label3->TabIndex = 12;
			this->label3->Text = L"Peringatan: \r\nData langsung masuk ke databases sehingga dapat langsung memengaruh"
				L"i output \r\ndari program. jadi tolong perhatikan input yang diberikan";
			// 
			// FeedbackForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(491, 539);
			this->Controls->Add(this->label3);
			this->Controls->Add(this->label2);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->comboWaktuMenu);
			this->Controls->Add(this->comboKategoriMenu);
			this->Controls->Add(this->comboRasaFeedback);
			this->Controls->Add(this->LabelRasa);
			this->Controls->Add(this->btnBatal);
			this->Controls->Add(this->btnKirim);
			this->Controls->Add(this->txtBahanFeedback);
			this->Controls->Add(this->LabelBahan);
			this->Controls->Add(this->txtNamaMenu);
			this->Controls->Add(this->LabelMenuBaru);
			this->Name = L"FeedbackForm";
			this->Text = L"FeedbackForm";
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion
	private: System::Void btnKirim_Click(System::Object^ sender, System::EventArgs^ e) {

		// 1. AMBIL DATA DARI UI
		String^ namaMenu = this->txtNamaMenu->Text;
		String^ rasa = this->comboRasaFeedback->Text;
		String^ bahanMentah = this->txtBahanFeedback->Text;

		// Ambil data Metadata baru
		String^ kategori = this->comboKategoriMenu->Text;
		String^ waktu = this->comboWaktuMenu->Text;

		// 2. VALIDASI
		// Pastikan user tidak mengosongkan input penting
		if (String::IsNullOrWhiteSpace(namaMenu) || String::IsNullOrWhiteSpace(bahanMentah) ||
			String::IsNullOrWhiteSpace(kategori) || String::IsNullOrWhiteSpace(waktu)) {
			MessageBox::Show("Mohon lengkapi semua data (Nama, Bahan, Kategori, dan Waktu).",
				"Data Belum Lengkap", MessageBoxButtons::OK, MessageBoxIcon::Warning);
			return;
		}

		// 3. SANITASI INPUT
		String^ bahanAman = bahanMentah->Replace("\r\n", " ")->Replace("\n", " ")->Replace("\"", "");
		String^ namaAman = namaMenu->Replace("\"", "");

		// 4. BENTUK JSON LENGKAP
		// Kita kirim field tambahan: 'kategori' dan 'waktu'
		String^ jsonKirim = String::Format(
			"{{"
			"\"nama\": \"{0}\", "
			"\"rasa\": \"{1}\", "
			"\"bahan\": \"{2}\", "
			"\"kategori\": \"{3}\", "
			"\"waktu\": \"{4}\""
			"}}",
			namaAman, rasa, bahanAman, kategori, waktu
		);

		// 5. KIRIM KE SERVER
		String^ url = "http://127.0.0.1:5000/tambah";

		try {
			WebClient^ client = gcnew WebClient();
			client->Headers->Add("Content-Type", "application/json");

			// Gunakan Encoding UTF8 agar karakter khusus aman
			client->Encoding = System::Text::Encoding::UTF8;

			// Kirim!
			String^ respon = client->UploadString(url, "POST", jsonKirim);

			MessageBox::Show("Terima kasih! Resep baru telah ditambahkan ke database dan dipelajari AI.",
				"Sukses", MessageBoxButtons::OK, MessageBoxIcon::Information);
			this->Close();
		}
		catch (Exception^ ex) {
			MessageBox::Show("Gagal terhubung ke server: " + ex->Message,
				"Error Server", MessageBoxButtons::OK, MessageBoxIcon::Error);
		}
	}
	private: System::Void btnBatal_Click(System::Object^ sender, System::EventArgs^ e) {
		this->Close();
	}
};
}
