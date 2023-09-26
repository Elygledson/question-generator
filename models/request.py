from pydantic import BaseModel, Field
from enum import Enum


class QuestionType(str, Enum):
    multiple_choice_question = 'multiple_choice'
    fill_blank_question = 'fill_blank'
    boolean_question = 'boolean'


class Request(BaseModel):
    type: QuestionType = Field(description='Tipo de questão a ser gerada')
    text: str = Field(
        description='Texto a ser usado para geração das questões')
    question_num: int = Field(
        default=3, description="Quantidade de questões a serem geradas")


class Question(BaseModel):
    question: str
    options: list[str]
    answer: str


class Questions(BaseModel):
    questions: list[Question]


class Transcription(BaseModel):
    url: str
    type: QuestionType = Field(description='Tipo de questão a ser gerada')
    question_num: int = Field(
        default=3, description="Quantidade de questões a serem geradas")
