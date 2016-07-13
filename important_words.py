import MySQLdb
import json
import string
import operator

db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID,claims,abstract FROM patent_data" 
cursor.execute(query)
output = cursor.fetchall()

index = {}

stopwords = []
with open("stopwords.txt", 'r') as f:
  for line in f:
    stopwords += [line.strip()]

for i in output:
  #print i[0]
  temp = i[1].lower()
  for c in string.punctuation:
    temp = temp.replace(c,"")
  temp = temp.replace("brbr"," ")
  for j in temp.split():
    if j not in stopwords:
      if j in index:
        index[j] = index[j]+1
      else:
        index[j] = 1
      #print j
  temp = i[2].lower()
  for c in string.punctuation:
    temp = temp.replace(c,"")
  temp = temp.replace("brbr"," ")
  for j in temp.split():
    if j not in stopwords:
      if j in index:
        index[j] = index[j] + 1
      else:
        index[j] = 1

sorted_index = sorted(index.items(), key=operator.itemgetter(1)) 
    
for i in sorted_index:
  print i[0],
  print " ",
  print i[1]

  #query = "INSERT INTO patent_index VALUES ( '{0}', '{1}' )".format(i, json.dumps(index[i]))
  #cursor.execute(query)
  #db.commit()

db.close()


