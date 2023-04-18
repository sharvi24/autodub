from service import AIDub

from flask import Flask, request, jsonify, render_template

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
    status_code = aidub.dub(youtube_url, language)
    
    if status_code != 200:
        return jsonify({'error': "Failed"}), status_code
    else:
        #return jsonify({'result': "Successfully saved"})
        return render_template('stream.html', video_file='dubbed_video.mp4')


@app.route('/video', methods=['GET'])
def stream_video():
    return render_template('stream.html', video_file='dubbed_video.mp4')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
