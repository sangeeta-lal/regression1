

"""
@Aurhor: Sangeeta
@Aim: This script will be used "combine" all the features score form bug report similiarity and individual risk score of revision ids
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

revid_str = "select distinct revid from " + revid_feature_table
select_cursor.execute(revid_str)
revid_data = select_cursor.fetchall()


for rev in revid_data:
    feature_str = "select rev_log_message, is_bug_fix, changed_path_count, lines_added, lines_deleted, lines_changed, chunks_added, chunks_deleted, chunks_modified, churn, changed_files, test_file_count, \
                   day, month, weakday, hour, max_dev_in_file, max_change_count, avg_rev_comitter_expr  from " +  revid_feature_table+ " where revid = "+ (str)(rev[0])
    
    #print feature_str 
    select_cursor.execute(feature_str)
    feature_data =  select_cursor.fetchall()
    for f in feature_data:
        rev_log_message = (str)( f[0])
        is_bug_fix  = (str)(f[1])
        changed_path_count =     (str)( f[2])
        lines_added  =    (str)( f[3])
        lines_deleted =    (str)(f[4])
        lines_changed =    (str)(f[5])
        chunks_added =     (str)(f[6])
        chunks_deleted =   (str)( f[7])
        chunks_modified =  (str)( f[8])
        churn =           (str)( f[9])
        changed_files =  (str)(f[10])
        test_file_count =  (str)(f[11])
        day =  (str)(f[12])
        month =  (str)(f[13])
        weakday  =  (str)(f[14])
        hour =  (str)(f[15])
        max_dev_in_file =  (str)(f[16] )
        max_change_count =  (str)(f[17])
        avg_rev_comitter_expr =  (str)(f[18])
    
        update_str = "update " +score_table    +" set  rev_log_message='"+ (str)(rev_log_message) +"', is_bug_fix="+ (str)(is_bug_fix)+""\
        +",changed_path_count=" +(str)(changed_path_count)+ ", lines_added="+(str)(lines_added)+\
        ",lines_deleted="+(str)(lines_deleted)+" , lines_changed="+(str)( lines_changed)+" ,chunks_added="+ (str)( chunks_added)+ ", chunks_deleted="+(str)( chunks_deleted) +\
        " ,chunks_modified="+\
        (str)( chunks_modified)+ ",churn="+(str)( churn)+ " ,changed_files='"+(str)( changed_files)+"' ,test_file_count="+ (str)(test_file_count)+ " ,day="+ (str)(day)+ ", month="+(str)( month)+\
        ", weakday="+(str)( weakday)+ ", hour="+ (str)(hour)+" ,max_dev_in_file="+ (str)(max_dev_in_file)+ ",max_change_count="+(str)( max_change_count)+" ,avg_rev_comitter_expr="+\
        (str)(avg_rev_comitter_expr ) + " where revid = "+ (str)(rev[0])
        
        #print "update str=", update_str
        update_cursor.execute(update_str)
  
        
    
db1.commit()   