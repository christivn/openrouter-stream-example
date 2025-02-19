from flask import Flask, request, jsonify, Response, render_template
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()  # Carga variables del .env

app = Flask(__name__)

# Configura el cliente de OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  # Usa una variable de entorno
)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Mensaje no proporcionado"}), 400

    def generate():
        try:
            response = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://tusitio.com",  # Opcional
                    "X-Title": "Chat con OpenRouter",       # Opcional
                },
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": user_message}],
                stream=True  # Habilita streaming
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(generate(), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
