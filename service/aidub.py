from service.util import (
    _get_yt_transcripts,
    _translate_en_2_new_lang,
    _translated_tts,
    _download_youtube_video,
    _stitch_audio_to_video
)

import logging

class AIDub:
    def __init__(self) -> None:
        pass

    def dub(self, youtube_url, language):
        transcripts, start_times = _get_yt_transcripts(youtube_url)
        # logging.warn(f'Got transcripts = {transcripts}')
        translated_transcripts = _translate_en_2_new_lang(
            transcripts, 
            language
        )
        # logging.warn(f'Got translated transcripts = {translated_transcripts}')
        audio = _translated_tts(translated_transcripts[0])
        
        # download the video 
        # video_url = "https://www.youtube.com/watch?v=FUiu-cdu6mA"
        # _download_youtube_video(video_url)
        
        # put audio on the video 
        audio_file_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/sample_audio.mp3"
        video_file_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/sample_video.mp4"
        _stitch_audio_to_video(audio_file_path, video_file_path)
        
        return None
