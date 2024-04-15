import telebot
from telebot import types
from itertools import *
import databaseConnect
import random


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
                collage('РТУ МИРЭА', 100, ('math_p', 'phis'), 'norm VUZ2'),
            collage('Ювилирный', 100, ('math_p', 'hist'), 'norm VUZ3'),
            collage('МГУ', 100, ('math_p', 'phis', 'inf', 'bio'), 'norm МГУ'),
            collage('МГТУ им.Баумана', 100, ('math_p', 'phis', 'bio'), 'norm 1111')]

bot = telebot.TeleBot('7019813202:AAG-TNA5l12ZC-244jw223iqQ2jT05shJPI');

names_subjects = {
    'math_p': ('математика профильная', 'математика профиль'),
    'math_b': ('математика базовая', 'математика база'),
    'phis': ('физика'),
    'inf': ('информатика'),
    'hist': ('история')
}
subjects_math = {
    'math_p':'📈Математика профиль',
    'math_b':'📉Математика база'
}
subjects_other = {
    'phis': '💀Физика',
    'inf': '🌐Информатика',
    'hist': '🏰История',
    'soc': '👤Общество',
    'bio': '🧬Биология',
    'chem': '🧪Химия',
    'geo': '🗺️География️',
    'eng': '🇬🇧Английский🇬🇧',
    'liter': '📚Литература'
}

