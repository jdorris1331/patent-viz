import MySQLdb
import json

db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID FROM patent_info" 
cursor.execute(query)
output = cursor.fetchall()

for i in output:
  print i #output[i][0]  
  query = "SELECT ref FROM patent_info WHERE ID='{0}'".format(i[0])
  cursor.execute(query)
  ref = json.loads(cursor.fetchall()[0][0])
  for j in ref:
    query = "SELECT EXISTS(SELECT * FROM patent_info WHERE ID='{0}')".format(j)
    cursor.execute(query)
    exists = cursor.fetchall()
    print "  {0}-{1}".format(j,exists[0][0])
    if exists[0][0] == "1":
      #SELECT ref_by
      #if NULL create [] else loads and append then dumps
      print "  {0}".format(j)

  #db.commit()

db.close()


