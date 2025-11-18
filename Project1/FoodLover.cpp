#include "MainForm.h" 

using namespace System;
using namespace System::Windows::Forms;

// Namespace ini harus sama dengan yang ada di MainForm.h
namespace FoodLover {

    [STAThread]
    int main(array<System::String^>^ args) {
        Application::EnableVisualStyles();
        Application::SetCompatibleTextRenderingDefault(false);

        // Sekarang compiler bisa menemukan MainForm di dalam FoodLover
        FoodLover::MainForm^ form = gcnew FoodLover::MainForm();

        Application::Run(form);

        return 0;
    }
}