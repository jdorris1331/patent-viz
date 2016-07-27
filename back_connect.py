import MySQLdb
import json


db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

query = "SELECT ID FROM patent_info limit 100000 offset 6000" 
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
      try:
        if int(j) < int(i[0]):
          query = "SELECT EXISTS(SELECT * FROM patent_info WHERE ID='0{0}')".format(j.encode('ascii','ignore'))
          #print query
          cursor.execute(query)
          exists = cursor.fetchall()
          #print exists
          #print exists[0][0]
          if exists[0][0] == 1:
            query = "SELECT ref_by FROM patent_info WHERE ID='0{0}'".format(j.encode('ascii','ignore'))
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows[0][0] == None:
              ref_by = [i[0]]
              query = "UPDATE patent_info SET ref_by = '{0}' WHERE ID='0{1}'".format(json.dumps(ref_by),j.encode('ascii','ignore'))
              cursor.execute(query)
              rows = cursor.fetchall()
              print query
              db.commit()
            else:
              ref_by = json.loads(rows[0][0])
              if i[0] not in ref_by:
                ref_by += [i[0]]
              query = "UPDATE patent_info SET ref_by = '{0}' WHERE ID='0{1}'".format(json.dumps(ref_by),j.encode('ascii','ignore'))
              print query
              cursor.execute(query)
              db.commit()
            print i[0]
            print "  0{0}".format(j)
      except:
        pass
  scan = scan + 1


db.close()


