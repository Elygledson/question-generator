
from models.request import QuestionType, Questions, Request, Transcription
from fastapi.responses import JSONResponse
from http import HTTPStatus
from fastapi import APIRouter

from config.database import db
from models.request import Request
# from question_generators.boolean_question import BooleanQuestion
from question_generators.mcq import MultipleChoiceQuestion
from question_generators.fill_blank import FillBlankQuestion
from question_generators.speech_to_text import SpeechToText

question_generator = APIRouter()


@question_generator.post('/generate')
def generate(request: Request):
    generated_questions = []
    text = request.text
    question_num = request.question_num
    question_type = request.type
    try:
        # if question_type == QuestionType.fill_blank_question:
        #     fill_blank_question = FillBlankQuestion()
        #     generated_questions = fill_blank_question.generate(text)
        # if question_type == QuestionType.boolean_question:
        #     boolean_question = BooleanQuestion()
        #     generated_questions = boolean_question.generate(
        #         text,  question_num)
        if question_type == QuestionType.multiple_choice_question:
            mcq_questions = MultipleChoiceQuestion()
            generated_questions = mcq_questions.generate(
                text, question_num)
        return JSONResponse(content={'generated_questions': generated_questions})
    except:
        return JSONResponse(status_code=500, content={'content': 'Erro ao gerar as questões.'})


@question_generator.get('/transcription/questions')
def generate_questions_from_url(request: Transcription):
    generated_questions = []
    url = request.url
    question_num = request.question_num
    question_type = request.type
    try:
        transcription = SpeechToText.get_transcription_from_youtube(url)
        # if question_type == QuestionType.fill_blank_question:
        #     fill_blank_question = FillBlankQuestion()
        #     generated_questions = fill_blank_question.generate(transcription)
        # if question_type == QuestionType.boolean_question:
        #     boolean_question = BooleanQuestion()
        #     generated_questions = boolean_question.generate(
        #         transcription,  question_num)
        if question_type == QuestionType.multiple_choice_question:
            mcq_questions = MultipleChoiceQuestion()
            generated_questions = mcq_questions.generate(
                transcription, question_num)
        return JSONResponse(content={'generated_questions': generated_questions})
    except:
        return JSONResponse(status_code=500, content={'content': 'Erro ao gerar as questões.'})


@question_generator.get('/transcription')
def get_transcriptio_from_url(request: Transcription):
    url = request.url
    transcription = SpeechToText.get_transcription_from_youtube(url)
    return JSONResponse(content={'status': HTTPStatus.ACCEPTED, 'transcription': transcription})


@question_generator.get('/question')
async def questions():
    try:
        questions = await db.find()
        return JSONResponse(content={'content': questions})
    except:
        return JSONResponse(status_code=500, content={'content': 'Erro ao buscar questões'})


@question_generator.post('/save-question')
async def save(request: Questions):
    try:
        await db.save(request)
        return JSONResponse(content={'content': 'Questões cadastradas.'})
    except:
        return JSONResponse(status_code=500, content={'content': str(e)})
