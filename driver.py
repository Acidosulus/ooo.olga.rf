from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from bs4 import BeautifulSoup as BS
from lxml import html
import requests
from click import echo, style
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import uuid

class WD:
	def init(self):
		self.site_url = 'https://ооо-ольга.рф/'
		config = configparser.ConfigParser()


		
	def __init__(self):
		self.init()
		if False:
			chrome_options = webdriver.ChromeOptions()
			chrome_prefs = {}
			chrome_options.experimental_options["prefs"] = chrome_prefs
			chrome_options.add_argument('--disable-gpu')
			chrome_options.add_argument("--disable-notifications")
			#chrome_options.add_argument('--headless')
			self.driver = webdriver.Chrome(options=chrome_options)
			self.driver.maximize_window()

	def __del__(self):
		try:
			self.driver.quit()
		except: pass

	def Get_HTML(self, curl):
		if False:
			if os.path.isfile('response.html'):
					echo(style('Загружен локальный файл: ', fg='bright_red') + style('response.html', fg='red'))
					self.page_source = file_to_str('response.html')
			else:
				r = requests.get(curl)
				self.page_source = r.text
				str_to_file('response.html', self.page_source)
		else:
			#r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
			r = requests.get(curl)
			self.page_source = r.text
			#str_to_file(file_path="response.html", st = r.text)
			#self.driver.get(curl)
			#self.page_source = self.driver.page_source
			#return self.page_source
		return self.page_source

	def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link:str) -> list:
		echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white'))
		list_of_pages =  self.Get_List_of_Catalog_Pages(pc_link)
		echo(style('Стрaницы каталога: ', fg='bright_yellow') + style(str(list_of_pages), fg='green'))
		ll_catalog_items = []
		for link in list_of_pages:
			self.Get_HTML(link)
			soup = BS(self.page_source, features='html5lib')
			items = soup.find_all('a', {'class': 'ast-loop-product__link'})
			for item in items:
				lc_link = item['href']
				echo(style('Товар каталога: ', fg='bright_green') + style(lc_link, fg='green'))
				append_if_not_exists(lc_link, ll_catalog_items)
		return ll_catalog_items

	
	def Get_List_of_Catalog_Pages(self, pc_href:str) -> list:
		ll = []
		lc = pc_href
		self.Get_HTML(pc_href)
		soup = BS(self.page_source, features='html5lib')
		try:
			paginator =soup.find('a',{'class':'next page-numbers'})['href']
			lc_last_page_number = sx(''.join(reversed(paginator)), '/', '/')
			print(paginator, '    => ', lc_last_page_number)
			for number in range(1,int(lc_last_page_number)+1):
				append_if_not_exists(f'{pc_href}page/{number}/', ll)
		except:
			ll = [pc_href]
		return ll

		
	def Write_To_File(self, cfilename):
		file = open(cfilename, "w", encoding='utf-8')
		file.write(self.page_source)
		file.close()


def Login():
	return WD()


#colorama.init()
#wd = Login()
#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://ооо-ольга.рф/magazin/vesna-osen/'))
