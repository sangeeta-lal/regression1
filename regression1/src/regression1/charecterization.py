

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

#"""
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

plt.rcParams.update({'font.size': 20})
x = [1,2]
y = [BFR, NBFR]
plt.bar(x, y,color = 'b',  align='center', width=0.20)
plt.xticks([1, 2], ['Bug Fixing', 'Non Bug Fixing'])
#plt.title('Distribution of Regression Causing Commits: Bug Fixing Vs. Non Bug Fixing')
plt.ylabel('Percentage')
plt.xlabel('')
plt.grid(True)
plt.show()

print "bug fixing revs = ", bug_fixing_revids

#Graph 2 : Identifying experince of developers with resoec to regression cauing commits
str_g2  = "select avg_rev_comitter_expr from " + revid_table + " where revid in (select revid from "+ bugid_revid_table +" )"
print "str g2=", str_g2
select_cursor.execute(str_g2)
g2_data = select_cursor.fetchall()
dev_exp = list()
dev_list=list()
count=0
for avg_exp  in g2_data:
    print "avg expr = ", avg_exp
    dev_exp.append(avg_exp)
    count=count+1
    dev_list.append(count)

plt.xlabel('Developers')
plt.ylabel('Average Comitter Experience (%)')
plt.scatter(dev_list, dev_exp,color='green')
plt.xlim([0,count+10])
plt.ylim([0,110])
#plt.savefig(file_path+"fun-scatter.eps")
plt.show()


# Graph3 =======Box plot==of the above developer average experience====#
boxes=[]
boxes.append(dev_exp)

plt.boxplot(boxes, 0, 'gD')
plt.ylabel("Average Comitter Experience (%)")
plt.show()


#Graph4 : Identifying number of files of developers with resoec to regression cauing commits
str_g3  = "select changed_path_count from " + revid_table + " where revid in (select revid from "+ bugid_revid_table +" )"
print "str g3=", str_g3
select_cursor.execute(str_g3)
g3_data = select_cursor.fetchall()
no_of_files = list()


for file_count  in g3_data:
    no_of_files.append(file_count)

boxes = []
boxes.append(no_of_files)
plt.boxplot(boxes, 0, 'gD')
plt.ylim([0,200])
plt.ylabel("Number of Files Changed")
plt.show()


plt.show()
