from question_model import Question
from quiz_brain import QuizBrain
import requests

parameter = {
    'amount': 25,
    'category': 17,
    'type': 'boolean'
}

response = requests.get('https://opentdb.com/api.php', params=parameter)
response.raise_for_status()
data = response.json()
question_data = data['results']

question_bank = []
for question in question_data:
    text = question['question']
    answer = question['correct_answer']
    question_obj = Question(text, answer)
    question_bank.append(question_obj)

quiz = QuizBrain(question_bank)

print(f'There is {parameter['amount']} Questions and Test your Brain ;)')
while quiz.still_has_questions():
    quiz.next_question()
print(f'\nyou completed the quiz \nyour final score was : {quiz.score}/{quiz.question_number}'.title())
