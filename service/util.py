from googletrans import Translator
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from pytube import YouTube
from service.util_constants import *
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

import ffmpeg
import glob
import json
import librosa
import os
import requests


REPO = os.getcwd()


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
    for i in range(N):
        all_text.append(transcript[i]['text'])
        all_ends.append(transcript[i]['start']*1000)
    return [all_text, all_ends]


def _translate_en_2_new_lang(text: list, lang: str = 'es'):
    """Translates transcriptions/text to target language

    Args:
        text (list): List of transcriptions/text
        lang (str, optional): Target language of conversion. Defaults to 'es'.

    Returns:
        str: List of translated transcriptions/text
    """
  
    if text == []:
        return text
    translator = Translator()
    translated_text = []
    for text_sample in text:
        translated_text.append(
            translator.translate(text_sample, dest=lang).text)
    return translated_text


def _get_voice_from_video(video_file):
    url = f'https://api.elevenlabs.io/v1/voices/add'
    payload = {
            "name": "yeonmi_park",
            "files": video_file
        }
    r = requests.post(url,
                      headers={"xi-api-key": XI_API_KEY},
                      data=json.dumps(payload))
    return r.content


def _translated_tts(text: list):
    """Generates and writes audio clips for the given list of texts

    Args:
        text (list): list of translated text
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
        r = requests.post(url,
                          headers={"xi-api-key": XI_API_KEY},
                          data=json.dumps(payload))
        file_name = f'{REPO}/translated_audio_clips/{str(i)}.wav'
        with open(file_name, mode='bx') as f:
            f.write(r.content)
        i += 1
    return None


def _combine_align_translated_audios(audio_files_path: str, end_times: list):
    """Combines the audio clips into a single wav file

    Args:
        audio_files_path (str): path to the audio clips
        end_times (list): list of end times of transcriptions for each clip
           
    """

    clip_files = sorted(
        glob.glob(f'{REPO}/translated_audio_clips/*.wav'),
        key=os.path.getmtime
    )
    # clip_files = clip_files[0:63]
    # end_times = end_times[0:63]
    clip_files = clip_files[0:4]
    end_times = end_times[0:4]    
    # # Load each audio clip and store the start time in a list
    clips = []

    for clip_file in clip_files:
        clip = AudioSegment.from_file(clip_file)
        clips.append(clip)

    # Combine the clips by appending them one after another
    combined_clip = clips[0]
    last_length = len(clips[0])

    clips = clips[1:]

    for clip, end_time in zip(clips, end_times):
        #print(last_length, end_time)
        if last_length >= end_time:
            combined_clip += clip
        else:
            #print("inside adding silence")
            silence_duration = (end_time - last_length)
            padded_clip = clip + AudioSegment.silent(duration=silence_duration)
            combined_clip += padded_clip

        last_length = len(combined_clip)

    # Export the combined clip to a new audio file
    combined_clip.export('combined.wav', format='wav')


def _duration_of_audio(audio_file):
    """Returns the duration in seconds of the given audio file

    Args:
        audio_file (str): path to the audio file

    Returns:
        float: duration in seconds of the given audio file
    """
    return librosa.get_duration(filename= audio_file)


def _download_youtube_video(video_url):
    """Download the Youtube video from its URL

    Args:
        video_url (str): Youtube video URL
    """
    # Create a YouTube object
    yt = YouTube(video_url)

    # Get the first stream (usually the highest quality)
    stream = yt.streams.get_highest_resolution()

    # Download the video to the current directory
    stream.download(filename="sample_video.mp4")


def _silent_youtube_video(video_file_path, output_silent_video_path, duration_in_sec):
    """Strips audio from the video, trims to the given length and saves in the specified path

    Args:
        video_file_path (str): path to the video file
        output_silent_video_path (str): output path of the silenced video
        duration_in_sec (float): duration of video to keep
    """
    video = VideoFileClip(video_file_path)
    # Trim the first 5 seconds of the video
    video = video.subclip(0, duration_in_sec)
    video_without_audio = video.without_audio()
    video_without_audio.write_videofile(output_silent_video_path)


def _stitch_audio_to_video(audio_file_path: str, silent_video_file_path: str, dubbed_video_path: str):
    """Stitches the audio onto the video and saves at the specified location

    Args:
        audio_file_path (str): path to the audio file
        silent_video_file_path (str): path to the video file
        dubbed_video_path (str): path of the combined video to write
    """
    audio = AudioFileClip(audio_file_path)
    video = VideoFileClip(silent_video_file_path)
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(dubbed_video_path)


