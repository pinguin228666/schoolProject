import telebot

bot = telebot.TeleBot('7019813202:AAG-TNA5l12ZC-244jw223iqQ2jT05shJPI');

@bot.message_handler(content_types=['text'])
def f(message):
    if message.text:
        bot.send_message(message.from_user.id, f'ur id: {message.from_user.id}')


bot.polling(none_stop=True, interval=0)