import json
from random import choice

used_questions = set()


def retrieve_questions(directory: str) -> list:
    with open(directory, 'r') as file:
        questions = json.load(file)
    return questions


def get_question(questions: list) -> dict:
    global used_questions
    unique_questions = [q for q in questions if q['question'] not in used_questions]
    if not unique_questions:
        used_questions.clear()
        unique_questions = questions
    question = choice(unique_questions)
    used_questions.add(question['question'])
    return question


def check_answer(question: dict, answer: str) -> bool:
    return question['answer'].strip().lower() == answer.strip().lower()


