import MySQLdb
import json
import string
import operator
import math
from collections import defaultdict
from gensim import corpora, models, similarities


#class MyCorpus(object):
#    def __iter__(self):
#        for line in open('mycorpus.txt'):
#            # assume there's one document per line, tokens separated by whitespace
#            yield dictionary.doc2bow(line.lower().split())



db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID,claims,abstract FROM patent_data limit 20000" 
cursor.execute(query)
output = cursor.fetchall()

frequency = defaultdict(int)

stopwords = {}
with open("stopwords.txt", 'r') as f:
  for line in f:
    stopwords[line.strip()] = 1


documents = [row[1] + row[2] for row in output]
for i in range(0,len(documents)):
  for c in string.punctuation:
    documents[i] = documents[i].replace(c,"")
  documents[i] = documents[i].replace("brbr"," ")

texts = [[word for word in document.lower().split() if word not in stopwords]
         for document in documents]

for text in texts:
  for token in text:
    frequency[token] +=1
print "created frequency"
 
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]
print "removed single words"

dictionary = corpora.Dictionary(texts)
print "created dictionary"
dictionary.save('patents.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
print "created corpus"
corpora.MmCorpus.serialize('patents.mm', corpus)
   
#tfidf = models.TfidfModel(corpus)
#print "created tfidf model"
#corpus_tfidf = tfidf[corpus]
#print "created tfidf"

#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=500)
#print "created lsi model"
#corpus_lsi = lsi[corpus_tfidf]
#print "created lsi"
#index = similarities.MatrixSimilarity(corpus_lsi)
#print "performed similarity"

#print lsi.print_topics(500)
 
#for i in corpus_lsi:
  #print i
  #print " ",

  #query = "INSERT INTO patent_index VALUES ( '{0}', '{1}' )".format(i, json.dumps(index[i]))
  #cursor.execute(query)
  #db.commit()

db.close()


