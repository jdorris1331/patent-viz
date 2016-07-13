import MySQLdb
import json
import string

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
    if j not in stopwords and len (j) < 41:
      if j in index:
        if i[0] not in index[j]:
          index[j].append(i[0])
      else:
        index[j] = [i[0]]
      #print j
  temp = i[2].lower()
  for c in string.punctuation:
    temp = temp.replace(c,"")
  temp = temp.replace("brbr"," ")
  for j in temp.split():
    if j not in stopwords and len (j) < 41:
      if j in index:
        if i[0] not in index[j]:
          index[j].append(i[0])
      else:
        index[j] = [i[0]]

    
for i in index:
  #print i
  #print index[i]

  query = "INSERT INTO patent_index VALUES ( '{0}', '{1}' )".format(i, json.dumps(index[i]))
  cursor.execute(query)
  db.commit()

  #query = "SELECT ref FROM patent_info WHERE ID='{0}'".format(i[0])
  #cursor.execute(query)
  #ref = json.loads(cursor.fetchall()[0][0])
  #for j in ref:
  #  query = "SELECT EXISTS(SELECT * FROM patent_info WHERE ID='{0}')".format(j)
  #  cursor.execute(query)
  #  exists = cursor.fetchall()
  #  print "  {0}-{1}".format(j,exists[0][0])
  #  if exists[0][0] == "1":
      #SELECT ref_by
      #if NULL create [] else loads and append then dumps
  #    print "  {0}".format(j)

  #db.commit()

db.close()


