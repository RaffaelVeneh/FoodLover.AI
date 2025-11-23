#pragma once
using namespace System;
using namespace System::Collections::Generic;

namespace FoodLover {

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
}