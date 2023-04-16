from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from googletrans import Translator

def _get_yt_transcripts(url: str):
    """ gets youtube transcripts using url

    Args:
        url (str): url

    Returns:
        str: transcripts
    """
    print(url)
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    video_id = query["v"][0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    all_text = []
    all_starts = []
    for i in range(len(transcript)):
        all_text.append(transcript[i]['text'])
        all_starts.append(transcript[i]['start'])
    return [all_text, all_starts]


def _translate_en_2_new_lang(text: list, lang: str = 'es'):
    """_summary_

    Args:
        lang (str, optional): _description_. Defaults to 'es'.

    Returns:
        str: _description_
    """
    if text == []:
        return text
    pass

    translator = Translator()
    translated_text = []
    for i in range(len(text)):
        translated_text.append(translator.translate(text[i], dest=lang).text)
    return translated_text
    


def _translated_tts(text: str):
    """_summary_

    Args:
        text (str): translated text
    """
    pass