from service import AIDub
from service.util import _stitch_audio_to_video, _get_yt_transcripts, _translate_en_2_new_lang, _translated_tts, _combine_align_translated_audios, _download_youtube_video, _silent_youtube_video, _duration_of_audio

import os
import logging

REPO = os.getcwd()
def main():
    aidub = AIDub()
    
    youtube_url = "https://www.youtube.com/watch?v=G6nxVgoRnXM"
    
    # transcripts, end_times = _get_yt_transcripts(youtube_url)
    # logging.warn(f'Got transcripts = {transcripts[0:5]} and corresponding end times in millisec= {end_times[0:5]}')
    
    # translated_transcripts = _translate_en_2_new_lang(
    #     transcripts,
    #     'es'
    # )
    # logging.warn(f'Got translated transcripts = {translated_transcripts[0:5]}')
    
    # _translated_tts(translated_transcripts)
    # logging.warn(f'Generated audio clips in target language')
    
    # _combine_align_translated_audios(f'{REPO}/translated_audio_clips', end_times)
    # logging.warn(f'Combined the generated audio clips into a single audio file with alignment and saved as combined.wav')
    
    duration_in_sec = _duration_of_audio(f'{REPO}/combined.wav')
    # logging.warn(f'The duration of the generated audio file in seconds = {duration_in_sec}')
    
    _download_youtube_video(youtube_url)
    logging.warn(f'Downloaded the Youtube video as sample_video.mp4')
    
    video_file_path = f'{REPO}/sample_video.mp4'
    output_silent_video_path = f'{REPO}/silent.mp4'
    _silent_youtube_video(video_file_path, output_silent_video_path, duration_in_sec)
    logging.warn(f'Stripped audio from video, trimmed it to given length and saved in the specified path as silent.mp4')
    
    dubbed_video_path = f'{REPO}/dubbed_video.mp4'
    _stitch_audio_to_video(f'{REPO}/combined.wav', output_silent_video_path,dubbed_video_path)
    logging.warn(f'Stitched the audio onto the video and saved it at the specified location')


if __name__ == '__main__':
    main()
