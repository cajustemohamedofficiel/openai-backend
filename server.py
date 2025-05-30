from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from openai import OpenAIError
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400

        user_input = data["message"]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            timeout=15  # optional timeout for OpenAI call
        )

        return jsonify({"response": response.choices[0].message.content})

    except OpenAIError as e:
        return jsonify({"error": f"OpenAI error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] Name: {name}, Email: {email}, Message: {message}\n"

    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(log_entry)

    return "<h2>Thank you for your message!</h2><a href='/'>Back to site</a>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides this
    app.run(host="0.0.0.0", port=port, debug=True)
