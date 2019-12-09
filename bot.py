#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import bs4
import parser
import markups as m
import sys
import subprocess
import json
import authMod
import get_api
reload(sys)
sys.setdefaultencoding('utf-8')
#main variables
TOKEN = "870626699:AAFdb_Ai72b_9FtrWJMSrZlU4dLIWYV63Ek"
bot = telebot.TeleBot(TOKEN)
account = {'name':'','phone':'', 'city':'','id':'','telegram_id':'', 'registered':'', 'parentRef':'','ref':'', 'wallet_id':'', 'wallet_amount': ''}
fromCrmId = {}
#

def checkWallet():
    fromCrmId = get_api.get_user_by_telegram_id(str(account['telegram_id']))
    #fromCrmId = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getAll.php', str(account['telegram_id'])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
    for value in fromCrmId['data']['list'][0]['fields']:
        if value['id']=='1564':
            account['wallet_id'] = value['value']
        if value['id']=='1566':
            account['wallet_amount'] = value['value']

@bot.message_handler(commands=['start'])
#Нажатие кнопки /start запускает бота
def start_handler(message):
    global isRunning
    global account
    account = {'name':'','phone':'', 'city':'','id':'','telegram_id':'', 'registered':'', 'parentRef':'','ref':'', 'wallet_id':'', 'wallet_amount': ''}
    isRunning = False
    text = message.text
    user_id = message.from_user.id
    account['telegram_id'] = user_id
    fromCrmId = get_api.get_user_by_telegram_id(str(account['telegram_id']))
    #fromCrmId = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getAll.php', str(account['telegram_id'])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
    print "--------------------------------------"
    print "Произошла авторизация пользователя с TelegramId: "+str(message.from_user.id)
    #Проверка наличия реферальной ссылки
    try:
        text.split(" ")[1]
    #Переход БЕЗ реферальной ссылки
    except:
        print 'Ошибка при вызове функции start_handler, при выполнении операции text.split(" ")[1] - реферальная ссылка не найдена (вход без ссылки)'
        referalLink = "0"
        msg = bot.send_message(message.chat.id, 'Добрый день! Вы попали в чат-бот реферальной программы *AMLS Недвижимости*.\nУказанная вами реферальная ссылка не действительна.\nЧтобы продолжить, необходимо зарегистрироваться.\nХотите продолжить?',reply_markup=m.start_markup, parse_mode="Markdown")  
        account['parentRef'] = '0'
        bot.register_next_step_handler(msg, register) 
    #Переход ПО реферальной ссылке
    else:
        referalLink = text.split(" ")[1]
    #Поиск реферальной ссылки в CRM
        fromCrmParent = get_api.get_ref_parent(str(referalLink))
        #fromCrmParent = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getRefParent.php', str(referalLink)]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
        try:
            fromCrmParent['data']['list'][0]['fields']
    #Реферальная ссылка не действительна (Вообще нет похожей)
        except:
            print "Ошибка при вызове функции start_handler, при выполнении операции fromCrmParent['data']['list'][0]['fields'] реферальная ссылка не найдена (введена какая-то дичь)"
            msg = bot.send_message(message.chat.id, 'Добрый день! Вы попали в чат-бот реферальной программы *AMLS Недвижимости*. \nУказанная вами реферальная ссылка не действительна.\nЧтобы продолжить, необходимо зарегистрироваться.\nХотите продолжить?',reply_markup=m.start_markup, parse_mode="Html") 
            account['parentRef'] = '0'
            bot.register_next_step_handler(msg, register) 
        else:
            referalParentFields = fromCrmParent['data']['list'][0]['fields']
            for field in referalParentFields:
                if field['telegram_id'] == str(1563):
                    crmParentValue  = str(field['value'])
    #Реферальная ссылка ДЕЙСТВИТЕЛЬНА
                    if crmParentValue == referalLink:
                        msg = bot.send_message(message.chat.id, 'Добрый день! Вы перешли по реферальной ссылке: \n<a href="https://t.me/AMLSrefbot?start='+referalLink+'">https://t.me/AMLSrefbot?start='+referalLink+'</a>.\nЧтобы продолжить, необходимо зарегистрироваться.\nХотите продолжить?',reply_markup=m.start_markup, parse_mode="Html")   
                        account['parentRef'] = referalLink
                        bot.register_next_step_handler(msg, register) 
    #Реферальная ссылка не действительна (Есть похожая, но не та)
                    else:
                        msg = bot.send_message(message.chat.id, 'Добрый день! Вы попали в чат-бот реферальной программы *AMLS Недвижимости*. \nУказанная вами реферальная ссылка не действительна.\nЧтобы продолжить, необходимо зарегистрироваться.\nХотите продолжить?',reply_markup=m.start_markup, parse_mode="Html")  
                        account['parentRef'] = '0'
                        bot.register_next_step_handler(msg, register) 
        #bot.send_message(message.chat.id, 'Привет, ты написал мне '+str(referalParentField))  
    print "Реферальная ссылка: "+str(referalLink)

    #bot.send_message(message.chat.id, 'Привет, ты написал мне '+str(message))      
    isRunning = True
