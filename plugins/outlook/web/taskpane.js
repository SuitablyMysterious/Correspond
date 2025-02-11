// Ensure Office.js is ready before using any Office APIs.
Office.onReady((info) => {
    if (info.host === Office.HostType.Outlook) {
      // Attach an event listener to the button with ID "generateDraft"
      document.getElementById("generateDraft").addEventListener("click", generateDraft);
    }
  });
  
  async function generateDraft() {
    // For demonstration purposes, we use a static email text.
    // In production, you might extract content from the currently selected email.
    const emailContent = "This is a sample email that requires a reply.";
  
    try {
      // Call the Python backend API (adjust URL as necessary)
      const response = await fetch("http://localhost:5000/generate_reply", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: emailContent })
      });
  
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
  
      const data = await response.json();
  
      // Use the Office JS API to insert the generated reply into the email body.
      Office.context.mailbox.item.body.setSelectedDataAsync(
        data.reply,
        { coercionType: Office.CoercionType.Text },
        (asyncResult) => {
          if (asyncResult.status !== Office.AsyncResultStatus.Succeeded) {
            console.error("Error inserting reply:", asyncResult.error.message);
          }
        }
      );
    } catch (error) {
      console.error("Error generating draft:", error);
      // Optionally, show an error message in the UI.
    }
  }
  