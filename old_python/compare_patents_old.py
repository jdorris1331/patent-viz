import MySQLdb
import json
from gensim import corpora, models, similarities


#class MyCorpus(object):
#    def __iter__(self):
#        for line in open('mycorpus.txt'):
#            # assume there's one document per line, tokens separated by whitespace
#            yield dictionary.doc2bow(line.lower().split())


colors = ["#F7271D","#F63D1B","#F55419","#F46B18","#F38316","#F29A14","#F1B213","#F0C911","#EFE110","#E3EE0E","#C9ED0D","#AFEC0B","#94EB0A","#7AEA08","#60E907","#45E805","#2AE704","#0FE602","#01E50D","#00E525"]


db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID,claims,abstract FROM patent_data limit 100000 #offset 80214" 
cursor.execute(query)
output = cursor.fetchall()

dictionary = corpora.Dictionary.load('patents.dict')
corpus = corpora.MmCorpus('patents.mm')
tfidf = models.TfidfModel.load("model.tfidf") # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel.load("model.lsi")
corpus_lsi = lsi[corpus_tfidf]

#index = similarities.MatrixSimilarity(lsi[corpus])
index = similarities.MatrixSimilarity.load('patents.index')
#print "index finished"
documents = [[row[0],row[1] + row[2]] for row in output]
scan = 0
for doc in documents:
  if scan%100 == 0:
    print scan
  scan += 1
  #print doc[0]
  vec_bow = dictionary.doc2bow(doc[1].lower().split())
  vec_lsi = lsi[vec_bow]
  sims = index[vec_lsi]
  sims = sorted(enumerate(sims), key=lambda item: -item[1])
  temp = sims[0:10]
%  add = []
%  for i in temp:
%    query = "SELECT ID,title FROM patent_info limit 1 offset {0}".format(i[0])
%    cursor.execute(query)
%    output = cursor.fetchall()
%    add += [[output[0][0],output[0][1],"%.4f" % i[1]]]
  
  print(sims[0:10])
  #print 
  #print
  #print
%  query = "UPDATE patent_info SET similar='{0}' WHERE ID='{1}'".format(json.dumps(add),doc[0])
%  cursor.execute(query)
%  db.commit()
  #print query

db.close()


#frequency = defaultdict(int)

#stopwords = {}
#with open("stopwords.txt", 'r') as f:
#  for line in f:
#    stopwords[line.strip()] = 1 


#documents = [row[1] + row[2] for row in output]
#for i in range(0,len(documents)):
#  for c in string.punctuation:
#    documents[i] = documents[i].replace(c,"")
#  documents[i] = documents[i].replace("brbr"," ")

#texts = [[word for word in document.lower().split() if word not in stopwords]
#         for document in documents]

