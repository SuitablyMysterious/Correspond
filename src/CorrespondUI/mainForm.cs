using System.Windows.Forms;
using System.Drawing;

namespace CorrespondUI
{
    public class MainForm : Form
    {
        public MainForm()
        {
            // Initialize the form
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            // Form properties
            this.Text = "Correspond Dashboard";
            this.Width = 400;
            this.Height = 200;
            this.StartPosition = FormStartPosition.CenterScreen;

            // Create a welcome label
            Label welcomeLabel = new Label();
            welcomeLabel.Text = "Welcome to Correspond!";
            welcomeLabel.Font = new Font("Segoe UI", 16);
            welcomeLabel.AutoSize = true;
            // Center the label roughly
            welcomeLabel.Location = new Point((this.ClientSize.Width - welcomeLabel.Width) / 2, 60);
            welcomeLabel.TextAlign = ContentAlignment.MiddleCenter;
            
            // Use anchor or adjust location on resize if needed
            this.Controls.Add(welcomeLabel);
        }
    }
}
