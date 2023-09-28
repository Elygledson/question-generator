
from models.request import QuestionType, Request, Transcription
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile

from config.database import db
from models.request import Request
# from question_generators.fill_blank import FillBlankQuestion
# from question_generators.boolean_question import BooleanQuestion
from question_generators.mcq import MultipleChoiceQuestion
from question_generators.speech_to_text import SpeechToText

import PyPDF2
import io

router = APIRouter()


@router.post('/generate')
def generate(request: Request):
    text = request.text
    num = request.question_num
    question_type = request.type
    return handle(question_type, text, num)


@router.post('/transcription/questions')
def generate_questions_from_url(request: Transcription):
    url = request.url
    num = request.num
    question_type = request.type
    transcription = SpeechToText.get_transcription_from_youtube(url)
    return handle(question_type, transcription, num)


@router.post("/file/questions")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(content={"error": "Somente arquivos pdfs são permitidos"}, status_code=400)

    try:
        file_content = await file.read()
        pdfReader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = "".join([pdfReader.pages[i].extract_text()
                        for i in range(len(pdfReader.pages))])
        return ''
    except:
        return JSONResponse(content={"error": "Erro ao extrair informações do PDF"}, status_code=500)


def handle(question_type, text, num):
    generated_questions = []
    try:
        # if question_type == QuestionType.fill_blank_question:
        #     fill_blank_question = FillBlankQuestion()
        #     generated_questions = fill_blank_question.generate(text)
        # if question_type == QuestionType.boolean_question:
        #     boolean_question = BooleanQuestion()
        #     generated_questions = boolean_question.generate(
        #         text,  num)
        if question_type == QuestionType.multiple_choice_question:
            mcq_questions = MultipleChoiceQuestion()
            generated_questions = mcq_questions.generate(
                text, num)
        return JSONResponse(content={'questions': generated_questions})
    except:
        return JSONResponse(content={'content': 'Erro ao gerar as questões.'}, status_code=500)
