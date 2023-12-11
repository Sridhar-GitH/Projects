import sys
from random import *
from Instagram_followers_data import data
from logo import logo, Vs
from replit import clear


def statements(account):
    """the function return the statement"""
    name = account['name']
    description = account['description']
    country = account['country']
    return f"'{name}' is a {description} from {country} ".title()


def Higher_Lower():
    """the game function was calling in while loop"""
    person_a = choice(data)
    person_b = choice(data)

    def check(a, b):
        """checking no of follower count and returns"""
        if a >= b:
            return 'a'
        elif b >= a:
            return 'b'

    Game_over = False
    score = 0
    while not Game_over:
        clear()
        print(logo)
        print(f'compare A: {statements(person_a)}'.title())
        print(Vs)
        print(f'Against B: {statements(person_b)}'.title())

        a_followers = person_a['follower_count']
        b_followers = person_b['follower_count']

        answer = input('\nwhich one has more followers: "person_a" or "person_b" :- '.title()).lower()

        if answer == check(a_followers, b_followers) or a_followers == b_followers:
            score += 1
            print(f'\nyour right! your score : {score}'.title())
            person_a = person_b
            person_b = choice(data)

        elif answer != check(a=a_followers, b=b_followers):
            Game_over = True
            print('you lose :('.upper())


continue_ = True
while continue_:
    if input('do you want to play the game Higher_Lower [y/n]: '.title()).lower() == 'y':
        Higher_Lower()
    else:
        sys.exit('Good Play ;)')
