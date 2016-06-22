import MySQLdb
import json
import xml.etree.ElementTree as ET

db = MySQLdb.connect('localhost','joe','password','patents');

cursor = db.cursor()

for i in range(0,999):
  print i
  file = "bulk_data/xx{0:04d}".format(i)
  tree = ET.parse(file)
  root = tree.getroot()

  #cursor.execute("SELECT * FROM patent_info")


  #ID = root[0][0][0][1].text
  if root.find('us-bibliographic-data-grant') is not None:
    bib = root.find('us-bibliographic-data-grant')
  else:
    continue
  
  ID = bib.find('publication-reference').find('document-id').find('doc-number').text
  # some dont have us-bibliographic-data-grant

  #title = root[0][6].text


  title = "NULL"
  if bib.find('invention-title') is not None:
    if bib.find('invention-title').text is not None:
      title = bib.find('invention-title').text.encode('ascii','ignore')

  title = title.replace("'","")

  temp_date = root.attrib['date-publ']
  date = temp_date[0:4] + "-" + temp_date[4:6] + "-" + temp_date[6:8]
  inventor = "NULL"
  inventor = bib.find('us-parties').find('inventors').find('inventor').find('addressbook').find('first-name').text + " " + root.find('us-bibliographic-data-grant').find('us-parties').find('inventors').find('inventor').find('addressbook').find('last-name').text
  inventor = inventor.replace("'","").encode('ascii','ignore')

  assignee = "NULL"
  if bib.find('assignees') is not None:
    if bib.find('assignees').find('assignee').find('addressbook').find('orgname') is not None:
      assignee = bib.find('assignees').find('assignee').find('addressbook').find('orgname').text
    elif bib.find('assignees').find('assignee').find('addressbook').find('last-name') is not None:
      assignee = bib.find('assignees').find('assignee').find('addressbook').find('first-name').text + " " + bib.find('assignees').find('assignee').find('addressbook').find('last-name').text
  assignee = assignee.replace("'","").encode('ascii','ignore')
  
  ref = "NULL"
  #for j in range(0,len(root.find('us-bibliographic-data-grant').find('us-references-cited'))):
  #  ref += [root.find('us-bibliographic-data-grant').find('us-references-cited')[j].find('patcit').find('document-id').find('doc-number').text]  
  ref_by= "NULL"

  query = "INSERT INTO patent_test VALUES ( '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6} )".format(ID,title,date,inventor,assignee,json.dumps(ref),ref_by) 
  print query

  cursor.execute(query)
  db.commit()


  #for j in range(0,len(root.find('claims'))):
    #root.find('claims')[j].find('claim').find('claim-text').text

  #abstract 

  #description

  #images

db.close()

#INSERT INTO patent_test VALUES ('7956546', 'Modular LED light bulb', '2011-06-07', 'Ghulam Hasnain', 'Bridgelux, Inc.', '[6127783, 6596977, 7215086, 7458934, 7479662, 7524097, 7641364, 20040066142, 20040222516, 20060097245, 20060227558, 20070109782]','[8306639, 8350485, 8421376, 8422889, 8430402, 8531137, 8708525]');

#patent_data = ID, claims, abstract, description, images
#  data = cursor.fetchone()



#json.loads(data[5])
