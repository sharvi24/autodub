from service import AIDub
from service.util import _stitch_audio_to_video, _get_yt_transcripts, _translate_en_2_new_lang, _translated_tts, _combine_align_translated_audios, _download_youtube_video, _silent_youtube_video, _duration_of_audio


def main():
    aidub = AIDub()
   
    # youtube_url = "https://www.youtube.com/watch?v=G6nxVgoRnXM"
    
    # transcripts, all_ends = _get_yt_transcripts(youtube_url)
    
    #translated_transcripts = _translate_en_2_new_lang(transcripts)
    #_translated_tts(translated_transcripts)
    
    #_combine_align_translated_audios("/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/translated_audio_clips",all_ends)
    audio_file_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/combined.wav"
    # duration_in_sec = _duration_of_audio(audio_file_path)
    
    #_download_youtube_video(youtube_url)
    
    #video_file_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/sample_video.mp4"
    output_silent_video_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/silent.mp4"
    # _silent_youtube_video(video_file_path, output_silent_video_path, duration_in_sec)
    
    dubbed_video_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/dubbed_video.mp4"
    _stitch_audio_to_video(audio_file_path, output_silent_video_path,dubbed_video_path)


if __name__ == '__main__':
    main()