def register(message):
    if message.text == "Нет":
        msg = bot.send_message(message.chat.id, 'Вы еще не зарегистрированы.\nДля продолжения работы с чат-ботом необходимо пройти небольшую регистрацию. \nПосле чего вы получите доступ к функционалу бота и собственную реферальную ссылку. \nКак мы можем к вам обращаться? (Укажите имя)', parse_mode="Html")
        bot.register_next_step_handler(msg, registerPhone)
    else:
        user_id = message.from_user.id
        fromCrmId = get_api.get_user_by_telegram_id(str(account['telegram_id']))
        #fromCrmId = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getAll.php', str(account['telegram_id'])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
        account['telegramid'] = user_id
        try:
            fromCrmId['data']['list'][0]['id']
        except:
            print "Ошибка при вызове функции register, при выполнении операции fromCrmId['data']['list'][0]['id']"
            msg = bot.send_message(message.chat.id, 'Вы еще не зарегистрированы.\nДля продолжения работы с чат-ботом необходимо пройти небольшую регистрацию. \nПосле чего вы получите доступ к функционалу бота и собственную реферальную ссылку. \nКак мы можем к вам обращаться? (Укажите имя)', parse_mode="Html")
            bot.register_next_step_handler(msg, registerPhone)
        else:
            account['name'] = fromCrmId['data']['list'][0]['name']
            account['id'] = fromCrmId['data']['list'][0]['id']
            msg = bot.send_message(message.chat.id, "Здравствуйте, "+account['name'], reply_markup=m.menu_markup) 
            bot.register_next_step_handler(msg, menuWelcome)   
def registerPhone(message):  
    text = message.text 
    account['name'] = text
    msg = bot.send_message(message.chat.id, 'Укажите ваш номер телефона в формате 7**********', parse_mode="Html")
    bot.register_next_step_handler(msg, registerCity)
def registerCity(message):
    global checkPhoneDuplicate
    text = message.text
    if authMod.checkPhone(text):
        account['phone'] = text
        checkPhoneDuplicate = get_api.get_phone_duplicate(str(account['phone']))
        #checkPhoneDuplicate = json.loads(subprocess.Popen(['php', 'CRM_API/example/customer/getPhoneDuplicate.php', str(account['phone'])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
        global isDuplicate
        try:    
            if checkPhoneDuplicate['data']['list'][0]['phone'][0]['phone'] == account['phone']:
                isDuplicate = True
                account['name'] = checkPhoneDuplicate['data']['list'][0]['name']
                try:
                    account['city'] = checkPhoneDuplicate['data']['list'][0]['city']
                    msg = bot.send_message(message.chat.id, 'К данному номеру уже привязан аккаунт в CRM с именем: '+account['name']+' Продолжить?',reply_markup=m.yn_markup, parse_mode="Html") 
                    bot.register_next_step_handler(msg, register)
                except:
                    print "Ошибка при вызове функции registerCity, при выполнении операции checkPhoneDuplicate['data']['list'][0]['city'] - не указан город"
                    msg = bot.send_message(message.chat.id, 'К данному номеру уже привязан аккаунт в CRM с именем: '+account['name']+ ', но не указан город. Укажите ваш город', parse_mode="Html")
                    bot.register_next_step_handler(msg, registerFinal)
            else:
                isDuplicate = False
                msg = bot.send_message(message.chat.id, 'Укажите ваш город', parse_mode="Html")
                bot.register_next_step_handler(msg, registerFinal)
        except:
            print "Ошибка при вызове функции registerCity, при проверке checkPhoneDuplicate['data']['list'][0]['phone'][0]['phone'] == account['phone'] - нет дупликатов"
            isDuplicate = False
            msg = bot.send_message(message.chat.id, 'Укажите ваш город', parse_mode="Html")
            bot.register_next_step_handler(msg, registerFinal)
    else:
        msg = bot.send_message(message.chat.id, 'Укажите ваш номер телефона в формате 7**********', parse_mode="Html")
        bot.register_next_step_handler(msg, registerCity)
