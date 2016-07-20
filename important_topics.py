import MySQLdb
import json
import operator

db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID FROM patent_info" 
cursor.execute(query)
output = cursor.fetchall()

scan = 0
topics = {}
for i in output:
  if scan%100 == 0:
    print scan
  query = "SELECT topics FROM patent_info WHERE ID='{0}'".format(i[0])
  cursor.execute(query)
  try:
    ref = json.loads(cursor.fetchall()[0][0])
    if ref != "NULL":
      for j in ref:
        try:
          if j in topics:
            topics[j] = topics[j]+1
          else:
            topics[j] = 1
        except:
          pass
  except:
    pass
  scan = scan + 1

sorted = sorted(topics.items(), key=operator.itemgetter(1), reverse=True)

for i in sorted:
  print i[0],
  print " ",
  print i[1]
