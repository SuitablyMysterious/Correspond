from flask import Flask, request, jsonify
from transformers import pipeline
import logging

# Set up logging to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the summarization pipeline
# (You can choose a different model if desired)
try:
    logger.info("Loading summarization pipeline...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    logger.info("Summarization pipeline loaded successfully.")
except Exception as e:
    logger.error(f"Error loading summarization pipeline: {e}")

# Initialize the text generation pipeline for generating replies.
# For now, we'll use a basic model (GPT-2) as an example.
try:
    logger.info("Loading text generation pipeline...")
    generator = pipeline("text-generation", model="gpt2")
    logger.info("Text generation pipeline loaded successfully.")
except Exception as e:
    logger.error(f"Error loading text generation pipeline: {e}")

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Expects JSON input with a "text" field containing the email text.
    Returns a JSON response with the summarized text.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400

    email_text = data.get("text", "")
    if not email_text:
        return jsonify({"error": "Missing 'text' field in JSON"}), 400

    try:
        # Adjust max_length and min_length as needed
        summary_output = summarizer(email_text, max_length=130, min_length=30, do_sample=False)
        summary_text = summary_output[0]["summary_text"]
        return jsonify({"summary": summary_text})
    except Exception as e:
        logger.error(f"Summarization error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate_reply', methods=['POST'])
def generate_reply():
    """
    Expects JSON input with a "text" field containing the email text.
    Returns a JSON response with a generated draft reply.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400

    email_text = data.get("text", "")
    if not email_text:
        return jsonify({"error": "Missing 'text' field in JSON"}), 400

    try:
        # Create a prompt to guide the generation.
        prompt = f"Reply to the following email in a professional tone:\n\nEmail: {email_text}\n\nReply:"
        # Generate text. Adjust max_length to control the reply length.
        reply_output = generator(prompt, max_length=150, num_return_sequences=1)
        generated_text = reply_output[0]["generated_text"]
        return jsonify({"reply": generated_text})
    except Exception as e:
        logger.error(f"Reply generation error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app. In production, consider using a WSGI server.
    app.run(host='0.0.0.0', port=5000, debug=True)
