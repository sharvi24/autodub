from googletrans import Translator
from moviepy.editor import VideoFileClip
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import ffmpeg
import json
import requests
from Bio.Align import PairwiseAligner
import librosa
from pydub import AudioSegment
import os

def _get_yt_transcripts(url: str):
    """ gets youtube transcripts using url

    Args:
        url (str): url

    Returns:
        str: transcripts
    """
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    video_id = query["v"][0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    N = len(transcript)
    all_text = []
    all_ends = []
    #all_ends = [0] * (N+1)
    for i in range(N):
        all_text.append(transcript[i]['text'])
        all_ends.append(transcript[i]['start']*1000)
        #all_ends.append(transcript[i]['duration'])
    return [all_text, all_ends]
    #     all_ends[i + 1] = all_ends[i] + transcript[i]['duration']
    # return [all_text, all_ends[1:]]


def _translate_en_2_new_lang(text: list, lang: str = 'es'):
    """_summary_

    Args:
        lang (str, optional): _description_. Defaults to 'es'.

    Returns:
        str: _description_
    """
    if text == []:
        return text
    translator = Translator()
    translated_text = []
    for text_sample in text:
        #import logging; logging.warn(f'text_sample = {text_sample}') 
        translated_text.append(translator.translate(text_sample, dest=lang).text)
    return translated_text
    

def _translated_tts(text: str):
    """_summary_

    Args:
        text (str): translated text
    """
    voice_id = '21m00Tcm4TlvDq8ikWAM'
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    i = 0 
    for text_sample in text:
        
        payload = {
            "text": text_sample,
            "voice_settings": {
                "stability": 0,
                "similarity_boost": 0 
                }
            }
        r = requests.post(url, data=json.dumps(payload))
        name = str(i) + ".wav"
        with open(name, mode='bx') as f:
            f.write(r.content)
        i += 1    
    return None


def _combine_align_translated_audios(audio_files_path: str, end_times: list):
    """_summary_

    Args:
        audio_files_path (str): _description_
        start_times (list): _description_
    """
    
    all_files = []
    for filename in os.listdir(audio_files_path):
        # Get the full path of the file
        all_files.append(os.path.join(audio_files_path, filename))
    
    # List of audio clip file paths
    clip_files = sorted(all_files)
    
    # Load each audio clip and store the start time in a list
    clips = []
    clip_files = clip_files[1:6]
    
    for clip_file in clip_files:
        clip = AudioSegment.from_file(clip_file)
        clips.append(clip)

    end_times = end_times[0:4]
    #end_times_in_milsec = [x * 1000 for x in end_times]

    # Combine the clips by appending them one after another
    combined_clip = clips[0]
    last_length = len(clips[0])
    
    clips = clips[1:]
    #print("all end times", end_times)
    print("all end times in milsec", end_times)
    
    for clip, end_time in zip(clips, end_times):
        print(last_length, end_time)
        if last_length >= end_time:
                combined_clip += clip
        else:
            print("inside adding silence")
            silence_duration = (end_time - last_length)  #### NOT SURE WHY 1000
            padded_clip =  clip + AudioSegment.silent(duration=silence_duration)
            combined_clip += padded_clip
            
        last_length = len(combined_clip)

    # Export the combined clip to a new audio file
    combined_clip.export('combined.wav', format='wav')
    
    
def _download_youtube_video(video_url):
    """_summary_

    Args:
        video_url (str): Youtube video URL

    Returns:
        _type_: _description_
    """
    # Create a YouTube object
    yt = YouTube(video_url)

    # Get the first stream (usually the highest quality)
    stream = yt.streams.get_highest_resolution()

    # Download the video to the current directory
    stream.download()
    return None


def _silent_youtube_video(video_file_path, output_silent_video_path):
    video = VideoFileClip(video_file_path)
    video_without_audio = video.without_audio()
    video_without_audio.write_videofile(output_silent_video_path)


def _stitch_audio_to_video(audio_file_path: str, silent_video_file_path: str, output_video_with_dub_path: str):
    """_summary_

    Args:
        audio_file_path (str): _description_
        video_file_path (str): _description_

    Returns:
        _type_: _description_
    """
    audio = ffmpeg.input(audio_file_path)
    video = ffmpeg.input(silent_video_file_path)
    ffmpeg.output(audio, video, output_video_with_dub_path).run()
    
    return None