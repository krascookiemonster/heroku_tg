#подключаем бибилиотеку request
import requests
#подключаем бибилиотеку BeautifulSoup
from bs4 import BeautifulSoup
#создаем список для хранения данных о товарах
d=[]

# получаем страницы при помощи цикла
for j in range(50):
    #указываем url и get параметры запроса
    url = 'https://biggeek.ru/catalog/apple-iphone'
    # указываем get параметр с помощью которого определяется номер страницы
    par = {'page': j}
    # записываем ответ сервера в переменную r
    r = requests.get(url, params=par)
    # получаем объект  BeautifulSoup и записываем в переменную soup
    soup = BeautifulSoup(r.text, 'html.parser')
    # с помощью циклам перебераем товары на странице и получаем из них нужные параметры
    for i in range(20):
           # получаем название товара
           product = soup.find_all('a', class_='title')[i].get_text()
           # получаем цену товара
           price = soup.find_all(class_='price')[i].get_text()
           # удаляем пробел из цены
           price = price.replace(" ", "")
           #получаем ссылку на товар
           link = soup.find_all('a', class_='title')[i]['href']
           #добавляем домен к ссылке
           link = 'https://biggeek.ru/' + link
           # добавляем данные о товаре в список
           d.append([product, price, link])
 
#открываем файл на запись
with open('product.csv', 'w') as ouf:
        #перебираем элементы списка d
        for i in d:
            #преобразуем элемент списка в строку
            i=str(i)
            #очищаем строку от ненужных символов
            i=i.replace("\'", "")
            i=i.replace("[", "")
            i=i.replace("]", "")
            #записываем строку в файл
            ouf.write(i + '\n')