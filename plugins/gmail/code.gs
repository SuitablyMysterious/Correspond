/**
 * Builds the initial card for the Gmail add-on.
 */
function buildAddOn(e) {
  return CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle("Correspond Draft Generator"))
    .addSection(
      CardService.newCardSection()
        .addWidget(
          CardService.newTextInput()
            .setFieldName("emailContent")
            .setTitle("Email Content")
            .setHint("Enter or paste email content")
        )
        .addWidget(
          CardService.newTextButton()
            .setText("Generate Draft Reply")
            .setOnClickAction(CardService.newAction().setFunctionName("generateDraft"))
        )
    )
    .build();
}

/**
 * Handles the button click to generate a draft reply.
 */
function generateDraft(e) {
  var emailContent = e.formInput.emailContent;
  
  // Set up options for the POST request to your Python backend.
  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify({ text: emailContent })
  };
  
  // Make the HTTP request. Update the URL to your backend's endpoint.
  var response = UrlFetchApp.fetch("https://yourdomain.com/generate_reply", options);
  var result = JSON.parse(response.getContentText());
  
  // Create a new card to display the generated draft reply.
  var replyCard = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle("Draft Reply"))
    .addSection(
      CardService.newCardSection()
        .addWidget(
          CardService.newTextParagraph().setText(result.reply)
        )
    )
    .build();
  
  return CardService.newActionResponseBuilder()
    .setNavigation(CardService.newNavigation().pushCard(replyCard))
    .build();
}

/**
 * This function is the entry point for the add-on.
 */
function getContextualAddOn(e) {
  return buildAddOn(e);
}
