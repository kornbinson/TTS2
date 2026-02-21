from quart import Quart, request, send_file, jsonify
import edge_tts
import io
import os

app = Quart(__name__)

# Configura tu clave API aquí o mediante variables de entorno (recomendado)
API_KEY = os.getenv("MY_API_KEY", "tu_clave_super_secreta_123")

@app.route('/generate', methods=['POST'])
async def generate():
    # 1. Verificación de Seguridad (API KEY)
    auth_key = request.headers.get("x-api-key")
    if auth_key != API_KEY:
        return jsonify({"error": "No autorizado. API Key inválida."}), 401

    # 2. Recibir datos
    data = await request.get_json()
    if not data:
        return jsonify({"error": "No se recibió cuerpo JSON"}), 400

    text = data.get('text', '')
    voice = data.get('voice', 'es-AR-TomasNeural')
    rate = data.get('rate', '+0%')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # 3. Generar el audio en memoria
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        audio_data = b""
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]

        audio_buffer = io.BytesIO(audio_data)
        audio_buffer.seek(0)

        return await send_file(
            audio_buffer, 
            mimetype="audio/mpeg", 
            download_name="audio.mp3"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500