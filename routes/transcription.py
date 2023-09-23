from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.request import Transcription

from question_generators.transcription_generator import SpeechToText


transcription_generator = APIRouter()


@transcription_generator.get('/transcription')
def get_transcription(request: Transcription):
    url = request.url
    transcription = SpeechToText.get_transcription_from_youtube(url)
    return JSONResponse(content={'status': HTTPStatus.ACCEPTED, 'transcription': transcription})
