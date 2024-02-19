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
            if sorted(self.subjects) == sorted(i):
                print(self.subjects)
                return True
            else: return False


collages = []
collages.append(collage('МИСИС', 270, ('math_p', 'inf'), 'norm VUZ'))

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
count = 0
queue_out = 0
id_user = ''
@bot.message_handler(content_types=['text'])
def f(message):
    global user_data
    global queue_out
    global id_user
    id_user = message.from_user.id

    keyboard_math = types.InlineKeyboardMarkup()
    keyboard_other = types.InlineKeyboardMarkup()
    keyboard_answer = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard_answer.add(key)
    key = types.InlineKeyboardButton(text='Посмотрю еще предметы', callback_data='no')
    keyboard_answer.add(key)
    for i in subjects_other:
        key = types.InlineKeyboardButton(text=subjects_other[i], callback_data=i)
        keyboard_other.add(key)
    for i in subjects_math:
        key = types.InlineKeyboardButton(text=subjects_math[i], callback_data=i)
        keyboard_math.add(key)

    print(collages[0].can_be(user_data, 0))

    if queue_out == 0: bot.send_message(id_user, text=f'ur id: {message.from_user.id}\nuser data: {user_data}',
                              reply_markup=keyboard_math)
    elif queue_out == 1: bot.send_message(id_user, text=f'ur id: {message.from_user.id}\nuser data: {user_data}',
                              reply_markup=keyboard_other)
    elif queue_out == 2: bot.send_message(id_user, text=f'Это все? У нас тут {count} результатов. Взглянешь?',
                              reply_markup=keyboard_answer)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global queue_out
    global user_data
    global id_user
    if call.data in subjects_math:
        queue_out = 1
        user_data.append(call.data)
    elif call.data in subjects_other:
        queue_out = 2
        user_data.append(call.data)
    elif call.data == 'no': queue_out = 1

    keyboard_math = types.InlineKeyboardMarkup()
    keyboard_other = types.InlineKeyboardMarkup()
    keyboard_answer = types.InlineKeyboardMarkup()
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
    if queue_out == 0: bot.send_message(id_user, text=f'user data: {user_data}',
                              reply_markup=keyboard_math)
    elif queue_out == 1: bot.send_message(id_user, text=f'user data: {user_data}',
                              reply_markup=keyboard_other)
    elif queue_out == 2: bot.send_message(id_user, text=f'Это все? У нас тут {count} результатов. Взглянешь?',
                              reply_markup=keyboard_answer)

bot.polling(none_stop=True, interval=0) # отработка декораторов