user_data = []
user_data_balls = 0
count = 0
count_with_balls = 0
queue_out = -1
id_user = ''
listV = []
flagColl = False
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
    elif queue_out == 2:
        bot.send_message(id_user, text=f'Это все? У нас тут {count} результатов. Взглянешь?',
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
    universalButton3 = types.InlineKeyboardButton(text='ИНФО', callback_data='info')
    keyboard_math = types.InlineKeyboardMarkup()
    keyboard_other = types.InlineKeyboardMarkup()
    keyboard_answer = types.InlineKeyboardMarkup()
    keyboard_answerBalls = types.InlineKeyboardMarkup()
    keyboard_mainMenu = types.InlineKeyboardMarkup()
    keyboard_mainMenu.add(types.InlineKeyboardButton(text='Начать', callback_data='starting'))
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
    if queue_out == -1: bot.send_photo(id_user, caption='Привет, это бот "After ЕГЭ" и он поможет тебе определиться с выбором вуза!', photo='https://i.imgur.com/k9NwTr7.png',
                                       reply_markup=keyboard_mainMenu)
    elif queue_out == 0: bot.send_photo(id_user, photo='https://i.imgur.com/9TQFoHQ.png', reply_markup=keyboard_math)
    elif queue_out == 1: bot.send_photo(id_user, photo='https://i.imgur.com/7VoNa5R.png', reply_markup=keyboard_other)
    elif queue_out == 2:
        count += random.randint(10, 20)
        bot.send_message(id_user, text=f'Это все? У нас тут {count} результатов. Взглянешь?',
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
    global flagColl
    universalButton1 = types.InlineKeyboardButton(text='ГЛАВНОЕ МЕНЮ', callback_data='mainMenu')
    universalButton2 = types.InlineKeyboardButton(text='ИЗБРАННОЕ', callback_data='izbrannoe')
    universalButton3 = types.InlineKeyboardButton(text='ИНФО', callback_data='info')
    if call.data in subjects_math:
        queue_out = 1
        user_data.append(call.data)
    elif call.data == 'izbrannoe':
        queue_out = -2
    elif call.data == 'info':
        queue_out = -3
    elif call.data == 'starting':
        queue_out = 0
    elif call.data == 'mainMenu':
        queue_out = -1
        user_data = []
        listV = []
        user_data_balls = 0
        balls_input = False
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
                                platno, cost, otsrochka, balls_user, subjects, speciality)
                                VALUES({id_user}, '{listV[0].name}', '{listV[0].description}', 
                                '{listV[0].link}', {listV[0].besplatno}, {listV[0].platno}, {listV[0].cost}, 
                                {listV[0].otsrochka}, {listV[0].balls}, '{listV[0].subjects[0]}', 'asd')""")
        listV.pop(0)
    if call.data == 'noV':
        listV.pop(0)

    keyboard_math = types.InlineKeyboardMarkup()
    keyboard_other = types.InlineKeyboardMarkup()
    keyboard_answer = types.InlineKeyboardMarkup()
    keyboard_answerBalls = types.InlineKeyboardMarkup()
    keyboard_answerVUZ = types.InlineKeyboardMarkup()
    keyboard_mainMenu = types.InlineKeyboardMarkup()
    keyboard_mainMenu.add(types.InlineKeyboardButton(text='Начать', callback_data='starting'))
    keyboard_mainMenu.add(universalButton2)
    keyboard_mainMenu.add(universalButton3)
    keyboard_answerVUZ.add(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='yesV'),
                           types.InlineKeyboardButton(text='Пропустить', callback_data='noV'))
    keyboard_answerVUZ.add(universalButton1)
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='55+', callback_data='55'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='70+', callback_data='70'))
    keyboard_answerBalls.add(types.InlineKeyboardButton(text='85+', callback_data='85'))
    keyboard_answer.add(types.InlineKeyboardButton(text='Да', callback_data='yes'))
    keyboard_answer.add(types.InlineKeyboardButton(text='Посмотрю еще предметы', callback_data='no'))
    keyboard_answer.add(universalButton1)

    flag = True
    row = []
    c = 0
    for index, i in enumerate(subjects_other):
        if len(row) == 2:
            keyboard_other.add(row[0], row[1])
            row = []
        elif len(row) == 1 and index+1 == len(subjects_other):
            keyboard_other.add(row[0])
        if i not in user_data:
            row.append(types.InlineKeyboardButton(text=subjects_other[i], callback_data=i))
    keyboard_other.add(universalButton1)

    for i in subjects_math:
        key = types.InlineKeyboardButton(text=subjects_math[i], callback_data=i)
        keyboard_math.add(key)
    keyboard_math.add(universalButton1)

    count = 0
    for i in collages:
        if i.can_be(user_data.copy(), 310):
            count += 1
    if flagColl and queue_out == 2:
        for i in collages:
            if i.can_be(user_data, user_data_balls):
                listV.append(i)
        flagColl = False

    count_with_balls = 310
    if user_data_balls:
        count_with_balls = 0
        for i in collages:
            if i.can_be(user_data.copy(), user_data_balls):
                count_with_balls += 1

    if count_with_balls < count and count_with_balls:
        text2 = f'С такими баллами выбор сужается до {count_with_balls} вузов'
    elif count_with_balls >= count:
        count += random.randint(10, 20)
        text2 = f'Это все? У нас тут {count} результатов. Взглянешь?'
    elif count_with_balls == 0 and count > 0:
        text2 = 'Для такого выбора с такими баллами ничгео не нашлось :('

    if queue_out == -1: bot.send_photo(id_user, caption='',
                                       photo='https://i.imgur.com/k9NwTr7.png',
                                       reply_markup=keyboard_mainMenu)
    elif queue_out == -2:
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton(text='Информация о вузе', url='https://vuzopedia.ru/vuz/405'))
        m.add(types.InlineKeyboardButton(text='Далее', callback_data=666))
        m.add(universalButton1)
        text1 = 'Национальный исследовательский технологический университет МИСИС'
        text2 = ('Университет МИСИС — ведущий вуз страны в области создания, '
                 'внедрения и применения новых технологий и материалов. В 2023 году НИТУ МИСИС занял 264-е место в мировом рейтинге университетов RUR, '
                 'войдя в ТОП-5 лучших вузов страны. Университет продемонстрировал наибольший рост по показателям «Преподавание» и «Исследования».')
        bot.send_message(id_user, text=text1)
        bot.send_message(id_user, text=text2, reply_markup=m)
    elif queue_out == -3:
        m1 = types.InlineKeyboardMarkup()
        m1.add(types.InlineKeyboardButton(text='ГЛАВНОЕ МЕНЮ', callback_data='mainMenu'))
        bot.send_photo(id_user, photo= 'https://i.imgur.com/65ipGkK.png',
                       caption='Бот супер классный, помогает с выбором вуза школьникам 10 и 11 классов) ', reply_markup=m1)
    elif queue_out == 0: bot.send_photo(id_user, photo='https://i.imgur.com/9TQFoHQ.png', reply_markup=keyboard_math)
    elif queue_out == 1: bot.send_photo(id_user, photo='https://i.imgur.com/7VoNa5R.png', reply_markup=keyboard_other)
    elif queue_out == 2: bot.send_message(id_user, text=text2, reply_markup=keyboard_answer)
    elif queue_out == 3:
        flagColl = True
        bot.send_photo(id_user, photo='https://i.imgur.com/kkyh2Zi.png',
                         reply_markup=keyboard_answerBalls)
    elif queue_out == 4:
        keyboard_end = types.InlineKeyboardMarkup()
        keyboard_end.add(universalButton1)
        if listV:
            bot.send_message(id_user, text=f'Name: {listV[0].name}'
                                           f'Subjects: {listV[0].subjects}'
                                           f'Balls_needed: {listV[0].balls}'
                                           f'Description: {listV[0].description}',
                             reply_markup=keyboard_answerVUZ)
        else:
            bot.send_message(id_user, text='Вузы кончились, можешь зайти во вкладку избранного и присмотреться '
                                             'к каждому вузу подробнее или добавить еще :)', reply_markup=keyboard_end)

bot.polling(none_stop=True, interval=0) # отработка декораторов