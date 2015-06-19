

"""
@This file is used to create graphs for charecterization study
@Following are the graphs

1. Graph 1:  How many of them are bug fixing
2. Graph 2: Developer experience

"""

import re
import MySQLdb
import urllib2
from pylab import *
from matplotlib import pyplot as plt
from matplotlib import *
import numpy

project   = "chromium"

"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
revid_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
training_revid_table =project +"_bugid_previous_30day_revids"
"""
port=3306
user="root"
password="1234"
database="regression1"
revid_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
training_revid_table =project +"_bugid_previous_30day_revids"
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
str_g4  = "select changed_path_count from " + revid_table + " where revid in (select revid from "+ bugid_revid_table +" )"
print "str g3=", str_g4
select_cursor.execute(str_g4)
g4_data = select_cursor.fetchall()
no_of_files = list()


for file_count  in g4_data:
    no_of_files.append(file_count)

boxes = []
boxes.append(no_of_files)
plt.boxplot(boxes, 0, 'gD')
plt.ylim([0,200])
plt.ylabel("Number of Files Changed")
plt.show()

#Graph5 : PLot number of files with experience
str_g5  = "select  changed_path_count, avg_rev_comitter_expr from " + revid_table + " where revid in (select revid from "+ bugid_revid_table +" )  order by changed_path_count desc"
print "g5", str_g5
print "str g5=", str_g5
select_cursor.execute(str_g5)
g5_data = select_cursor.fetchall()
no_of_files = list()
avg_rev_comitter_expr = list()

for d  in g5_data:
    file_count = d[0]
    comitter_expr = d[1]
    no_of_files.append(file_count)
    avg_rev_comitter_expr.append(comitter_expr)

plt.plot(no_of_files, avg_rev_comitter_expr, 'ro')
plt.xlabel("Number of Files Changed")
plt.ylabel("Average Committer Experience")
plt.xlim([0,100])
plt.show()


#Graph 6:  Plot number of lines added, deletd, and mmodified
str_g6  = "select  lines_added, lines_deleted, lines_changed from " + revid_table + " where revid in (select revid from "+ bugid_revid_table +" )  order by changed_path_count desc"
print "g6", str_g6

select_cursor.execute(str_g6)
g6_data = select_cursor.fetchall()
lines_added = list()
lines_deleted = list()
lines_changed = list()
num= list()
count = 0
for d  in g6_data:
    temp_lines_added = d[0]
    temp_lines_deleted = d[1]
    temp_lines_changed = d[2]
    lines_added.append(temp_lines_added)
    lines_deleted.append(temp_lines_deleted)
    lines_changed.append(temp_lines_changed)
    count = count +1
    num.append(count)

plt.plot(num, lines_added,label = 'Lines Added')
plt.plot(num, lines_deleted, label =  'Lines Deleted')
plt.plot(num, lines_changed, label = 'Lines Changed')
plt.ylabel('Count')


plt.show()


#Graph 7:  Plot number of chunks added, chunks deletd, and  chunksmmodified
str_g7  = "select  chunks_added, chunks_deleted, chunks_modified from " + revid_table + " where revid in (select revid from "+ bugid_revid_table +" )  order by changed_path_count desc"
print "g7", str_g7

select_cursor.execute(str_g7)
g7_data = select_cursor.fetchall()
chunks_added = list()
chunks_deleted = list()
chunks_modified = list()
num= list()
count = 0
for d  in g7_data:
    temp_chunks_added = d[0]
    temp_chunks_deleted = d[1]
    temp_chunks_modified = d[2]
    chunks_added.append(temp_chunks_added)
    chunks_deleted.append(temp_chunks_deleted)
    chunks_modified.append(temp_chunks_modified)
    count = count +1
    num.append(count)

plt.plot(num, chunks_added,label = 'chunks Added')
plt.plot(num, chunks_deleted, label =  'chunks Deleted')
plt.plot(num, chunks_modified, label = 'chunks Changed')
plt.ylabel('Count')
plt.show()


#Graph 8:  Number of commits before 10, 20, 30 days of regression bug report
day_10_before = list()
day_20_before = list()
day_30_before = list()

str_10  = "select  bugid, count(*) from " + training_revid_table + " where  bugid_revid_day_diff<=10.0 group by bugid"
print "10 days = ", str_10
select_cursor.execute(str_10)
data_10 = select_cursor.fetchall()

for d in data_10:
    count = d[1]
    day_10_before.append(count)

str_20  = "select  bugid, count(*) from " + training_revid_table + " where  bugid_revid_day_diff<=20.0  group by bugid"
print "20 days = ", str_20
select_cursor.execute(str_20)

data_20 = select_cursor.fetchall()
for d in data_20:
    count = d[1]
    day_20_before.append(count)
    

str_30  = "select  bugid, count(*) from " + training_revid_table + " where  bugid_revid_day_diff<=30.0  group by bugid"
print "day 30=", str_30
select_cursor.execute(str_30)
data_30 = select_cursor.fetchall()
for d in data_30:
    count = d[1]
    day_30_before.append(count)

boxes=[]
boxes.append(day_10_before)
boxes.append(day_20_before)
boxes.append(day_30_before)

plt.boxplot(boxes, 0, 'gD')
plt.ylabel("Commit Count in SVN")
plt.xlabel("Before 10 Days", "Before 20 Days", "Before 30 Days")
plt.show()


"""
#calculating trend line
z =  numpy.polyfit(no_of_files, avg_rev_comitter_expr,1)
p=numpy.ploy1d(z)
plt.plot(no_of_files,p(no_of_files), "r-")
print   "y=%,6fx+(%.6f)"%(z[0], z[1])
"""
plt.show()