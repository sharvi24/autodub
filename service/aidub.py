from util import (
    _get_yt_transcripts,
    _translate_en_2_new_lang,
    _translated_tts
)


class AIDub:
    def __init__(self) -> None:
        pass

    def dub(self, youtube_url, language):
        transcripts, start_times = _get_yt_transcripts(youtube_url)
        translated_transcripts = _translate_en_2_new_lang(
            transcripts, 
            language
        )
        audio = _translated_tts(translated_transcripts)
        # put audio on the video 
        
        return None
