import MySQLdb
from gensim import corpora, models, similarities


#class MyCorpus(object):
#    def __iter__(self):
#        for line in open('mycorpus.txt'):
#            # assume there's one document per line, tokens separated by whitespace
#            yield dictionary.doc2bow(line.lower().split())



db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID,claims,abstract FROM patent_data limit 10" 
cursor.execute(query)
output = cursor.fetchall()

dictionary = corpora.Dictionary.load('patents20k.dict')
corpus = corpora.MmCorpus('patents20k.mm')
tfidf = models.TfidfModel.load("model.tfidf") # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel.load("model.lsi")
corpus_lsi = lsi[corpus_tfidf]

index = similarities.MatrixSimilarity(lsi[corpus])

documents = [row[1] + row[2] for row in output]
for doc in documents:
  vec_bow = dictionary.doc2bow(doc.lower().split())
  vec_lsi = lsi[vec_bow]
  sims = index[vec_lsi]
  sims = sorted(enumerate(sims), key=lambda item: -item[1])
  print(sims[0:10])
  print
  print


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

