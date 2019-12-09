#! /usr/bin/env python
# -*- coding: utf-8 -*-
from telebot import types
#YES-NO клавиатура
yn_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
yn_markup_btn1 = types.KeyboardButton('Да')
yn_markup_btn2 = types.KeyboardButton('Нет')
yn_markup.add(yn_markup_btn1)
yn_markup.add(yn_markup_btn2)
yn_markup_remove=types.ReplyKeyboardRemove() 
#askRegister клавиатура
start_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
start_markup_btn1 = types.KeyboardButton('Да')
start_markup_btn2 = types.KeyboardButton('Узнать больше')
start_markup.add(start_markup_btn1)
start_markup.add(start_markup_btn2)
start_markup_remove=types.ReplyKeyboardRemove() 
#menuMarkUp
menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
menu_markup_btn1 = types.KeyboardButton('Кошелек')
menu_markup_btn2 = types.KeyboardButton('Оставить заявку')
menu_markup_btn3 = types.KeyboardButton('О сервисе')
menu_markup_btn4 = types.KeyboardButton('Проверить собственника')
menu_markup.add(menu_markup_btn1)
menu_markup.add(menu_markup_btn2)
menu_markup.add(menu_markup_btn3)
menu_markup.add(menu_markup_btn4)
#authWallet_inline
authWallet_inline = types.InlineKeyboardMarkup()
authWallet_inline_btn1 = types.InlineKeyboardButton("Создать кошелек", url="https://qiwi.com/register/form.action")
authWallet_inline_btn2 = types.InlineKeyboardButton("Ввести номер кошелька", callback_data="printWalletId")
authWallet_inline.add(authWallet_inline_btn1,authWallet_inline_btn2)
#walletMenu_markup
walletMenu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
walletMenu_markup_btn1 = types.KeyboardButton('Обновить баланс')
walletMenu_markup_btn2 = types.KeyboardButton('Вывести средства')
walletMenu_markup_btn3 = types.KeyboardButton('В меню')
walletMenu_markup.add(walletMenu_markup_btn1)
walletMenu_markup.add(walletMenu_markup_btn2)
walletMenu_markup.add(walletMenu_markup_btn3)

#walletMenu_markup
walletMenu_markup_1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
walletMenu_markup_1_btn1 = types.KeyboardButton('Обновить баланс')
walletMenu_markup_1_btn2 = types.KeyboardButton('Статус вывода')
walletMenu_markup_1_btn3 = types.KeyboardButton('В меню')
walletMenu_markup_1.add(walletMenu_markup_btn1)
walletMenu_markup_1.add(walletMenu_markup_btn2)
walletMenu_markup_1.add(walletMenu_markup_btn3)
