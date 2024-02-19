import telebot
from telebot import types

bot = telebot.TeleBot('7019813202:AAG-TNA5l12ZC-244jw223iqQ2jT05shJPI');
collages = {
    'first colllage': (['math_p', 'phis'], 55),
    'second collage': (['math_b', 'hist'], 55),
    'third collage': (['math_p', 'phis', 'inf'], 70)
}
names_subjects = {
    'math_p': ('математика профильная', 'математика профиль'),
    'math_b': ('математика базовая', 'математика база'),
    'phis': ('физика'),
    'inf': ('информатика'),
    'hist': ('история')

}
subjects = {
    'math_p': 'Математика профиль',
    'math_b': 'Математика база',
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


@bot.message_handler(content_types=['text'])
def f(message):
    global user_data
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');
    keyboard.add(key_yes);
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    if message.text:
        for i in names_subjects:
            if message.text in names_subjects[i]:
                if i not in user_data: user_data.append(i)
    # bot.send_message(message.from_user.id, text=f'ur id: {message.from_user.id}\nuser data: {user_data}')
    # bot.send_message(message.from_user.id, text=f'Для этого спсиска найдено {count} вариантов. Посмотреть?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        pass
    elif call.data == "no":
        pass

bot.polling(none_stop=True, interval=0) # отработка декораторов