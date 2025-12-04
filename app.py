import os
import time
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    model = data.get("model", "amazon/nova-2-lite-v1:free")
    history = data.get("history", [])
    temperature = data.get("temperature")
    max_tokens = data.get("max_tokens")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if not OPENROUTER_API_KEY:
        return jsonify({"error": "OpenRouter API key not configured in .env file"}), 500

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Local Chat App",
    }

    # Construct messages including history if you want context (simple version just sends current message for now, but better to include history for chat)
    # The prompt implies a basic chat interface. I'll implement it to send the conversation history if the frontend provides it,
    # or just the last message if I want to keep it simple. Let's start with just sending the user message as a single turn for simplicity
    # unless I build a full history manager in the frontend.
    # Let's assume the frontend sends the current message, and maybe I should append it to a list of messages.
    # Actually, for a chat app, usually we want context.
    # I'll update the frontend to keep track of history, and here I will accept a list of messages.

    # However, to keep it robust:
    messages = history + [{"role": "user", "content": user_message}]

    payload = {
        "model": model,
        "messages": messages
    }

    if temperature:
        try:
            payload["temperature"] = float(temperature)
        except ValueError:
            pass

    if max_tokens:
        try:
            payload["max_tokens"] = int(max_tokens)
        except ValueError:
            pass

    response = None
    try:
        start_time = time.time()
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        end_time = time.time()

        response.raise_for_status()
        result = response.json()

        if 'choices' in result and len(result['choices']) > 0:
            bot_message = result['choices'][0]['message']['content']

            # Extract metrics
            usage = result.get('usage', {})
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_time = end_time - start_time

            tokens_per_second = 0
            if total_time > 0:
                tokens_per_second = completion_tokens / total_time

            metrics = {
                "input_tokens": prompt_tokens,
                "output_tokens": completion_tokens,
                "total_time": round(total_time, 3),
                "tokens_per_second": round(tokens_per_second, 2)
            }

            return jsonify({
                "reply": bot_message,
                "metrics": metrics
            })
        else:
             return jsonify({"error": "Invalid response from OpenRouter"}), 500

    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if response:
            try:
                if response.content:
                    error_data = response.json()
                    if "error" in error_data:
                        if isinstance(error_data["error"], dict):
                            error_msg = error_data["error"].get("message", str(e))
                        else:
                            error_msg = str(error_data["error"])
            except:
                pass
        return jsonify({"error": f"OpenRouter API Error: {error_msg}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
