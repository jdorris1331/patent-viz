import MySQLdb
import json
import string
import operator
import math

db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID,claims,abstract FROM patent_data" 
cursor.execute(query)
output = cursor.fetchall()

stopwords = []
with open("stopwords.txt", 'r') as f:
  for line in f:
    stopwords += [line.strip()]

idf = {}
with open("idf_cut.txt", "r") as f:
  for line in f:
    idf[line.split()[0]] = line.split()[1]

doc_words_count = {}
for i in output:
  print i[0]
  #print
  temp = i[1].lower()
  for c in string.punctuation:
    temp = temp.replace(c,"")
  temp = temp.replace("brbr"," ")
  for j in temp.split():
    if j not in stopwords:
      if j in doc_words_count:
        doc_words_count[j] = doc_words_count[j]+1
      else:
        doc_words_count[j] = 1
  temp = i[2].lower()
  for c in string.punctuation:
    temp = temp.replace(c,"")
  temp = temp.replace("brbr"," ")
  for j in temp.split():
    if j not in stopwords:
      if j in doc_words_count:
        doc_words_count[j] = doc_words_count[j]+1
      else:
        doc_words_count[j] = 1

  for j in doc_words_count:
    if j in idf:
      doc_words_count[j] = (1.0+math.log(doc_words_count[j]))*float(idf[j])
    else:
      doc_words_count[j] = (1.0+math.log(doc_words_count[j]))*10.6157753766

  sort_dict = sorted(doc_words_count.items(), key=operator.itemgetter(1), reverse=True) 
    
  important_words = []
  if len(sort_dict) > 9:
    for j in range(0,10):
      important_words += [sort_dict[j][0]]
    #for j in important_words:
      #print j
    doc_words_count.clear()
    query = "UPDATE patent_info SET topics='{0}' WHERE ID='{1}'".format(json.dumps(important_words),i[0])
    cursor.execute(query)
    db.commit()

db.close()


