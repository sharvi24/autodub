from service.util import _get_yt_transcripts

import unittest


class TestYoutubeTranscripts(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sample_url = 'https://www.youtube.com/watch?v=G6nxVgoRnXM'
    
    def test_youtube_transcripts_success(self):
        result = _get_yt_transcripts(self.sample_url)
        texts, start_times = result[0], result[1]
        self.assertEqual(type(texts), list)
        self.assertEqual(type(start_times), list)