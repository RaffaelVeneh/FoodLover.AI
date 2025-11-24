#pragma once

using namespace System;
using namespace System::Net;
using namespace System::Text;
using namespace System::Windows::Forms;

namespace FoodLover {

	public ref class ApiService {
	private:
		String^ BASE_URL = "http://127.0.0.1:5000";

	public:
		ApiService() {}

		// TRIGGER TRAINING (GET)
		void LatihAi(DownloadStringCompletedEventHandler^ handler) {
			try {
				WebClient^ client = gcnew WebClient();
				client->DownloadStringCompleted += handler;
				client->DownloadStringAsync(gcnew Uri(BASE_URL + "/latih-ulang"));
			}
			catch (Exception^ ex) {
				Console::WriteLine("Error ApiService: " + ex->Message);
			}
		}

		// CARI RESEP (POST)
		void CariResep(String^ bahan, String^ rasa, String^ kategori, UploadStringCompletedEventHandler^ handler) {
			try {
				String^ url = BASE_URL + "/cari";

				// Sanitasi Input sederhana
				String^ bahanAman = bahan->Replace("\r\n", " ")->Replace("\n", " ")->Replace("\"", "");

				String^ jsonKirim = String::Format(
					"{{\"bahan\": \"{0}\", \"rasa\": \"{1}\", \"kategori\": \"{2}\"}}",
					bahanAman, rasa, kategori
				);

				WebClient^ client = gcnew WebClient();
				client->Headers->Add("Content-Type", "application/json");
				client->Encoding = System::Text::Encoding::UTF8;
				client->UploadStringCompleted += handler;

				client->UploadStringAsync(gcnew Uri(url), "POST", jsonKirim);
			}
			catch (Exception^ ex) {
				Console::WriteLine("Error Request Cari: " + ex->Message);
			}
		}

		// POST - Fire & Forget
		void CatatPilihan(String^ inputUser, String^ rasaInput, String^ menuDipilih) {
			try {
				// Hitung waktu
				int jam = DateTime::Now.Hour;
				String^ waktuSekarang = "malam";
				if (jam >= 5 && jam < 11) waktuSekarang = "pagi";
				else if (jam >= 11 && jam < 15) waktuSekarang = "siang";
				else if (jam >= 15 && jam < 19) waktuSekarang = "sore";

				String^ url = BASE_URL + "/catat-pilihan";

				// Sanitasi
				String^ inputAman = inputUser->Replace("\n", " ")->Replace("\"", "");
				String^ menuAman = menuDipilih;

				String^ jsonLog = String::Format(
					"{{"
					"\"input_user\": \"{0}\", "
					"\"rasa_input\": \"{1}\", "
					"\"menu_dipilih\": \"{2}\", "
					"\"waktu_akses\": \"{3}\", "
					"\"timestamp\": \"{4}\""
					"}}",
					inputAman, rasaInput, menuAman, waktuSekarang, DateTime::Now.ToString("yyyy-MM-dd HH:mm:ss")
				);

				WebClient^ client = gcnew WebClient();
				client->Headers->Add("Content-Type", "application/json");
				client->UploadStringAsync(gcnew Uri(url), "POST", jsonLog);
			}
			catch (Exception^ ex) {
				Console::WriteLine("Gagal Log: " + ex->Message);
			}
		}

		void TambahResep(String^ nama, String^ rasa, String^ bahan, String^ kategori, String^ waktu, UploadStringCompletedEventHandler^ handler) {
			try {
				String^ url = BASE_URL + "/tambah";
				String^ bahanAman = bahan->Replace("\r\n", " ")->Replace("\n", " ")->Replace("\"", "");
				String^ namaAman = nama->Replace("\"", "");

				String^ jsonKirim = String::Format(
					"{{"
					"\"nama\": \"{0}\", \"rasa\": \"{1}\", \"bahan\": \"{2}\", "
					"\"kategori\": \"{3}\", \"waktu\": \"{4}\""
					"}}",
					namaAman, rasa, bahanAman, kategori, waktu
				);

				WebClient^ client = gcnew WebClient();
				client->Headers->Add("Content-Type", "application/json");
				client->Encoding = System::Text::Encoding::UTF8;

				if (handler != nullptr) {
					client->UploadStringCompleted += handler;
				}

				client->UploadString(gcnew Uri(url), "POST", jsonKirim);
			}
			catch (Exception^ ex) {
				throw ex; 
			}
		}
	};
}