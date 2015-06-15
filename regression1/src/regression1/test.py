
"""
This is the file used to test can multithreading work
"""

import MySQLdb
project = "chromium"
port=3306
user="root"
password="1234"
database="regression1"
lower_limit = 0
upper_limit = 100000
#"""
table =project+ "_bugid_previous_30day_revids"
insert_rev_table= project+"_revids_feature"

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
insert_cursor =  db1.cursor()

#count = 0 
str1=  "select bugid, revid from "+ table + " limit  "+(str)(lower_limit)+","+ (str)(upper_limit)

select_cursor.execute(str1)
table_data = select_cursor.fetchall()

print " table data = ", len(table_data)

print table_data[10:20]

"""
i=0
while i <= len(table_data):
    print i
    print "i=", table_data[i][1]
   # print "i+1=", table_data[i+1]
    i=i+1
  """  