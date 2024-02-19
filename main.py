import telebot
from telebot import types
from itertools import *


class collage(object):
    def __init__(self, name, balls, subjects, description):
        self.name = name
        self.balls = balls
        self.subjects = subjects
        self.description = description

    def can_be(self, our_subjects, our_balls):
        for i in permutations(our_subjects, r=2):
            if sorted(self.subjects) == sorted(i) and our_balls >= self.balls:
                return True
        return False


collages = [collage('МИСИС', 250, ('math_p', 'inf'), 'norm VUZ1'),
                collage('BAD', 100, ('math_p', 'phis'), 'norm VUZ2')]

bot = telebot.TeleBot('7019813202:AAG-TNA5l12ZC-244jw223iqQ2jT05shJPI');

names_subjects = {
    'math_p': ('математика профильная', 'математика профиль'),
    'math_b': ('математика базовая', 'математика база'),
    'phis': ('физика'),
    'inf': ('информатика'),
    'hist': ('история')
}
subjects_math = {
    'math_p':'Математика профиль',
    'math_b':'Математика база'
}
subjects_other = {
    'phis': 'Физика',
    'inf': 'Информатика',
    'hist': 'История',
    'soc': 'Обществознание',
    'bio': 'Биология',
    'chem': 'Химия',
    'geo': 'География',
    'eng': 'Английский',
    'liter': 'Литература'
}

user_data = []
user_data_balls = 0
count = 0
count_with_balls = 0
queue_out = 0
id_user = ''
listV = []
balls_input = False

@bot.message_handler(content_types=['text'])
def f(message):
    global user_data
    global queue_out
    global id_user
    global balls_input
    id_user = message.from_user.id

    keyboard_math = types.InlineKeyboardMarkup()
    keyboard_other = types.InlineKeyboardMarkup()
    keyboard_answer = types.InlineKeyboardMarkup()
    keyboard_answerBalls = types.InlineKeyboardMarkup()
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='55+', callback_data='55'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='70+', callback_data='70'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='85+', callback_data='85'))
    key = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard_answer.add(key)
    key = types.InlineKeyboardButton(text='Посмотрю еще предметы', callback_data='no')
    keyboard_answer.add(key)

    for i in subjects_other:
        if i not in user_data:
            key = types.InlineKeyboardButton(text=subjects_other[i], callback_data=i)
            keyboard_other.add(key)
    for i in subjects_math:
        key = types.InlineKeyboardButton(text=subjects_math[i], callback_data=i)
        keyboard_math.add(key)

    if queue_out == 0: bot.send_message(id_user, text=f'ur id: {message.from_user.id}\nuser data: {user_data}',
                              reply_markup=keyboard_math)
    elif queue_out == 1: bot.send_message(id_user, text=f'ur id: {message.from_user.id}\nuser data: {user_data}',
                              reply_markup=keyboard_other)
    elif queue_out == 2: bot.send_message(id_user, text=f'Это все? У нас тут {count} результатов. Взглянешь?',
                              reply_markup=keyboard_answer)
    elif queue_out == 3: bot.send_message(id_user, text='На сколько баллов метишь? Можешь написать сам:',
                         reply_markup=keyboard_answerBalls)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global queue_out
    global user_data
    global balls_input
    global id_user
    global listV
    global user_data_balls

    if call.data in subjects_math:
        queue_out = 1
        user_data.append(call.data)
    elif call.data in subjects_other:
        queue_out = 2
        user_data.append(call.data)
    elif call.data == 'no': queue_out = 1
    elif user_data_balls and call.data == 'yes':
        queue_out = 4
    elif call.data == 'yes':
        queue_out = 3
        balls_input = True
    elif call.data == '55':
        user_data_balls = 55*3
        queue_out = 2
    elif call.data == '70':
        user_data_balls = 70*3
        queue_out = 2
    elif call.data == '85':
        user_data_balls = 85*3
        queue_out = 2
    elif call.data in ('yesV', 'noV'): queue_out = 4


    keyboard_math = types.InlineKeyboardMarkup()
    keyboard_other = types.InlineKeyboardMarkup()
    keyboard_answer = types.InlineKeyboardMarkup()
    keyboard_answerBalls = types.InlineKeyboardMarkup()
    keyboard_answerVUZ = types.InlineKeyboardMarkup()
    keyboard_answerVUZ.add(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='yesV'))
    keyboard_answerVUZ.add(types.InlineKeyboardButton(text='Пропустить', callback_data='noV'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='55+', callback_data='55'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='70+', callback_data='70'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='85+', callback_data='85'))
    keyboard_answer.add(types.InlineKeyboardButton(text='Да', callback_data='yes'))
    keyboard_answer.add(types.InlineKeyboardButton(text='Посмотрю еще предметы', callback_data='no'))
    for i in subjects_other:
        if i not in user_data:
            key = types.InlineKeyboardButton(text=subjects_other[i], callback_data=i)
            keyboard_other.add(key)
    for i in subjects_math:
        key = types.InlineKeyboardButton(text=subjects_math[i], callback_data=i)
        keyboard_math.add(key)

    count = 0
    for i in collages:
        if i.can_be(user_data.copy(), 310):
            count += 1

    count_with_balls = 310
    if user_data_balls:
        count_with_balls = 0
        for i in collages:
            if i.can_be(user_data.copy(), user_data_balls):
                count_with_balls += 1

    if count_with_balls < count and count_with_balls:
        text2 = f'С такими баллами выбор сужается до {count_with_balls} вузов'
    elif count_with_balls >= count:
        text2 = f'Это все? У нас тут {count} результатов. Взглянешь?'
    elif count_with_balls == 0 and count > 0:
        text2 = 'Для такого выбора с такими баллами ничгео не нашлось :('

    for i in collages:
        if i.can_be(user_data, user_data_balls):
            listV.append(i)

    if queue_out == 0: bot.send_message(id_user, text=f'user data: {user_data}',
                              reply_markup=keyboard_math)
    elif queue_out == 1: bot.send_message(id_user, text=f'user data: {user_data}',
                              reply_markup=keyboard_other)
    elif queue_out == 2: bot.send_message(id_user, text=text2,
                              reply_markup=keyboard_answer)
    elif queue_out == 3: bot.send_message(id_user, text='На сколько баллов метишь? Можешь написать сам:',
                         reply_markup=keyboard_answerBalls)
    elif queue_out == 4:
        bot.send_message(id_user, text=f'Name: {listV[0].name}'
                                       f'Subjects: {listV[0].subjects}'
                                       f'Balls_needed: {listV[0].balls}'
                                       f'Description: {listV[0].description}',
                         reply_markup=keyboard_answerVUZ)
        listV.pop(0)

bot.polling(none_stop=True, interval=0) # отработка декораторов