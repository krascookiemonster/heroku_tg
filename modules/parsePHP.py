#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess
import sys
import checkId
#Функции взаимодействия с php возвращают JSON строку или просто выполняет запрос

#Функция запроса к CRM для получения строки в JSON
#url - сслыка на исполняемый файл
#args - аргументы (обязательно в виде str(аргумент))
"""def parseByUrl(url, *args):
	output = json.loads(subprocess.Popen(['php', url, args]+ sys.argv[1:], stdout=subprocess.PIPE).communicate()[0])
	return output"""
print checkUser.findTelegramIdInCRM("123")