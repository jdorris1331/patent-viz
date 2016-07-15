import MySQLdb
import json
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np


db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID FROM patent_info" 
cursor.execute(query)
output = cursor.fetchall()

scan = 0
referenced_patents = []
for i in output:
  if scan%100 == 0:
    print scan
  query = "SELECT ref FROM patent_info WHERE ID='{0}'".format(i[0])
  cursor.execute(query)
  ref = json.loads(cursor.fetchall()[0][0])
  if ref != "NULL":
    for j in ref:
      try:
        referenced_patents+= [int(j.encode('ascii','ignore'))]
      except:
        pass
  scan = scan + 1

rp = [s for s in referenced_patents if s<9279926]
plt.hist(rp,30)
plt.show()
db.close()


