
"""====================================================
@Author: Sangeeta
@Uses: This file will be used to parse revision ids to extract data
@Uses: This is a test command
========================================================"""

import re
import MySQLdb
import urllib2
#import urllib
import python_utility as pu

project   = "chromium"
project_basic_url = "http://src.chromium.org"

"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
file_path="E:\\Sangeeta\\Research\\regression1\\web_page_data.txt"
lower_limit = 0
upper_limit = 100000
"""
port=3306
user="root"
password="1234"
database="regression1"
file_path="F:\\web_page_data.txt"
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
for temp in table_data:
    bugid = temp[0]
    revid = temp[1]
   
    print  "revid=", revid 
    #pytrevid = 2270
        
    fetch_url = "http://src.chromium.org/viewvc/chrome?revision="+(str)(revid)+"&view=revision"

    print "fetch url = ",fetch_url
    
    web_page_info = urllib2.urlopen(fetch_url)
    web_page_data = web_page_info.read()
    flag = 0
    flag= pu.check_for_show_all(web_page_data, revid)
   
    #print "flag=", flag
    #"""
    if flag==1:
        #fetch_url = "http://src.chromium.org/viewvc/chrome?limit_changes=0&view=revision&revision="+(str)(revid)
        #web_page_info = urllib2.urlopen(fetch_url)
        #web_page_data = web_page_info.read()
        file = open(file_path,'a')   
        file.write("Revid = ")
        file.write((str)(revid))
        file.write("\n")
        file.close()
    
    #print "New Web Page Data = ", web_page_data
    rev_log_message, rev_comitter = pu.get_log_message_and_comitter(web_page_data)
    rev_log_message =  pu.remove_html_tags(rev_log_message)
    rev_log_message = pu.remove_quote_new_line (rev_log_message)
    rev_day, rev_month, rev_weakday,rev_hour =  pu.get_time(web_page_data) #Time metric

    rev_is_bug_fix = pu.contains_bug_fix(web_page_data)
    changed_path_files =  pu.get_changed_files(web_page_data)
    test_file_count  = pu.test_file_count(web_page_data)
    
    #Size Metric
    lines_added,lines_deleted, lines_changed, chunks_added, chunks_deleted, chunks_changed= pu.get_lines_added_count(web_page_data, fetch_url, project_basic_url)
    churn  =  lines_added + lines_deleted + lines_changed
    
    #Files Metric
    changed_path_count= pu.no_of_files_modified(web_page_data)
    max_devs_in_file, max_change_count  = pu.get_max_no_of_devs_and_change_count(web_page_data,project)
    
    #java_file, cpp_files, other_file = pu.get_types_files_modified

    #print "chucks added=", chunks_added    
    insert_str = "insert into "+insert_rev_table+" values("+(str)(bugid)+","+(str)(revid)+",'"+rev_log_message+"',"+(str)(rev_is_bug_fix)+","+(str)(changed_path_count)+","\
    +(str)(lines_added)+","+  (str)(lines_deleted)+","+(str)(lines_changed)+","+(str)(chunks_added)+","+(str)(chunks_deleted)+","+(str)(chunks_changed)+","\
    +(str)(churn)+",'"+changed_path_files+"',"+(str)(test_file_count)+","+(str)(rev_day)+","+(str)(rev_month)+","+(str)(rev_weakday)+","+(str)(rev_hour)+","\
    +(str)(max_devs_in_file)+","+(str)(max_change_count)+")"
    
    #print "insert str=",insert_str
    
    insert_cursor.execute(insert_str)
    
    db1.commit()    
