

"""
@This file is used to create graphs for charecterization study
@Following are the graphs

1. Graph 1:  How many of them are bug fixing
2. Graph 2: Developer experience

"""

import re
import MySQLdb
import urllib2
import python_utility as pu
from pylab import *
from matplotlib import pyplot as plt
from matplotlib import *


project   = "chromium"

"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
revid_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
"""
port=3306
user="root"
password="1234"
database="regression1"
revid_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()

#Basic
str =  "select count(*) from  "+ bugid_revid_table
select_cursor.execute(str)
table_data = select_cursor.fetchall()
total_bugs =  table_data[0][0]
print "Total Bugs=", total_bugs

#Graph 1: Identifying how many are bug fixing
str_g1  = "select count(*) from " + revid_table+ " where  is_bug_fix = 1 and revid in (select revid from "+ bugid_revid_table +" )"
print "str g1 = ", str_g1
select_cursor.execute(str_g1)
bug_fixing_revids = select_cursor.fetchall()[0][0]

non_bug_fixing_revids = total_bugs - bug_fixing_revids

BFR = (bug_fixing_revids *100)/total_bugs
NBFR = (non_bug_fixing_revids *100)/total_bugs
style.use('ggplot')
x = [1,2]
y = [BFR, NBFR]
plt.bar(x, y,color = 'g',  align='center', width=0.20)
plt.xticks([1, 2], ['Bug Fixing', 'Non Bug Fixing'])
plt.title('Distribution of Regression Causing Commits: Bug Fixing Vs. Non Bug Fixing')
plt.ylabel('Percentage')
plt.xlabel('')

plt.show()



print "bug fixing revs = ", bug_fixing_revids
