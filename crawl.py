from bs4 import BeautifulSoup
import requests
import codecs
import os


def Title(name):
	for i in range(1,len(name)):
		if (name[i] == '/'):
			return i + 1

def WriteData(i,url):
	text = ""
	web_2 = requests.get(url + i)
	beutifulsoup_2 = BeautifulSoup(web_2.content, 'html.parser')
	
	try:
		tieude = beutifulsoup_2.find("h1", class_="fon31 mgb15")
		text = text + tieude.text[6:] + ". \n"
		first_2 = beutifulsoup_2.find("div", class_="clearfix adm-mainsection").find("div", class_="fon34 mt3 mr2 fon43 detail-content").find_all("p")
		for j in first_2:
			text = text + j.text + "\n"
		file1 = codecs.open('./Data/' + i[Title(i):-4] + ".txt", "w", "utf-8")
		print(text, file = file1)
		file1.close()	
	except Exception:
		pass
	
def start_crawl():
	location = 2
	url = "http://dantri.com.vn/"
	web = requests.get(url)
	beautifulsoup = BeautifulSoup(web.content, 'html.parser')
	first = beautifulsoup.find("div", class_="nav-wrap")
	second = first.find("ul", class_="nav").find_all("a")
	for item in range(location, len(second)):

		print(location)
		if (location != 11):
			page = 2 
			link = second[item].get("href")
			web_1 = requests.get(url + link)
			print(url + link)
			beutifulsoup_1 = BeautifulSoup(web_1.content, 'html.parser')
			first_1 = beutifulsoup_1.find("div", class_="fl wid470").find_all("div",class_="clearfix")
			link = []
			try:
				for i in first_1:
					link.append(i.a.get('href'))
			except Exception:
				pass
			temp_link = link[-1]
			del(link[-1])
			for i in link:
				WriteData(i,url)	
			for i in range(0, 10):
				link.clear()
				print(i)
				web_1 = requests.get(url + temp_link) 
				beutifulsoup_1 = BeautifulSoup(web_1.content, 'html.parser')
				first_1 = beutifulsoup_1.find("div", class_="fl wid470").find_all("div",class_="clearfix")
				try:
					for j in first_1:
						link.append(j.a.get('href'))
				except Exception:
					pass
				temp_link = link[-1]
				del(link[-1])
				for l in link:
					WriteData(l,url)
		location = location + 1
def stop_crawl():
	pass