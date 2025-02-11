using System;
using System.Windows.Forms;

namespace CorrespondUI
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            // Run your main form
            Application.Run(new MainForm());
        }
    }
}
