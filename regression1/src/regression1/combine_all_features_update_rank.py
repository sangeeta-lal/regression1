

"""
@Aurhor: Sangeeta
@Aim: This script will be used "combine" all the features score form bug report similiarity and individual risk score of revision ids
"""
import MySQLdb

project   = "chromium"

lower_limit = 0
upper_limit = 5000
"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
revid_feature_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
score_table= project+"_score_table"

"""
port=3306
user="root"
password="1234"
database="regression1"
revid_feature_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
score_table= project+"_score_table"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
update_cursor  = db1.cursor()

revid_str = "select distinct revid from " + revid_feature_table  +"  limit "+ (str)(lower_limit)+","+ (str)(upper_limit)
select_cursor.execute(revid_str)
revid_data = select_cursor.fetchall()


count = 0
for rev in revid_data:
    feature_str = "select rev_log_message, is_bug_fix, changed_path_count, lines_added, lines_deleted, lines_changed, chunks_added, chunks_deleted, chunks_modified, churn, changed_files, test_file_count, \
                   day, month, weakday, hour, max_dev_in_file, max_change_count, avg_rev_comitter_expr  from " +  revid_feature_table+ " where revid = "+ (str)(rev[0]) 
    
    # print "revid=",rev[0] 
    print " lower limit = ", lower_limit, " upper limit = ", upper_limit, "  count = ", count
    select_cursor.execute(feature_str)
    feature_data =  select_cursor.fetchall()
    for f in feature_data:
        rev_log_message =  f[0]
        is_bug_fix  =       f[1]
        changed_path_count =    f[2]
        lines_added  =    f[3]
        lines_deleted =   f[4]
        lines_changed =   f[5]
        chunks_added =    f[6]
        chunks_deleted =   f[7]
        chunks_modified =  f[8]
        churn =            f[9]
        changed_files =  f[10]
        test_file_count =  f[11]
        day =  f[12]
        month =  f[13]
        weakday  =  f[14]
        hour =  f[15]
        max_dev_in_file =  f[16]
        max_change_count =  f[17]
        avg_rev_comitter_expr = f[18]
    
        update_str = "update " +score_table    +" set  rev_log_message='"+ (str)(rev_log_message) +"', is_bug_fix="+ (str)(is_bug_fix)+""\
        +",changed_path_count=" +(str)(changed_path_count)+ ", lines_added="+(str)(lines_added)+\
        ",lines_deleted="+(str)(lines_deleted)+" , lines_changed="+(str)( lines_changed)+" ,chunks_added="+ (str)( chunks_added)+ ", chunks_deleted="+(str)( chunks_deleted) +\
        " ,chunks_modified="+\
        (str)( chunks_modified)+ ",churn="+(str)( churn)+ " ,changed_files='"+(str)( changed_files)+"' ,test_file_count="+ (str)(test_file_count)+ " ,day="+ (str)(day)+ ", month="+(str)( month)+\
        ", weakday="+(str)( weakday)+ ", hour="+ (str)(hour)+" ,max_dev_in_file="+ (str)(max_dev_in_file)+ ",max_change_count="+(str)( max_change_count)+" ,avg_rev_comitter_expr="+\
        (str)(avg_rev_comitter_expr ) + " where revid = "+ (str)(rev[0])
        
        #print "update str=", update_str
        update_cursor.execute(update_str)
        count =  count +1
            
        db1.commit()

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
    str2 = "select  combined_score,  revid  from "+ score_table+"  where  bugid="\
    + (str) ( bugid)+ " order by combined_score desc"  
    print "str2=", str2
    
    select_cursor.execute(str2)
    temp2_data = select_cursor.fetchall()
    
    for t2 in temp2_data:
        reg_causing_TF = 0
        rev_total_sim_score = t2[0] 
        temp_revid = t2[1]
        rank  =  rank+1
        
        if  reg_causing_revid == temp_revid:
            reg_causing_TF = 1
            
            
        update_str = " update "+ score_table +" set  rank="+(str)(rank)+", reg_causing ="+ (str)(reg_causing_TF) +"  where bugid="+(str)(bugid)+ "  and revid="+ (str)(temp_revid)
        update_cursor.execute(update_str)   


db1.commit() 