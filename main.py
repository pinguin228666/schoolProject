import telebot
from telebot import types
from itertools import *
import databaseConnect


class collage(object):
    def __init__(self, name='0', balls=0, subjects='0', description='0',
                 link='0', besplatno=0, platno=0, cost=0, otsrochka=0):
        self.name = name
        self.balls = balls
        self.subjects = subjects
        self.description = description
        self.link = link
        self.besplatno = besplatno
        self.platno = platno
        self.cost = cost
        self.otsrochka = otsrochka

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
    'math_p':'❤Математика профиль❤',
    'math_b':'♿Математика база♿'
}
subjects_other = {
    'phis': '💀Физика💀',
    'inf': '🌐Информатика🌐',
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


@bot.message_handler(commands=['reset'])
def f2(message):
    global user_data
    global queue_out
    global id_user
    global balls_input
    id_user = message.from_user.id

    user_data = []
    queue_out = 0
    balls_input = []

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

    flag = True
    row = []
    for i in subjects_other:
        if len(row) == 2: flag = False
        if i not in user_data and flag:
            key = types.InlineKeyboardButton(text=subjects_other[i], callback_data=i)
            row.append(key)
        if flag == False:
            keyboard_other.add(row[0], row[1])
            row = []
            flag = True

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

@bot.message_handler(commands=['start'])
def f1(message):
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

    flag = True
    row = []
    for i in subjects_other:
        if len(row) == 2: flag = False
        if i not in user_data and flag:
            key = types.InlineKeyboardButton(text=subjects_other[i], callback_data=i)
            row.append(key)
        if flag == False:
            keyboard_other.add(row[0], row[1])
            row = []
            flag = True

    for i in subjects_math:
        key = types.InlineKeyboardButton(text=subjects_math[i], callback_data=i)
        keyboard_math.add(key)

    if queue_out == 0: bot.send_photo(id_user, photo='https://i.imgur.com/9TQFoHQ.png', reply_markup=keyboard_math)
    #https://i.imgur.com/7VoNa5R.png
    elif queue_out == 1: bot.send_photo(id_user, photo='https://i.imgur.com/7VoNa5R.png', reply_markup=keyboard_other)
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
    elif call.data in ('yesV', 'noV') and listV:
        queue_out = 4
    if call.data == 'yesV':
        databaseConnect.writeDB(f"""INSERT INTO users (user_id, nameV, discriptionV, linkV, besplatno,
                                platno, cost, otsrochka, balls_user, subjects)
                                VALUES({id_user}, '{listV[0].name}', '{listV[0].description}', 
                                '{listV[0].link}', {listV[0].besplatno}, {listV[0].platno}, {listV[0].cost}, 
                                {listV[0].otsrochka}, {listV[0].balls}, '{listV[0].subjects[0]}')""")
        listV.pop(0)
    if call.data == 'noV':
        listV.pop(0)

    keyboard_math = types.InlineKeyboardMarkup()
    keyboard_other = types.InlineKeyboardMarkup()
    keyboard_answer = types.InlineKeyboardMarkup()
    keyboard_answerBalls = types.InlineKeyboardMarkup()
    keyboard_answerVUZ = types.InlineKeyboardMarkup()
    keyboard_answerVUZ.add(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='yesV'),
                           types.InlineKeyboardButton(text='Пропустить', callback_data='noV'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='55+', callback_data='55'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='70+', callback_data='70'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='85+', callback_data='85'))
    keyboard_answer.add(types.InlineKeyboardButton(text='Да', callback_data='yes'))
    keyboard_answer.add(types.InlineKeyboardButton(text='Посмотрю еще предметы', callback_data='no'))

    flag = True
    row = []
    c = 0
    for i in subjects_other:
        c+=1
        if len(row) == 2: flag = False
        if i not in user_data and flag:
            row.append(types.InlineKeyboardButton(text=subjects_other[i], callback_data=i))
        if flag == False:
            keyboard_other.add(row[0], row[1])
            row = [types.InlineKeyboardButton(text=subjects_other[i], callback_data=i)]
            flag = True
        if (len(subjects_other) - len(user_data))%2==0 and c==len(subjects_other) and len(row)==1:
            keyboard_other.add(row[0])

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
    elif queue_out == 1: bot.send_photo(id_user, photo='https://i.imgur.com/7VoNa5R.png', reply_markup=keyboard_other)

    elif queue_out == 2: bot.send_message(id_user, text=text2, reply_markup=keyboard_answer)
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