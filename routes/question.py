
from models.request import QuestionType, Questions, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from fastapi import APIRouter

from config.database import db
from models.request import Request
# from question_generators.boolean_question import BooleanQuestion
from question_generators.mcq import MultipleChoiceQuestion
# from question_generators.fill_blank_question import FillBlankQuestion

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
        return JSONResponse(content={'status': HTTPStatus.CREATED, 'generated_questions': generated_questions})
    except:
        return JSONResponse(content={'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'content': f'An error occurred while generating the questions'})


@question_generator.post('/save-question')
async def save(request: Questions):
    try:
        # question = request.question
        # distractors = request.distractors
        # answer = request.answer
        # print(question, distractors, answer)
        await db.save(request)
        return JSONResponse(content={'status': HTTPStatus.ACCEPTED, 'content': 'Successfully saved questions'})
    except Exception as e:
        return JSONResponse(content={'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'content': str(e)})


@question_generator.get('/question')
async def questions():
    try:
        # question = request.question
        # distractors = request.distractors
        # answer = request.answer
        # print(question, distractors, answer)
        questions = await db.find()
        return JSONResponse(content={'status': HTTPStatus.ACCEPTED, 'content': questions})
    except Exception as e:
        return JSONResponse(content={'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'content': str(e)})
