import turtle as t
import pandas as pd

WIDTH, HEIGHT = 1000, 1000
screen = t.Screen()
img = 'india-outline-map.gif'
screen.title('India states & union territories map'.title())
screen.setup(WIDTH, HEIGHT)
screen.addshape(img)
t.shape(img)

guessed_states = []
df = pd.read_csv('28_states_8_union_territories.csv')

while len(guessed_states) < 36:
    states_list = df.state.to_list()
    answer = screen.textinput(title=f'score : {len(guessed_states)}/{len(states_list)}'.title(),
                              prompt='guess the states answer'.title()).title()

    def Turtle_Draw(color, states):
        Turtle = t.Turtle()
        Turtle.begin_fill()
        Turtle.color(color)
        Turtle.fillcolor(color)
        Turtle.penup()
        state_text = states.iloc[0, 0]
        x_coordinate = states.iloc[0, 1]
        y_coordinate = states.iloc[0, 2]
        Turtle.goto(float(x_coordinate), float(y_coordinate))
        Turtle.write(state_text, font=("Verdana", 10, 'bold'))
        Turtle.end_fill()

    if answer in states_list:
        guessed_states.append(answer)
        answer_state = df[df['state'].isin([answer])]
        Turtle_Draw(color='green', states=answer_state)

    if answer == 'Exit':
        for guessed_answer in guessed_states:
            states_list.remove(guessed_answer)

        print('states you need to know😮 : '.title())
        for i in states_list:
            answer_not_known = df[df['state'].isin([i])]
            Turtle_Draw(color='red', states=answer_not_known)
            print('\t\t', i)
        break

t.mainloop()
