import MySQLdb
import json
import operator

db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID FROM patent_info" 
cursor.execute(query)
output = cursor.fetchall()

scan = 0
referenced_patents = {}
for i in output:
  if scan%100 == 0:
    print scan
  query = "SELECT ref FROM patent_info WHERE ID='{0}'".format(i[0])
  cursor.execute(query)
  ref = json.loads(cursor.fetchall()[0][0])
  if ref != "NULL":
    for j in ref:
      try:
        temp = int(j.encode('ascii','ignore'))
        if temp in referenced_patents:
          referenced_patents[temp] = referenced_patents[temp]+1
        else:
          referenced_patents[temp] = 1
      except:
        pass
  scan = scan + 1

sorted = sorted(referenced_patents.items(), key=operator.itemgetter(1), reverse=True)

for i in sorted:
  print i[0],
  print " ",
  print i[1]
