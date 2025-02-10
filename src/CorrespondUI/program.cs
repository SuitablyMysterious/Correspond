using System;
using System.Windows.Forms;

namespace CorrespondUI
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            // Configure application settings
            Application.SetHighDpiMode(HighDpiMode.SystemAware);
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            // Run the main form
            Application.Run(new MainForm());
        }
    }
}