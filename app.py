from service import AIDub

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome!"


@app.route('/dub', methods=['POST'])
def dub_video():
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    language = data.get('language')
    if not youtube_url:
        return jsonify({'error': 'No youtube url specified'}), 400

    if not language:
        return jsonify({'error': 'No language specified'}), 400
    aidub = AIDub()
    video = aidub.dub(youtube_url, language)
    # save video


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
