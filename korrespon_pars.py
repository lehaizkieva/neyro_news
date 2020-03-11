import telebot
import random
import os
from telebot import types
import requests
from bs4 import BeautifulSoup as bs

URL = 'https://korrespondent.net/Default.aspx?page_id=60&lang=ru&stx=%D0%BD%D0%B1%D1%83&roi=0&st=1'
HEADERS = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
HOST = 'https://korrespondent.net'

# Функция получкния HTML
def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	session = requests.Session()
	request = session.get(url, headers=HEADERS)
	return r


# Функция сбора
def get_content(html):
	soup = bs(html, 'html.parser')
	divs = soup.find_all('div', attrs={'class': 'article article_rubric_top'})
	news = []
	for div in divs:
		title = div.find('div', attrs={'class': 'article__title'}).get_text(strip=True)
		link = div.find('a')['href']
		rubric = div.find('a', attrs={'class': 'article__rubric'}).get_text(strip=True)
		date = div.find('div', attrs={'class': 'article__date'}).get_text(strip=True)
		news.append({
			'title': title,
			'link': link,
			'rubric': rubric,
			'date': date,
			})

		print(len(news))
	print(news)


# Основная функция
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
    else:
        print('Error')


parse()