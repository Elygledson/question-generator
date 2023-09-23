from typing import Optional
from pydantic import BaseModel
from enum import Enum


class QuestionType(str, Enum):
    multiple_choice_question = 'multiple_choice'
    fill_blank_question = 'fill_blank'
    boolean_question = 'boolean'


class Request(BaseModel):
    type: QuestionType
    text: str
    question_num: Optional[int] = 5


class Question(BaseModel):
    question: str
    options: list[str]
    answer: str


class Questions(BaseModel):
    questions: list[Question]


class Transcription(BaseModel):
    url: str