def registerFinal(message):
    global checkPhoneDuplicate
    text = message.text
    account['city'] = text
    account['ref'] = str( ((int(account['telegram_id']) + int(account['parentRef'])) / 2))
    print "Родительская реферальная ссылка: "+account['parentRef']
    if isDuplicate:
        account['id'] = str(json.loads(checkPhoneDuplicate['data']['list'][0]['id']))
        checkPhoneDuplicate = get_api.update_contact_duplicate(str(account['id']),str(account['telegram_id']),str(account['parentRef']),str(account['ref']))
        #output_addCustomer = subprocess.Popen(['php', 'CRM_API/example/customer/update_contact_duplicate.php', str(account['id']),str(account['telegram_id']),str(account['parentRef']),str(account['ref'])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0]
        msg = bot.send_message(message.chat.id, 'Информация обновлена. Ваша реферальная ссылка: \n<a href="https://t.me/AMLSrefbot?start='+account['ref']+'">https://t.me/AMLSrefbot?start='+account['ref']+'</a>.\nПриступить к работе в боте?',reply_markup=m.start_markup, parse_mode="Html")
        bot.register_next_step_handler(msg, start_handler)
    else:
        output_addCustomer = get_api.add(str(account['name']),str(account['phone']),str(account['telegram_id']))
        #output_addCustomer = subprocess.Popen(['php', 'CRM_API/example/customer/add.php', str(account['name']),str(account['phone']),str(account['telegram_id']),str(account['parentRef']),str(account['ref'])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0]
        account['id'] = str(json.loads(output_addCustomer)['data'])[1:-1]
        msg = bot.send_message(message.chat.id, 'Регистрация прошла успешно. Ваша реферальная ссылка: \n<a href="https://t.me/AMLSrefbot?start='+account['ref']+'">https://t.me/AMLSrefbot?start='+account['ref']+'</a>.\nПриступить к работе в боте?',reply_markup=m.start_markup, parse_mode="Html")
        bot.register_next_step_handler(msg, register)
def menuWelcome(message):
    #print "Имя: "+str(account['name'])+", Телефон: "+str(account['phone'])+", id: "+str(account['id'])+", Родительская ссылка: "+str(account['parentRef'])+", Своя ссылка: "+str(account['ref'])
    if message.text == "Кошелек":
        checkWallet()
        if account['wallet_id'] == '':
            msg = bot.send_message(message.chat.id, 'Ваш кошелек не найден',reply_markup=m.authWallet_inline, parse_mode="Html")
            #bot.register_next_step_handler(msg, menuWallet_add_wallet)
        else:
            bot.send_chat_action(message.chat.id, 'typing')  
            msg = bot.send_message(message.chat.id, 'Найден номер кошелька в CRM id = '+account['wallet_id']+" \nБаланс: "+account['wallet_amount']+" руб.", reply_markup=m.walletMenu_markup, parse_mode="Html")
            print "Найден номер кошелька в CRM id = "+account['wallet_id']+" Баланс: "+account['wallet_amount']+" руб."
            bot.register_next_step_handler(msg, inWallet)  
    elif message.text == "Оставить заявку":
        try:
            bot.register_next_step_handler(msg, zayavka) 
        except Exception as e:
            print "Ошибка при вызове функции menuWelcome, при выполнении операции bot.register_next_step_handler(msg, zayavka)"
            msg = bot.send_message(message.chat.id, 'Не удалось выполнить команду, ошибка: '+str(e),reply_markup=m.menu_markup, parse_mode='Html')
            bot.register_next_step_handler(msg, menuWelcome)
        else:
            pass
        finally:
            pass
    elif message.text == "О сервисе":
        msg = bot.send_message(message.chat.id, 'Выпопали в сервис позволяющий (ВСТАВИТЬ ТЕКСТ ПРО РЕФЕРАЛЬНУЮ ПРОГРАММУ)',reply_markup=m.menu_markup, parse_mode='Html')
        bot.register_next_step_handler(msg, menuWelcome)
    elif message.text == "Проверить собственника":
        try:
            bot.register_next_step_handler(msg, check) 
        except Exception as e:
            print "Ошибка при вызове функции menuWelcome, при выполнении операции bot.register_next_step_handler(msg, check)"
            msg = bot.send_message(message.chat.id, 'Не удалось выполнить команду, ошибка: '+str(e),reply_markup=m.menu_markup, parse_mode='Html')
            bot.register_next_step_handler(msg, menuWelcome)
        else:
            pass
        finally:
            pass
    else:
        try:
            msg = bot.send_message(message.chat.id, 'Возвращаемся обратно',reply_markup=m.menu_markup, parse_mode='Html')
            bot.register_next_step_handler(msg, start_handler) 
        except Exception as e:
            print "Ошибка при вызове функции menuWelcome, при выполнении операции bot.register_next_step_handler(msg, ERROR)"
            msg = bot.send_message(message.chat.id, 'Не удалось выполнить команду, ошибка: '+str(e),reply_markup=m.menu_markup, parse_mode='Html')
            bot.register_next_step_handler(msg, menuWelcome)
        else:
            pass
        finally:
            pass
 #
 #
 #
 ######   WALLET    ######
 #
 #
 #   
