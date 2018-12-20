#!/usr/bin/env python
# encoding: utf-8

"""
Extract news and summorize with BeautifulSoup as bs4
"""

__author__ = 'Aazim'

import bs4 as bs  
import urllib.request  
import re
import nltk
import heapq

scraped_data = urllib.request.urlopen('https://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:  
	article_text += p.text

article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

#Tokenizing sentences
sentence_list = nltk.sent_tokenize(article_text)

stopwords = nltk.corpus.stopwords.words('english')

sent_occurrence = {}  
for word in nltk.word_tokenize(formatted_article_text):  
	if word not in stopwords:
		if word not in sent_occurrence.keys():
			sent_occurrence[word] = 1
		else:
			sent_occurrence[word] += 1

maximum_frequncy = max(sent_occurrence.values())

#Calculating the frequency of occurrence of words
for word in sent_occurrence.keys():
	sent_occurrence[word] = (sent_occurrence[word]/maximum_frequncy)

sent_frequencies = {}
for sent in sentence_list:  
	for word in nltk.word_tokenize(sent.lower()):
		if word in sent_occurrence.keys():
			if len(sent.split(' ')) < 30:
				if sent not in sent_frequencies.keys():
					sent_frequencies[sent] = sent_occurrence[word]
				else:
					sent_frequencies[sent] += sent_occurrence[word]


summary_sentences = heapq.nlargest(9, sent_frequencies, key=sent_frequencies.get)

summary = ' '.join(summary_sentences)
print(summary)