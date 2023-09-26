

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


class SpeechToText:
    @staticmethod
    def get_id(url):
        u_pars = urlparse(url)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            return quer_v[0]
        ids = u_pars.path.split('/')
        if ids:
            return ids[-1]

    @staticmethod
    def get_transcription_from_youtube(url):
        try:
            text = ''
            youtube_id = SpeechToText.get_id(url)
            transcription = YouTubeTranscriptApi.get_transcript(
                youtube_id, languages=['en', 'pt'])
            for s in transcription:
                text += ' ' + s['text']
            return text
        except:
            return f'Error ao tentar obter transcrição do vídeo'
