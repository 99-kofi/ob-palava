from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
from app.services.translation_service import TranslationService
from app.services.tts_service import TTSService
from app.database import log_visit, log_translation, init_db, DB_NAME
import os
import sqlite3

main = Blueprint('main', __name__)

@main.route('/temp_audio/<path:filename>')
def serve_temp_audio(filename):
    return send_from_directory('/tmp/audio', filename)

# Initialize services
translation_service = TranslationService()
# Note: In production, dynamic path resolution might be needed depending on deployment
tts_path = os.path.join(os.getcwd(), 'app', 'static') 
tts_service = TTSService(tts_path)

# Ensure DB is ready
init_db()

@main.route('/')
def index():
    log_visit(request.headers.get('User-Agent'))
    return render_template('index.html')

@main.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    direction = data.get('direction', 'en_to_pidgin')
    variant = data.get('variant', 'ghana')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = translation_service.translate(text, direction, variant)
    
    # Log it
    log_translation(direction, variant, len(text))
    
    return jsonify(result)

@main.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text')
    direction = data.get('direction', 'en_to_pidgin')
    variant = data.get('variant', 'ghana')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    audio_url = tts_service.generate_audio(text, variant, direction)
    
    if audio_url:
        return jsonify({"audio_url": audio_url})
    else:
        return jsonify({"error": "TTS generation failed"}), 500

@main.route('/analytics/stats')
def stats():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM visits")
        visits = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM translations")
        translations = c.fetchone()[0]
        conn.close()
        return jsonify({"visits": visits, "translations": translations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
