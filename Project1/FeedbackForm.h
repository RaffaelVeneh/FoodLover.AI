#pragma once

namespace FoodLover {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace System::IO;

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
			this->txtNamaMenu->Size = System::Drawing::Size(449, 20);
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
			this->txtBahanFeedback->Size = System::Drawing::Size(446, 185);
			this->txtBahanFeedback->TabIndex = 3;
			// 
			// btnKirim
			// 
			this->btnKirim->Location = System::Drawing::Point(16, 341);
			this->btnKirim->Name = L"btnKirim";
			this->btnKirim->Size = System::Drawing::Size(90, 28);
			this->btnKirim->TabIndex = 4;
			this->btnKirim->Text = L"Kirim";
			this->btnKirim->UseVisualStyleBackColor = true;
			this->btnKirim->Click += gcnew System::EventHandler(this, &FeedbackForm::btnKirim_Click);
			// 
			// btnBatal
			// 
			this->btnBatal->Location = System::Drawing::Point(113, 341);
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
			this->comboRasaFeedback->Items->AddRange(gcnew cli::array< System::Object^  >(3) { L"Pedas", L"Manis", L"Gurih" });
			this->comboRasaFeedback->Location = System::Drawing::Point(16, 306);
			this->comboRasaFeedback->Name = L"comboRasaFeedback";
			this->comboRasaFeedback->Size = System::Drawing::Size(140, 21);
			this->comboRasaFeedback->TabIndex = 7;
			// 
			// FeedbackForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(477, 440);
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

		// 1. Ambil SEMUA data
		String^ namaMenu = this->txtNamaMenu->Text;
		String^ rasa = this->comboRasaFeedback->Text; // Data baru
		String^ bahanInputKotor = this->txtBahanFeedback->Text; // Data "kotor"

		// 2. Validasi (sekarang cek rasa juga)
		if (String::IsNullOrWhiteSpace(namaMenu) ||
			String::IsNullOrWhiteSpace(rasa) ||
			String::IsNullOrWhiteSpace(bahanInputKotor))
		{
			MessageBox::Show("Nama menu, rasa, dan bahan tidak boleh kosong.",
				"Input Tidak Lengkap",
				MessageBoxButtons::OK,
				MessageBoxIcon::Warning);
			return;
		}

		// --- INI BAGIAN PINTARNYA (POIN 4) ---
		// 3. Bersihkan/Normalkan input bahan
		// Kita gunakan parser yang sama persis dengan di MainForm
		array<Char>^ delimiters = { ',', '.', '\r', '\n', ' ' };
		array<String^>^ bahanArray =
			bahanInputKotor->Split(delimiters, StringSplitOptions::RemoveEmptyEntries);

		// Satukan kembali array yang sudah bersih menjadi SATU string
		// dipisahkan oleh koma yang konsisten.
		String^ bahanBersih = String::Join(",", bahanArray);
		// --- AKHIR BAGIAN PINTAR ---


		// 4. Format data baru untuk disimpan
		String^ namaFile = "feedback.txt";
		// Format baru: Jauh lebih bersih dan mudah dibaca!
		String^ dataUntukDisimpan =
			"Nama Menu: " + namaMenu + "\r\n" +
			"Rasa: " + rasa + "\r\n" + // <-- Data baru
			"Bahan: " + bahanBersih + "\r\n" + // <-- Data bersih
			"--- FEEDBACK BARU ---" + "\r\n\r\n"; // Pemisah

		// 5. Tulis ke file
		try
		{
			StreamWriter^ writer = File::AppendText(namaFile);
			writer->Write(dataUntukDisimpan);
			writer->Close();

			MessageBox::Show("Terima kasih! Feedback Anda telah disimpan.",
				"Feedback Terkirim",
				MessageBoxButtons::OK,
				MessageBoxIcon::Information);

			this->Close();
		}
		catch (Exception^ ex)
		{
			MessageBox::Show("Terjadi error saat menyimpan: " + ex->Message,
				"Error",
				MessageBoxButtons::OK,
				MessageBoxIcon::Error);
		}
	}
	private: System::Void btnBatal_Click(System::Object^ sender, System::EventArgs^ e) {
		this->Close();
	}
};
}