@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    data = query.data
    if data == 'printWalletId':
       printWalletId_callback(query)
def printWalletId_callback(query):
    bot.answer_callback_query(query.id)
    printWalletId(query.message)
def printWalletId(message):
    text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    msg = bot.send_message(message.chat.id, 'Введите номер кошелька в формате 7**********', parse_mode='Html')
    bot.register_next_step_handler(msg, printWalletId_Error)
def printWalletId_Error(message):
    text = message.text
    if authMod.checkPhone(text):
        account['wallet_id'] = text  
        checkWalletId(message)
    else:
        msg = bot.send_message(message.chat.id, 'Неверный формат номера', parse_mode='Html')
        bot.register_next_step_handler(msg, printWalletId)
def checkWalletId(message):
    print "Добавление кошелька пользователю с CRMID: "+str(account['id'])+" с номером: "+str(account['wallet_id'])
    output_addCustomer = get_api.update_contact(str(account['id']),str(account['wallet_id']))
    #output_addCustomer = subprocess.Popen(['php', 'CRM_API/example/customer/update_contact.php', str(account['id']),str(account['wallet_id'])]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0]
    msg = bot.send_message(message.chat.id, 'Кошелек №'+account['wallet_id']+' добавлен',reply_markup=m.walletMenu_markup, parse_mode='Html')
    bot.register_next_step_handler(msg, inWallet)
def inWallet(message):
    if message.text == "Обновить баланс":
        checkWallet()
        msg = bot.send_message(message.chat.id, 'Кошелек № '+account['wallet_id']+" \nБаланс: "+account['wallet_amount']+" руб.", reply_markup=m.walletMenu_markup, parse_mode="Html")
        bot.register_next_step_handler(msg, inWallet)  
    elif message.text == "Вывести средства":
        checkWallet()
        msg = bot.send_message(message.chat.id, "Для вывода доступно: "+account['wallet_amount']+" руб.\nКакую суммы вы хотите вывести на свой счет?", reply_markup=m.walletMenu_markup_1, parse_mode="Html")
        #print msg.text 
        try:
            bot.register_next_step_handler(msg, walletPay) 
        except Exception as e:
            print "Ошибка при вызове функции inWallet, при выполнении операции bot.register_next_step_handler(msg, walletPay)"
            msg = bot.send_message(message.chat.id, 'Не удалось выполнить команду, ошибка: '+str(e),reply_markup=m.menu_markup, parse_mode='Html')
            bot.register_next_step_handler(msg, menuWelcome)
        else:
            pass
        finally:
            pass
    elif message.text == "В меню":
        msg = bot.send_message(message.chat.id, account['name']+", выберите пункт меню", reply_markup=m.menu_markup) 
        try:
            bot.register_next_step_handler(msg, menuWelcome)
        except Exception as e:
            print "Ошибка при вызове функции inWallet, при выполнении операции bot.register_next_step_handler(msg, menuWelcome)"
            msg = bot.send_message(message.chat.id, 'Не удалось выполнить команду, ошибка: '+str(e),reply_markup=m.menu_markup, parse_mode='Html')
            bot.register_next_step_handler(msg, menuWelcome)
        else:
            pass
        finally:
            pass
    elif message.text == "Статус вывода":
        msg = bot.send_message(message.chat.id, account['name']+", выберите транзакцию, чтобы узнать статус", reply_markup=m.menu_trsns) 
        try:
            bot.register_next_step_handler(msg, transactions) 
        except Exception as e:
            print "Ошибка при вызове функции inWallet, при выполнении операции bot.register_next_step_handler(msg, transactions) "
            msg = bot.send_message(message.chat.id, 'Не удалось выполнить команду, ошибка: '+str(e),reply_markup=m.menu_markup, parse_mode='Html')
            bot.register_next_step_handler(msg, menuWelcome)
        else:
            pass
        finally:
            pass
#def walletPay(message):
#def transactions(message):

 #
 #
 #
 ######   ZAYAVKA    ######
 #
 #
 #  

 #
 #
 #
 ######   CHECK    ######
 #
 #
 #  
bot.polling()

