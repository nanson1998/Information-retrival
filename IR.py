import collections
import threading
import os
import re
import math
import json
import codecs
from itertools import islice

def Stopwords(path):
	file =  codecs.open("stopWords.txt", "r", "UTF-8")
	conTent = file.read().split('\n')
	del(conTent[0])
	file.close()
	return conTent

def Build():
	sw = Stopwords("stopWords.txt")
	invertedIndex("./Data/", sw)
	txt = codecs.open('Invented.txt', 'r', 'utf-8')
	conTent = json.load(txt)
	txt.close()
	TF_IDF("./Data/", conTent)

def TF_IDF(path, words):
	allFile = os.listdir(path)
	tf_idf = {}
	for i in words:
		tf_idf[i] = {}
		y = 1.0 + math.log10(float(len(allFile) / len(words[i])))
		for j in allFile:
			if(j in words[i]):
				file = codecs.open(path + j, "r", 'utf-8')
				conTent = file.read().lower()
				file.close()
				conTent = re.sub(r'[-|?|$|.|!|"|,|(|)|/|_|\'|`|*|+|@|#|%|^|&|[|]|{|}|;|:|<|>|]',r' ', conTent)
				listConTent = list(conTent.split())
				tf_idf[i][j] = (y * (words[i][j] / len(listConTent)))
	with codecs.open("TF_IDF.txt", "w", "UTF-8") as fp:
		json.dump(tf_idf, fp)


def invertedIndex(path, stopwords):

	allFile = os.listdir(path)
	inverted_index = {}
	stop_words = re.compile(r"\b(" + "|".join(stopwords) + ")\\W")
	for i in allFile:
		file = codecs.open(path + i, "r", "utf-8")
		conTent = file.read().lower()
		file.close()
		conTent = re.sub(stop_words,r' ', conTent)
		conTent = re.sub(r'[-|?|$|.|!|"|,|(|)|/|_|\'|`|*|+|@|#|%|^|&|[|]|{|}|;|:|<|>|]',r' ', conTent)
		listConTent = list(conTent.split())
		del(listConTent[0])
		for j in listConTent:
			if(j not in inverted_index):
				inverted_index[j] = {}
			if(i not in inverted_index[j]):
				inverted_index[j][i] = 1
			else:
				inverted_index[j][i] += 1


	with codecs.open("Invented.txt", "w", "UTF-8") as fp:
		json.dump(inverted_index, fp)	


	
def query_TF_IDF(path, words, query):
	allFile = os.listdir(path)
	file = []
	TF_IDF_QUERY = {}
	list_query = list(query.lower().split())
	for i in list_query:
		if(i in words):
			for j in words[i]:
				file.append(j)
			x = 0.0
			y = 1.0 + math.log10(float(len(allFile) / len(words[i])))
			for l in list_query:
				if(l == i):
					x += 1.0
			x /= len(query.split())
			TF_IDF_QUERY[i] = x * y
	return TF_IDF_QUERY, file


def calCosine(TF_IDF, query, TF_IDF_QUERY, file, cosine, threadLocation):
	start = int(len(file) / 100 *(threadLocation - 1))
	stop = int((len(file) / 100)*threadLocation - 1)
	for i in range(start,stop + 1):
		sum = 0.0
		c1 = 0.0
		c2 = 0.0
		cosine[file[i]] = []
		for j in TF_IDF:
			if(file[i] in TF_IDF[j]):
				if(j in TF_IDF_QUERY):
					sum += (TF_IDF[j][file[i]] * TF_IDF_QUERY[j])
					c1 += (TF_IDF[j][file[i]]**2)
					c2 += (TF_IDF_QUERY[j]**2)
				else:
					c1 += (TF_IDF[j][file[i]]**2)
			else:
				if(j in TF_IDF_QUERY):
					c2 += (TF_IDF_QUERY[j]**2)
		if(c1 * c2 != 0.0):
			cosine[file[i]].append(sum / (math.sqrt(c1) * math.sqrt(c2)))

def listCosine(query):
	Build()
	temp = codecs.open("TF_IDF.txt", 'r', 'UTF-8')
	TF_IDF = json.load(temp)
	temp.close()
	TF_IDF_QUERY, file = query_TF_IDF("./Data/", TF_IDF, query)
	threads = []
	cosine = {}

	for i in range(1, 101):
		t = threading.Thread(target = calCosine, args = (TF_IDF, query, TF_IDF_QUERY, file, cosine, i))
		threads.append(t)

	for i in threads:
		i.start()

	for i in threads:
		i.join()

	cosine = dict(collections.OrderedDict(sorted(cosine.items(), key = lambda kv: kv[1], reverse = True)))
	keys = list(islice(cosine, 30))
	list_cosine = {}
	for i in keys:
		list_cosine[i] = cosine[i]
	return list_cosine

def calDistance(TF_IDF, query, TF_IDF_QUERY, file, distance, currentThread):
	start = int(len(file) / 100 *(currentThread - 1))
	stop = int((len(file) / 100)*currentThread - 1)
	for i in range(start,stop + 1):
		d = 0.0
		distance[file[i]] = []
		for j in TF_IDF:
			if(file[i] in TF_IDF[j]):
				if(j in TF_IDF_QUERY):
					d += (TF_IDF[j][file[i]] - TF_IDF_QUERY[j])**2
				else:
					d += TF_IDF[j][file[i]]**2
			else:
				if(j in TF_IDF_QUERY):
					d += TF_IDF_QUERY[j]**2
		distance[file[i]].append(math.sqrt(d))
		
def listDistance(query):
	Build()
	temp = codecs.open("TF_IDF.txt", 'r', 'UTF-8')
	TF_IDF = json.load(temp)
	temp.close()
	TF_IDF_QUERY, file = query_TF_IDF("./Data/", TF_IDF, query)
	threads = []
	distance = {}

	for i in range(1, 101):
		t = threading.Thread(target = calDistance, args = (TF_IDF, query, TF_IDF_QUERY, file, distance, i))
		threads.append(t)

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	distance = dict(collections.OrderedDict(sorted(distance.items(), key = lambda kv: kv[1])))
	keys = list(islice(distance, 30))
	list_distance= {}
	for i in keys:
		list_distance[i] = distance[i]
	return list_distance




