import MySQLdb
import json
from gensim import corpora, models, similarities
import sys
from nltk.stem.porter import *




db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

#query = "SELECT ID FROM patent_data limit 30000 offset 70700" #offset 80214" 
#cursor.execute(query)
#output = cursor.fetchall()

message = sys.argv[1]

dictionary = corpora.Dictionary.load('patents.dict')
corpus = corpora.MmCorpus('patents.mm')
tfidf = models.TfidfModel.load("model.tfidf") # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel.load("model.lsi")
corpus_lsi = lsi[corpus_tfidf]

index = similarities.MatrixSimilarity.load('patents.index')
#documents = output
stemmer = PorterStemmer()
text = [stemmer.stem(word) for word in message.lower().split()]
vec_bow = dictionary.doc2bow(text)
vec_lsi = lsi[vec_bow]
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
temp = sims[0:10]
with open("log",'w') as f:
  f.write(str(vec_lsi))
  for i in sims:
    f.write(str(i))
    f.write("\n")
add = []
for i in temp:
  query = "SELECT ID,title FROM patent_info limit 1 offset {0}".format(i[0])
  cursor.execute(query)
  output = cursor.fetchall()
  add += [{"id": output[0][0],"title": output[0][1] }]
  
print json.dumps(add)

db.close()
