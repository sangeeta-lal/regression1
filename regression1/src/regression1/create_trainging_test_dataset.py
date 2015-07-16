


"""================================================================================
@Author: Sangeeta
@Aim: This file is used to  create training and test data set for regression bugs

==================================================================================="""

import MySQLdb
import numpy as np

project = "chromium"

"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
main_table = project +"_bugid_reg_revids"
train_table = project +"_train_bugid_reg_revids"
test_table = project+"_test_bugid_reg_revids"
"""
port=3306
user="root"
password="1234"
database="regression1"
main_table = project +"_bugid_reg_revids"
train_table = project +"_train_bug_reg_revids"
test_table = project+"_test_bug_reg_revids"
#"""


db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
insert_cursor=  db1.cursor()

total_bugs = 0
total_str = "select count(*) from "+ main_table
select_cursor.execute(total_str)
data =  select_cursor.fetchall()
total_bug_count =  data[0][0]


print "total bugs=", total_bug_count
train_count =  (total_bug_count*70)/100
test_count  = total_bug_count-train_count

print "train count =", train_count , " test count=", test_count
random_seed_val=0
np.random.seed(random_seed_val)
indices = np.random.permutation(total_bug_count)



train_indices = list()
count = 0
for index  in indices:
    count = count+1
    if count<=train_count:
        train_indices.append(index)
           

train_bug_reg_rev = list()
test_bug_reg_rev = list()

str_bug_reg_revid = " select bugid, revid from "+ main_table
select_cursor.execute(str_bug_reg_revid)
bug_reg_revid_data =  select_cursor.fetchall()
    
count = 0
for data in bug_reg_revid_data:
   # print "count = ", count
   
    if count  in train_indices: 
       train_bug_reg_rev.append(data)
        
    else:        
        test_bug_reg_rev.append(data)
    count = count+1
    
#print  len(train_bug_reg_rev),"  " , len(test_bug_reg_rev)  
  
#training table       
for data in train_bug_reg_rev:
    bugid =  data[0]
    revid =  data[1]
    
    insert_str = " insert into " +  train_table+ "  values ("+ (str)(bugid) +","+ (str)(revid)+")"
    insert_cursor.execute(insert_str)
    
#test table
for data in test_bug_reg_rev:
    bugid =  data[0]
    revid =  data[1]
    
    insert_str = " insert into " +  test_table+ "  values ("+(str)( bugid) +","+ (str)(revid)+")"
    insert_cursor.execute(insert_str)  

print " created.."    
db1.commit()          
        



