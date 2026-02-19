from flask import Flask, render_template, request, redirect, jsonify
from database import Database
import string
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
db = Database()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not db.get_url(code):
            return code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    short_code = generate_short_code()
    db.save_url(short_code, original_url)

    short_url = request.host_url + short_code
    return render_template('index.html', short_url=short_url, original_url=original_url)

@app.route('/<short_code>')
def redirect_url(short_code):
    url = db.get_url(short_code)
    if url:
        db.increment_clicks(short_code)
        return redirect(url)
    return render_template('index.html', error='Short URL not found'), 404

@app.route('/all')
def all_urls():
    urls = db.get_all_urls()
    return jsonify(urls)

@app.route('/stats/<short_code>')
def stats(short_code):
    data = db.get_stats(short_code)
    if data:
        return jsonify(data)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, port=port)
