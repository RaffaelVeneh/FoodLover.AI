#pragma once
#pragma once

#include <string>
#include <vector>

// Kita gunakan namespace .NET agar bisa dipakai di GUI
using namespace System;
using namespace System::Collections::Generic;

public ref class Menu {
public:
    String^ namaMenu;
    String^ preferensiRasa; // "pedas", "gurih", "manis"
    List<String^>^ bahan;

    // Constructor untuk memudahkan
    Menu(String^ nama, String^ rasa, List<String^>^ listBahan) {
        namaMenu = nama;
        preferensiRasa = rasa;
        bahan = listBahan;
    }
};