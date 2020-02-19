import telebot
import requests, random, datetime, sys, time, argparse, os
import time
import bot_db
import datetime
import spammer_serv
import number_spam_db

from datetime import timedelta

from telebot import types

TOKEN = '918851085:AAFhLBqJvMmmJWslrNAPpDMdr8Sxz_OO8SI'
bot = telebot.TeleBot(TOKEN)
user_pass = 'user117'
num_spam = '0'
num_spam_trial = '0'
id_trial = 0


@bot.message_handler(commands=['start'])
def welcome(message):
    global id_trial
    full_name = '{} - {}'.format(message.from_user.first_name, message.from_user.last_name)
    bot_db.reg(message.from_user.id, message.from_user.username, full_name)
    bot_db.date_sms_spam(message.from_user.id)
    id_trial = message.from_user.id
    item1 = types.KeyboardButton("Начать спам ✉")
    item2 = types.KeyboardButton("Инфо 📜")
    item3 = types.KeyboardButton("Обновить ⚙")
    item4 = types.KeyboardButton("Статус 🎩")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1, item2, item3, item4)
    if bot_db.ver != 3:
        item5 = types.KeyboardButton("Professional version 🛡")
        markup.add(item5)
    print(bot_db.ver)
    if bot_db.ver == 3:
        item8 = types.KeyboardButton("База даных 📚")
        markup.add(item8)

    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                    "Приветствую, {0.first_name}! 😉\nЯ - <b>{1.first_name}</b>, помогу тебе завалить телефон твоего дружка!\n"
                    .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def sms(message):
    global num_spam, num_spam_trial
    if message.chat.type == 'private':
        bot_db.date_sms_spam(message.from_user.id)
        if message.text == 'Начать спам ✉':
            if bot_db.time_sms != 0:
                bot_db.time_sms = datetime.datetime.strptime(bot_db.time_sms, '%Y-%m-%d %H:%M:%S.%f')
                date_time_spam = datetime.datetime.now() - timedelta(days=0.5)
            if bot_db.ver != 0 or bot_db.time_sms == 0 or bot_db.time_sms < date_time_spam:
                bot.send_message(message.chat.id,
                                 "Введите номер телефона в формате:\n+380XXXXXXXXX UA 🇺🇦\n+7XXXXXXXXXX RU 🇷🇺")
            else:
                bot.send_message(message.chat.id, 'У вас закончились попытки спама на сегодня, приобретите нашу '
                                                  'про версию, или попробуйте позже')
                exit(0)
        _phone = message.text
        s = _phone
        #     print(_phone)
        s = s[:0] + s[0 + 1:]
        if s.isdigit():
            if bot_db.ver == 2 or bot_db.ver == 3:
                num_spam = _phone
            elif bot_db.ver == 0:
                num_spam_trial = _phone

            bot.send_message(message.chat.id, "Вы ввели: " + _phone)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Начать", callback_data='good')
            item2 = types.InlineKeyboardButton("Отмена", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "к спаму готов!", reply_markup=markup)

        elif message.text == 'Инфо 📜':
            bot.send_message(message.chat.id,
                             "Дружочек <b>{0.first_name}</b>, Я бот и предназначен для флуда мобильных"
                             " телефонов средством массовых 📩 сообщений и 📞 Работаю с многими странами СНГ."
                             .format(message.from_user), parse_mode='html')
        elif message.text == 'Обновить ⚙':
            bot.message_handler(commands=['start'])
            # welcome('start')
            bot.send_message(message.chat.id, "Бот обновлен 💚")
            welcome(message)
        elif message.text == 'База даных 📚':
            if bot_db.ver == 3:
                bot.send_message(message.chat.id, "Вывожу базу даных 💎")
                bot_db.db_info_adm()
                print(bot_db.baza_viv)
        elif message.text == 'Статус 🎩':
            bot_db.date_sms_spam(message.from_user.id)
            status = ''
            if bot_db.ver == 0:
                status = 'trial version'
            elif bot_db.ver == 2:
                status = 'professional version'
            elif bot_db.ver == 3:
                status = 'Administrator'
            else:
                status = 'Error'
            t_ime = bot_db.time_sms
            if bot_db.time_sms == 0:
                t_ime = '--'
            bot.send_message(message.chat.id, "<b>{}</b>\nСтатус : <b>{}</b> \nПоследнее время спама: <b>{}</b>"
                                              "\nСейчас: <b>{}</b>"
                             .format(message.from_user.first_name, status, t_ime, datetime.datetime.now()),
                             parse_mode='html')
        elif message.text == 'Professional version 🛡':
            bot_db.date_sms_spam(message.from_user.id)
            if bot_db.ver == 0:
                bot.send_message(message.chat.id, "Купи приватку, и получи следующие плюшки:\n• Спам без границ\n "
                                                  "Анти спам\n Спам без очереди\n Больше 📩 сообщений и 📞\n Чтобы "
                                                  "приобрести промо версию, напишите администратору <b>@Xande_er</b>"
                                 ,parse_mode='html')
            else:
                bot.send_message(message.chat.id, "У вас куплена Professional version, спассибо что вы с нами)")
        elif message.text == '':
            if spammer_serv._phone == '':
                number_spam_db.number_spam_proces()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global num_spam, num_spam_trial, id_trial
    try:
        if call.message:
            if call.data == 'good':
                bot_db.date_sms_spam(call.message.chat.id)
                if bot_db.ver == 2 or bot_db.ver == 3:
                    bot.send_message(call.message.chat.id, "Спам запущен на 15 мин. 😃 😃")
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text="щасливого дня 😎")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="щасливого дня 😎", reply_markup=None)
                    bot_db.spam_date(call.message.chat.id)
                    spammer_serv.Main_1(num_spam)
                elif bot_db.ver == 0:
                    number_spam_db.bd_numbers(num_spam_trial, call.message.chat.id)
                    bot.send_message(call.message.chat.id, "Ваш номер добавлен в очередь, ожидайте спама 😃 😃\n"
                                                           "Не хотите ждать?? Приобретите professional version")
                    bot_db.spam_date(call.message.chat.id)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="щасливого дня 😎", reply_markup=None)
                    num_spam_trial = ''
                if num_spam_trial == '':
                    number_spam_db.number_spam_proces()
                    num_spam_trial = str(number_spam_db.number_spam_go)
                    num_spam_trial = '+{}'.format(num_spam_trial)
                    if num_spam_trial != 0 and num_spam_trial != '':
                        bot.send_message(number_spam_db.id_spam_go, "Прийшла ваша очередь\nСпам запущен на 15 мин. "
                                                                    "😃 😃")
                        spammer_serv.Main_1(num_spam_trial)
                        number_spam_db.id_spam_go = 0
                        num_spam_trial = ''
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, "Спам закончен 😃 😃")
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="щасливого дня 😎")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
                exit(0)

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)