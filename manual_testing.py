from service import AIDub
from service.util import _stitch_audio_to_video, _get_yt_transcripts, _translate_en_2_new_lang, _translated_tts, _combine_align_translated_audios

def main():
    aidub = AIDub()
    # video = aidub.dub(
    #     'https://www.youtube.com/watch?v=G6nxVgoRnXM',
    #     'es'
    # )
    
    youtube_url = "https://www.youtube.com/watch?v=G6nxVgoRnXM"
    transcripts, all_ends = _get_yt_transcripts(youtube_url)
    # print(len(transcripts), len(all_ends))
    # print(transcripts[0:5])
    # print(all_ends[0:5])
    # print(transcripts[-1])
    # print(all_ends[-1])
    # translated_transcripts = _translate_en_2_new_lang(transcripts)
    # _translated_tts(translated_transcripts)
    _combine_align_translated_audios("/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/few_audios",all_ends)
    
    # audio_file_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/sample_audio.mp3"
    # video_file_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/sample_video.mp4"
    # silent_video_file_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/silent.mp4"
    # output_silent_video_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/silent.mp4"
    # output_video_with_dub_path = "/Users/sharvitomar/Desktop/Sem4/deeptune/Autodub/final.mp4"
    # _stitch_audio_to_video(audio_file_path, silent_video_file_path)
        
        
if __name__ == '__main__':
    main()