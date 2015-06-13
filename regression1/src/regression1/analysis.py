

"""
@Author: Sangeeta
@Aim: This python file will help me in analyzing the output of the propsed approach
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
score_table= project+"_score_table"
analysis_table1 = "analysis_table1"
"""
port=3306
user="root"
password="1234"
database="regression1"
revid_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
score_table= project+"_score_table"
analysis_table1 = "analysis_table1"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
insert_cursor = db1.cursor()

str1  = "select bugid, revid from "+ bugid_revid_table
select_cursor.execute(str1)
temp_data =  select_cursor.fetchall()

for t in temp_data:
    bugid  = t[0]
    reg_causing_revid = t[1]
    print " bug=", bugid, "  rev=", reg_causing_revid
    
    rank = 0
    str2 = "select   combined_score, revid from "+ score_table+"  where  bugid="+ (str) ( bugid)+ " order by combined_score desc"  
    print "str2=", str2
    
    select_cursor.execute(str2)
    temp2_data = select_cursor.fetchall()
    
    for t2 in temp2_data:
        rev_total_sim_score = t2[0] 
        temp_revid = t2[1]
        rank  =  rank+1
        
        if temp_revid==reg_causing_revid:
            
            break        
    
    insert_str = " insert into "+ analysis_table1 +" values ("+ (str)(bugid)+","+(str)(reg_causing_revid)+","+(str)(rev_total_sim_score)+ ", "+  (str)(rank)+")"
    insert_cursor.execute(insert_str)   
 
db1.commit()   