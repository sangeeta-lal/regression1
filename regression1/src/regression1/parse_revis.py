
"""====================================================
@Author: Sangeeta
@Uses: This file will be used to parse revision ids to extract data
@Uses: This is a test command
========================================================"""

import re
import MySQLdb
import urllib2
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
    rev_log_message = pu.get_log_message(web_page_data)
    rev_log_message =  pu.remove_html_tags(rev_log_message)
    rev_log_message = pu.remove_quote (rev_log_message)
    rev_hour, rev_weakday =  pu.get_time(web_page_data)
    #print "rev hour = ", rev_hour, " rev_weakday=", rev_weakday
    rev_is_bug_fix = pu.contains_bug_fix(web_page_data)
    changed_path_count= pu.no_of_files_modified(web_page_data)
    change_path_file =  pu.get_changed_files(web_page_data)
    test_file_count  = pu.test_file_count(web_page_data)
    
    lines_added,chunks_added = pu.get_lines_added_count(web_page_data, fetch_url, project_basic_url)
     
    lines_deleted =  pu.get_lines_deleted_count(web_page_data, fetch_url, project_basic_url) 
    lines_changed =  pu.get_lines_changed_count(web_page_data, fetch_url, project_basic_url) 
    #print "lines addes = ",lines_added ,  "  lines deleted = ", lines_deleted
    #count =  count + rev_is_bug_fix
    #print "rev is bug fix=", rev_is_bug_fix, "count = ",count," \n ----------------------------\n"
    print "chucks added=", chunks_added
    
    insert_str = "insert into "+insert_rev_table+" values("+(str)(bugid)+","+(str)(revid)+",'"+rev_log_message+"',"+(str)(rev_is_bug_fix)+","+(str)(changed_path_count)+","+(str)(test_file_count)+","+(str)(lines_added)+","+\
    (str)(lines_changed)+","+(str)(lines_deleted)+")"
    print "insert str=",insert_str
    #insert_cursor.execute(insert_str)
    
    db1.commit()    
