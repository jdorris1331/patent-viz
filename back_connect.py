import MySQLdb
import json


db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID FROM patent_info" 
cursor.execute(query)
output = cursor.fetchall()

scan = 0
referenced_patents = []
for i in output:
  #print i 
  if scan%100 == 0:
    print scan
  query = "SELECT ref FROM patent_info WHERE ID='{0}'".format(i[0])
  cursor.execute(query)
  ref = json.loads(cursor.fetchall()[0][0])
  if ref != "NULL":
    #print ref
    for j in ref:
      query = "SELECT EXISTS(SELECT * FROM patent_info WHERE ID='0{0}')".format(j.encode('ascii','ignore'))
      cursor.execute(query)
      exists = cursor.fetchall()
      if exists[0][0] == "1":
        #SELECT ref_by
        #if NULL create [] else loads and append then dumps
        print i
        print "  0{0}".format(j)
  scan = scan + 1
    #db.commit()


db.close()


