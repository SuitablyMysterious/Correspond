using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;

namespace CorrespondUI
{
    public class MainForm : Form
    {
        private TextBox txtEmailContent;
        private Button btnSummarize;
        private TextBox txtSummary;

        public MainForm()
        {
            // Set up the form properties
            this.Text = "Correspond UI";
            this.Width = 800;
            this.Height = 600;

            // Create and position a label for the email content
            Label lblEmailContent = new Label()
            {
                Text = "Email Content:",
                Top = 20,
                Left = 20,
                Width = 100
            };
            this.Controls.Add(lblEmailContent);

            // Create a multiline textbox for email content
            txtEmailContent = new TextBox()
            {
                Top = lblEmailContent.Bottom + 5,
                Left = 20,
                Width = 740,
                Height = 150,
                Multiline = true,
                ScrollBars = ScrollBars.Vertical
            };
            this.Controls.Add(txtEmailContent);

            // Create a button to trigger summarization
            btnSummarize = new Button()
            {
                Text = "Summarize",
                Top = txtEmailContent.Bottom + 10,
                Left = 20,
                Width = 100
            };
            btnSummarize.Click += async (sender, e) => await BtnSummarize_Click(sender, e);
            this.Controls.Add(btnSummarize);

            // Create and position a label for the summary
            Label lblSummary = new Label()
            {
                Text = "Summary:",
                Top = btnSummarize.Bottom + 10,
                Left = 20,
                Width = 100
            };
            this.Controls.Add(lblSummary);

            // Create a multiline textbox to display the summary
            txtSummary = new TextBox()
            {
                Top = lblSummary.Bottom + 5,
                Left = 20,
                Width = 740,
                Height = 150,
                Multiline = true,
                ScrollBars = ScrollBars.Vertical,
                ReadOnly = true
            };
            this.Controls.Add(txtSummary);
        }

        // Event handler for the Summarize button click
        private async Task BtnSummarize_Click(object sender, EventArgs e)
        {
            string emailText = txtEmailContent.Text;
            if (string.IsNullOrWhiteSpace(emailText))
            {
                MessageBox.Show("Please enter email content to summarize.");
                return;
            }

            // Prepare to call the Python LLM backend
            using (HttpClient client = new HttpClient())
            {
                // Create the JSON payload
                var payload = new { text = emailText };
                string json = JsonConvert.SerializeObject(payload);
                StringContent content = new StringContent(json, Encoding.UTF8, "application/json");

                try
                {
                    // Call the /summarize endpoint (adjust the URL if needed)
                    HttpResponseMessage response = await client.PostAsync("http://localhost:5000/summarize", content);
                    response.EnsureSuccessStatusCode();

                    // Read and deserialize the response
                    string responseBody = await response.Content.ReadAsStringAsync();
                    dynamic result = JsonConvert.DeserializeObject(responseBody);

                    // Display the summary
                    txtSummary.Text = result.summary;
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error: " + ex.Message);
                }
            }
        }
    }
}
