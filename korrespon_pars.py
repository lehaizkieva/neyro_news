import telebot
import random
import os
from telebot import types
import requests
from bs4 import BeautifulSoup as bs
import csv

URL = 'https://korrespondent.net/Default.aspx?page_id=60&lang=ru&isd=1&roi=0&tp=0&st=1&stx=%D0%BD%D0%B1%D1%83&y='
HEADERS = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
HOST = 'https://korrespondent.net'
FILE = 'news_f_korre.csv'

# Функция получкния HTML
def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	session = requests.Session()
	request = session.get(url, headers=HEADERS)
	return r

# Функция получения страниц запроса
def get_pages_count(html):
	soup = bs(html, 'html.parser')
	pagination = soup.find_all('a', attrs={'class': 'pagination__link'})
	if pagination:
		return int(pagination[-2].text)
	else:
		return 1


# Функция сбора
def get_content(html):
	soup = bs(html, 'html.parser')
	divs = soup.find_all('div', attrs={'class': 'article article_rubric_top'})
	news = []
	for div in divs:
		title = div.find('div', attrs={'class': 'article__title'}).get_text(strip=True)
		link = div.find('a')['href']
		rubric = div.find('a', attrs={'class': 'article__rubric'}).get_text(strip=True)
		date = div.find('div', attrs={'class': 'article__date'})
		date = (str(date))
		date = (date[date.find("</a>") + 4 :])
		date = (date[: - 24 :])
		print(date)
		news.append({
			'title': title,
			'link': link,
			'rubric': rubric,
			'date': date,
			})
	print(news)
	print(len(news))
	return news


def save_file(items, path):
	with open(path, 'w', newline='', encoding='utf8') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Тема', 'Ссылка', 'Рубрика', 'Дата'])
		for item in items:
			writer.writerow([item['title'], item['link'], item['rubric'], item['date']])


# Основная функция
def parse():
    html = get_html(URL)
    if html.status_code == 200:
    	news = []
    	pages_count = 4 #get_pages_count(html.text)
    	get_content(html.text)   	
    	for page in range(1, pages_count + 1):    		
    		print(f'Парсинг страницы {page} из {pages_count}...')
    		html = get_html(URL, params={'p': page})
    		news.extend(get_content(html.text))
    	print(f'Получено {len(news)} новостей')
    	save_file(news, FILE)    	
    else:
    	print('Error')
			

parse()