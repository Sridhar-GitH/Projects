import html


class QuizBrain:

    def __init__(self, q_list):
        self.current_question = None
        self.question_list = q_list
        self.question_number = 0
        self.score = 0

    def still_has_questions(self):
        """the function checks end of question and return boolean"""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """the function ask and get user input and call check_answer() --> method"""
        self.current_question = self.question_list[self.question_number]
        question_text = html.unescape(self.current_question.text)

        self.question_number += 1
        user = input(f'\nQ.{self.question_number}: {question_text} (True/False) : '.title()).lower()
        self.check_answer(user, self.current_question.answer)

    def check_answer(self, user, answer):
        """the function check the user input and actual answer"""
        if user == answer.lower():
            self.score += 1
            print("You're right! :)".title())
        else:
            print("that's wrong".title())
        print(f'the correct answer is : {answer}'.title())
        print(f"you're current score : {self.score}/{self.question_number}".title())
