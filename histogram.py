import MySQLdb
import json
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import math

def year(x):
  x = math.log(x,10)              
  ret = -0.411218030494638* pow(x,6) + 10.895688032037000*pow(x,5) - 114.625576892541000*pow(x,4) + 610.520817699953000*pow(x,3) - 1724.229196863340000*pow(x,2) + 2450.449447910530000*x + 423.574791551009000
  return ret

db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID FROM patent_info" 
cursor.execute(query)
output = cursor.fetchall()

scan = 0
referenced_patents = []
for i in output:
  try:
    y1 = year(float(i[0]))
    if scan%100 == 0:
      print scan
    query = "SELECT ref FROM patent_info WHERE ID='{0}'".format(i[0])
    cursor.execute(query)
    ref = json.loads(cursor.fetchall()[0][0])
    if ref != "NULL":
      for j in ref:
        try:
          if int(j.encode('ascii','ignore')) < int(i[0]):
            y2 = year(float(j.encode('ascii','ignore')))
            referenced_patents+= [y1-y2] #[int(i[0].encode('ascii','ignore'))-int(j.encode('ascii','ignore'))]
        except:
          pass
  except:
    pass
  scan = scan + 1

#rp = [s for s in referenced_patents if s<9279926]
plt.hist(referenced_patents,100)
plt.show()
db.close()


