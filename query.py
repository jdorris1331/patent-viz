import MySQLdb
import json
from gensim import corpora, models, similarities
import sys
from nltk.stem.porter import *
import string




db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID,title FROM patent_info limit 100000" #offset 80214" 
cursor.execute(query)
output = cursor.fetchall()


#message = """ Enhanced methods and systems for human-pet communication are described. Example embodiments provide an Internet Canine Communication System (ICCS). The ICCS facilitates remote communication and interaction with between a dog and its owner, caretaker, trainer, family member, or the like. The ICCS may include a base station or similar device that is configured to deliver treats to a dog and to transmit audio/visual communication between the dog and a remote client device operated by a human user. The ICCS may also facilitate training the dog to utilize the ICCS to communicate with the user, such as by answering calls from or initiating calls to the remote client device of the user. """ 
#message = " Apparatus and method for combining network conferences that are not co-located " 

message = sys.argv[1]
message = message.encode('ascii', 'ignore')

for c in string.punctuation:
  message = message.replace(c,"")

stemmer = PorterStemmer()
text = [stemmer.stem(word).encode('ascii','ignore') for word in message.lower().split()]
#print text

#sys.argv[1]

dictionary = corpora.Dictionary.load('patents.dict')
#corpus = corpora.MmCorpus('patents.mm')
tfidf = models.TfidfModel.load("model.tfidf") # step 1 -- initialize a model
#corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel.load("model.lsi")
#corpus_lsi = lsi[corpus_tfidf]
#print corpus_lsi

index = similarities.MatrixSimilarity.load('patents.index')
##documents = output
##stemmer = PorterStemmer()
##text = [stemmer.stem(word) for word in message.lower().split()]
vec_bow = dictionary.doc2bow(text)
#print vec_bow
tfidf_vec = tfidf[vec_bow]
vec_lsi = lsi[tfidf_vec]
#print vec_lsi
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
temp = sims[0:50]
#print 
#print
#print temp
##with open("log",'w') as f:
##  f.write(str(vec_lsi))
##  for i in sims:
##    f.write(str(i))
##    f.write("\n")
add = []
for i in temp:
  #query = "SELECT ID,title FROM patent_info limit 1 offset {0}".format(i[0])
  #cursor.execute(query)
  #output = cursor.fetchall()
  add += [{"id": output[i[0]][0],"title": output[i[0]][1] }]
  
print json.dumps(add)
#
#db.close()
