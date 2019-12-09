#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import bs4
import parser
import markups as m
import sys
import subprocess
import json
import functions
reload(sys)
sys.setdefaultencoding('utf-8')
#main variables
TOKEN = "870626699:AAFdb_Ai72b_9FtrWJMSrZlU4dLIWYV63Ek"
bot = telebot.TeleBot(TOKEN)
account = {'name':'','surname':'','phone':'','id':''}
global ref_par
ref_par = "nothing"
#
@bot.message_handler(commands=['start', 'go'])
#Нажатие кнопки /start запускает бота
def start_handler(message):
    global isRunning
    isRunning = False
    if not isRunning:
        chat_id = message.chat.id
        text = message.text
        def refParTrue(val):
            try:
                int(output['data']['list'][0]['id'])
            except:
                msg = bot.send_message(chat_id, "Пользователь не найден. Добавить вас в реферальную систему? "+str(val), reply_markup=m.start_markup)
                bot.register_next_step_handler(msg, askRegister)
            else:
                account['name'] = output['data']['list'][0]['name']
                msg = bot.send_message(chat_id, "Здравствуйте, "+output['data']['list'][0]['name'])
        try:
            ref_par = text.split(' ')[1]
        except:  
            refParTrue("0")
        else:
            refParTrue(text.split(' ')[1])
        user_id = message.from_user.id
        output = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getAll.php', str(user_id)]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
        
    isRunning = True
#Нажатие кнопки ДА запускает создание нового пользователя (registerName), нажатие кнопки Узнать о программе выводит инофрмационное сообщение (showInfo)
def askRegister(message):
    chat_id = message.chat.id
    text = message.text
    print " "
    print message
    print " "
    try:
        text.split(" ")[1]
    except:
        start_ref = text
    else:
        start_ref= text.split(" ")[0]
        output_ref_par = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getRefParent.php', str(text.split(" ")[1])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
    user_id = message.from_user.id
    if text == "Да":
        msg = bot.send_message(chat_id, "Введите ваш номер телефона в формате 7**********", reply_markup=m.zero_markup)
        bot.register_next_step_handler(msg, registerPhone)
    elif text == "Узнать больше":
        msg = bot.send_message(chat_id, "Реферальная программа это бла бла бла, где выполучаете бла бла бла",reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askRegister)
    elif start_ref == "/start" :
        try:
            int(output_ref_par['data']['list'][0]['id'])
        except:
             msg = bot.send_message(chat_id, "Реферальная ссылка не действительна")
             isRunning = False
             ref_par = "0"
        else:
            ref_par = ext.split(" ")[1]
            msg = bot.send_message(chat_id, "Вы перешли по реферальной ссылке: https://t.me/AMLSrefbot?start="+text.split(" ")[1]+"\nПользователь не найден. Добавить вас в реферальную систему? Вы перешли по реферальной ссылке "+text.split(" ")[1], reply_markup=m.start_markup)
            bot.register_next_step_handler(msg, start_handler)
    else:
        msg = bot.send_message(chat_id, "Вы ввели неверную команду", reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askRegister)
def registerPhone(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id   
    account['phone'] = text #записали в переменную имя
    try:
            account['phone']
    except:
        print "registerName excepted : С Телефоном что-то не так"
        bot.register_next_step_handler(msg, registerName)
    else:
        msg = bot.send_message(chat_id, "Введите ваше имя", reply_markup=m.zero_markup)
        bot.register_next_step_handler(msg, registerName)
def registerName(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id   
    account['name'] = text #записали в переменную имя
    try:
            account['name']
    except:
        print "registerName excepted : С Именем что-то не так"
        bot.register_next_step_handler(msg, registerName)
    else:
        msg = bot.send_message(chat_id, "Введите вашу фамилию", reply_markup=m.zero_markup)
        bot.register_next_step_handler(msg, registerSName)
def registerSName(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id   
    account['surname'] = text #записали в переменную имя
    try:
            account['surname']
    except:
        print "registerSName excepted : С Фамилией что-то не так"
        bot.register_next_step_handler(msg, registerSName)
    else:
        msg = bot.send_message(chat_id, "Проверьте информацию! Фамилия: "+account['surname']+" Имя: "+account['name']+" Номер телефона: "+account['phone'], reply_markup=m.yesNo_markup)
        bot.register_next_step_handler(msg, checkRegInfo)
def checkRegInfo(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id
    user_id_hash = str(user_id)
    print "--------"
    print ref_par
    print "--------"
    if text == "Да":
        output_addCustomer = subprocess.Popen(['php', 'CRM_API/example/customer/add.php', str(account['name']),str(account['surname']),str(account['phone']),str(user_id_hash),str(ref_par)]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0]
        #output = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getAll.php', str(user_id)]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
        msg = bot.send_message(chat_id, "Здравствуйте, "+account['name'])
        bot.register_next_step_handler(msg,start_handler)
    elif text == "Нет":
        msg = bot.send_message(chat_id, "Введите ваш номер телефона в формате 7**********", reply_markup=m.zero_markup)
        bot.register_next_step_handler(msg, registerPhone)
    else:
        msg = bot.send_message(chat_id, "Вы ввели неверную команду", reply_markup=m.yesNo_markup)
        bot.register_next_step_handler(msg, checkRegInfo)
bot.polling()

