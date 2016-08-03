import MySQLdb
import json
import string
import operator
import math
import nltk
from collections import defaultdict,Counter
from gensim import corpora, models, similarities
from nltk.stem.porter import *

#class MyCorpus(object):
#    def __iter__(self):
#        for line in open('mycorpus.txt'):
#            # assume there's one document per line, tokens separated by whitespace
#            yield dictionary.doc2bow(line.lower().split())



db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID,claims,abstract FROM patent_data limit 100000" 
cursor.execute(query)
output = cursor.fetchall()

frequency = defaultdict(int)


stopwords = {}
with open("stopwords.txt", 'r') as f:
  for line in f:
    stopwords[line.strip()] = 1

stemmer = PorterStemmer()
documents = [row[1] + row[2] for row in output]
for i in range(0,len(documents)):
  for c in string.punctuation:
    documents[i] = documents[i].replace(c,"")
  documents[i] = documents[i].replace("brbr"," ")

texts = [[stemmer.stem(word) for word in document.lower().split() if not word in stopwords]
         for document in documents]
#texts = [[word for word in document.lower().split() if not word in stopwords]
#         for document in documents]

for text in texts:
  for token in text:
    frequency[token] +=1
print "created frequency"

#print len(frequency) 
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]
print "removed single words"

#sum = 0
#for token in frequency: 
#  if frequency[token] > 1:
#    sum+=1
#print sum
dictionary = corpora.Dictionary(texts)
print "created dictionary"
dictionary.save('patents.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
print "created corpus"
corpora.MmCorpus.serialize('patents.mm', corpus)
   
db.close()


