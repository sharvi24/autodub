from service.util import _translate_en_2_new_lang

import unittest


class TestTranslateTexts(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sample_txt = 'hello'
    
    def test_translate_texts_success(self):
        result = _translate_en_2_new_lang(text=self.sample_txt, lang='es')
        self.assertEqual(result, 'hola')