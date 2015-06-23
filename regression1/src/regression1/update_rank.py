

"""
@Author: Sangeeta
@Aim: This file will be used to compute the rank of the revision ids.
"""

import MySQLdb

project   = "chromium"

#"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
revid_feature_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
#score_table= project+"_score_table"
combined_score_table = project+"_combined_score_table"
"""
port=3306
user="root"
password="1234"
database="regression1"
revid_feature_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
#score_table= project+"_score_table"
combined_score_table = project+"_combined_score_table"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
update_cursor= db1.cursor()

######========== Now update Rank=======###   

select_str = " select bugid, revid  from "  +bugid_revid_table
select_cursor.execute(select_str)
temp_data = select_cursor.fetchall()
for t in temp_data:
    bugid  = t[0]
    reg_causing_revid = t[1]
    print " bug=", bugid, "  rev=", reg_causing_revid
    reg_causing = 0    
    rank = 0
    str2 = "select  combined_score,  revid  from "+ combined_score_table+"  where  bugid="\
    + (str) ( bugid)+ " order by combined_score desc"  
    #print "str2=", str2
    
    select_cursor.execute(str2)
    temp2_data = select_cursor.fetchall()
    
    for t2 in temp2_data:
        reg_causing_TF = 0
        rev_total_sim_score = t2[0] 
        temp_revid = t2[1]
        rank  =  rank+1
     
            
            
        update_str = " update "+ combined_score_table +" set  rank="+(str)(rank) +"  where bugid="+(str)(bugid)+ "  and revid="+ (str)(temp_revid)
        update_cursor.execute(update_str)   

db1.commit() 