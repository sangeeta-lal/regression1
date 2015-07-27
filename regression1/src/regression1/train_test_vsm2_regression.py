

"""
@Sangeeta: This file is used to compute the similarity between regression bug report and revision causing commit
Link :
http://blog.christianperone.com/?p=2497
http://aimotion.blogspot.in/2011/12/machine-learning-with-python-meeting-tf.html 
"""

"""
@To be done
1. split on spaces
2. Spilt on _
3. Remove hexadecimal charecters
"""

import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import python_utility as pu

project   = "chromium"

#"""
model =  "VCE"
w1=w2=w3=w4=1.0
days = 30
#"""

"""
model =  "VCB"
w1=w2=w3=w4=
days = 30
#"""

#"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
bug_report_feature_table = project + "_bug_report_features"
bugid_previous_30_days_revids_table = project +"_bugid_previous_30day_revids"
revid_feature_table = project+"_revids_feature"
train_bugid_revid_table = project+"_train_bugid_reg_revids"
test_bugid_revid_table = project+"_test_bugid_reg_revids"
#bug_report_feature_table             = "temp"  + "_bug_report_features"
#bugid_previous_30_days_revids_table  = "temp"  +"_30_day"
#revid_feature_table                  = "temp"  +"_revid_feature"
#train_bugid_revid_table              = "temp"  
learning_table = project +"_"+model+"_weight_learning"
result_table_all="result_table_all"
"""
port=3306
user="root"
password="1234"
database="regression1"
bug_report_feature_table = project + "_bug_report_features"
bugid_previous_30_days_revids_table = project +"_bugid_previous_30day_revids"
revid_feature_table = project+"_revids_feature"
train_bugid_revid_table = project+"_train_bugid_reg_revids"
test_bugid_revid_table = project+"_test_bugid_reg_revids"
learning_table = project +"_"+model+"weight_learning"
result_table_all="result_table_all"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
insert_cursor = db1.cursor()

precision_percentage = 0
threshold = 50
total_bugs = 0
total_revids_found = 0
  
  
# This function used to extract the features of bug id 
def get_cleaned_bug_feature_info(bugid):
    str_bug_info  = "select title, description, cr, area from  "+bug_report_feature_table+ " where bugid="+(str)(bugid)
    print "bugid=", bugid #, "  total bugs=", total_bugs,  "  found=", total_revids_found
    select_cursor.execute(str_bug_info)
    bug_feature_info  =  select_cursor.fetchall()
    bug_title  =  bug_feature_info[0][0]
    bug_desc   =  bug_feature_info[0][1]
    bug_cr     =  bug_feature_info[0][2]
    bug_area   =  bug_feature_info[0][3]
    
    bug_cr_and_area =  bug_cr+ " "+ bug_area
    
    #=============@clean====================#
    
    bug_title  = pu.remove_operator_camel_stem(bug_title)
    #print " bug desc before= ", bug_desc
    bug_desc   = pu.remove_operator_camel_stem(bug_desc)
    #print "bug desc after====", bug_desc
    #print "******************************"
    bug_cr_and_area = pu.remove_operator_camel_stem(bug_cr_and_area)
                       
    
    #============@Make List==================#
    title_rev_log =  list()
    desc_rev_log = list()
    cr_area_top_level=list()
    title_file_name = list()
    
    title_rev_log.append(bug_title)     
    desc_rev_log.append(bug_desc)
    cr_area_top_level.append(bug_cr_and_area)
    title_file_name.append(bug_title)
    
    return title_rev_log, desc_rev_log, cr_area_top_level, title_file_name 

#===@This will extract the information about  revision ======#           
def get_cleaned_rev_info(bugid,title_rev_log,  desc_rev_log, cr_area_top_level,  title_file_name ):
    str_revs =   "select revid, reg_causing from "+ bugid_previous_30_days_revids_table +"  where  bugid="+(str)(bugid)
    #print "str revs=", str_revs
    candidate_revid_list = list()
    select_cursor.execute(str_revs)
    temp_revs = select_cursor.fetchall()
    #print  "total revids = ", len(temp_revs)
    #break
    reg_causing_revid = 0
    for r in temp_revs:
        #print "r is =",r
        candidate_revid_list.append(r[0])  
        if r[1]==1:
            reg_causing_revid = r[0]              
          
    print "reg causing revdi = ", reg_causing_revid
    #Identify reg-causing revids and their log message
    reg_causing_revid_pos = 0
    count = 0
    for temp_rev in candidate_revid_list:            
        str_rev_info = "select  rev_log_message, changed_files from "+revid_feature_table+ " where revid="+(str)(temp_rev)
        #print "str=", str_rev_info
        select_cursor.execute(str_rev_info)
        rev_info  =  select_cursor.fetchall()
                            
        #print " rev info = ", rev_info
        rev_log_mess =  rev_info[0][0]
        changed_files_with_path=  rev_info[0][1]
        changed_files_arr=[]
        changed_files_arr = changed_files_with_path.split("\n")
        changed_file_names = ""
        top_level_names = ""
        i=0
        while i< len(changed_files_arr):
            dir_depth= len(changed_files_arr[i].split("/"))
            changed_file_names =changed_files_arr[i].split("/")[dir_depth-1].split(".")[0] +" "+changed_file_names
            top_level_names = changed_files_arr[i].split("/")[dir_depth-2] +" "+top_level_names
            i=i+1
            
            # print "revid=", temp_rev,  "log mess", rev_log_mess, "  files=", changed_files_with_path,  " fie name=", changed_file_names, " \n top level=", top_level_names      
        
        #=========@Clean==========#
        rev_log_mess          =  pu.remove_operator_camel_stem(rev_log_mess)
        changed_file_name     =  pu.remove_operator_camel_stem(changed_file_names)
        top_level_names       =  pu.remove_operator_camel_stem(top_level_names) 
        
                           
        title_rev_log.append(rev_log_mess)
        desc_rev_log.append(rev_log_mess)
        cr_area_top_level.append(top_level_names)
        title_file_name.append(changed_file_names)
        
        count= count + 1
        if temp_rev == reg_causing_revid:
             reg_causing_revid_pos = count


    return title_rev_log, desc_rev_log, cr_area_top_level, title_file_name,  reg_causing_revid_pos

  
#========================TRAINING PART==============================#
#===================================================================#        
def  training():
    w1=-0.1
    w2 =- 0.1
    w3 =-0.1
    w4=-0.1

    while w4<=0.9:
        w4=w4+0.1
        w3=-0.1
        while w3 <=0.9:
            w3=w3+0.1
            w2=-0.1
            while w2<=0.9:
                w2=w2+0.1
                w1=-0.1
                while w1<=0.9:
                    w1= w1+0.1
                    print w1, " ", w2, " ", w3," ", w4
                    if(w1+w2+w3+w4)==1.0:
                        print "yes"

                    
                        total_sim_reg_causing=0.0
                        total_bugs = 0
                        total_revids_found = 0
                    
                        str_bug = "select distinct bugid   from " + train_bugid_revid_table
                        select_cursor.execute(str_bug)
                        bug_data =  select_cursor.fetchall()
                        print "@debug: Total bugs=", len(bug_data)

                        for id in bug_data:
                            total_bugs =  total_bugs+1
                            bugid   = id[0]
                        
                            ##=== This will give me already clean features =========##
                            title_rev_log, desc_rev_log,  cr_area_top_level, title_file_name = get_cleaned_bug_feature_info(bugid)
                  
                        
                            title_rev_log, desc_rev_log, cr_area_top_level, title_file_name, reg_causing_revid_pos = get_cleaned_rev_info(bugid, title_rev_log, desc_rev_log, cr_area_top_level, title_file_name )
                            
                            title_rev_log_sim_matrix, desc_rev_log_sim_matrix, cr_area_top_level_sim_matrix, title_file_name_sim_matrix=pu.create_sim_matrix( title_rev_log, desc_rev_log, cr_area_top_level, title_file_name)
    
                            #Get this data for reg causing revid 
                            title_rev_log_sim       =  title_rev_log_sim_matrix[0][reg_causing_revid_pos]
                            desc_rev_log_sim        =  desc_rev_log_sim_matrix[0][reg_causing_revid_pos]
                            cr_area_top_level_sim   =  cr_area_top_level_sim_matrix[0][reg_causing_revid_pos]
                            title_file_name_sim     =  title_file_name_sim_matrix[0][reg_causing_revid_pos]
                        
                            #print "reg causing t-r",  title_rev_log_sim
                            #print "desc rev-log",     desc_rev_log_sim
                            #print "cr area",          cr_area_top_level_sim   
                            #print "titel file",       title_file_name_sim
    
                            total_sim_reg_causing =  w1*title_rev_log_sim + w2*desc_rev_log_sim + w3*cr_area_top_level_sim + w4*title_file_name_sim
                            #print sim_matrix
                            rank = pu.get_rank(title_rev_log_sim_matrix, desc_rev_log_sim_matrix, cr_area_top_level_sim_matrix,title_file_name_sim_matrix, threshold, total_sim_reg_causing,w1, w2, w3, w4)
                            if rank<=threshold:
                                total_revids_found = total_revids_found +1
                        
                            print " @debug total revids found=", total_revids_found
                            #break   

                        print "Total bug found=", total_bugs
                        print  "total revids =", total_revids_found
                        precision =  (total_revids_found*100)/total_bugs
                        print "precsion = ", precision
                      
                        insert_str =  "insert into "+learning_table+   " values ("+ (str)(w1)+","+ (str)(w2)+","+(str)(w3)+","+(str)(w4)+","+ model+","+(str)(threshold)\
                        +","+(str)(precision)+","+(str)(total_bugs)+","+(str)(total_revids_found)+ ")" 
        
                        #print "insert str=", insert_str
                        insert_cursor.execute(insert_str)
                        db1.commit()
       


#===========================@Testing Phase====================================#
#============================================================================#
def testing():
    w1=1.0
    w2=1.0
    w3=1.0
    w4=1.0
    
    total_sim_reg_causing=0.0
    total_testing_bugs = 0
    total_revids_found = 0
    str_bug = "select distinct bugid   from " + test_bugid_revid_table
    select_cursor.execute(str_bug)
    bug_data =  select_cursor.fetchall()
    print "@debug: Total bugs=", len(bug_data)

    for id in bug_data:
        total_testing_bugs =  total_testing_bugs+1
        bugid   = id[0]
         
        #***************** This will give me already clean features *****************#
        title_rev_log, desc_rev_log,  cr_area_top_level, title_file_name = get_cleaned_bug_feature_info(bugid)              
        title_rev_log, desc_rev_log, cr_area_top_level, title_file_name, reg_causing_revid_pos = get_cleaned_rev_info(bugid, title_rev_log, desc_rev_log, cr_area_top_level, title_file_name )                      
        title_rev_log_sim_matrix, desc_rev_log_sim_matrix, cr_area_top_level_sim_matrix, title_file_name_sim_matrix=pu.create_sim_matrix( title_rev_log, desc_rev_log, cr_area_top_level, title_file_name)
       
        #==============Get this data for reg causing revid==========================#
        title_rev_log_sim       =  title_rev_log_sim_matrix[0][reg_causing_revid_pos]
        desc_rev_log_sim        =  desc_rev_log_sim_matrix[0][reg_causing_revid_pos]
        cr_area_top_level_sim   =  cr_area_top_level_sim_matrix[0][reg_causing_revid_pos]
        title_file_name_sim     =  title_file_name_sim_matrix[0][reg_causing_revid_pos]
                  
        #print "reg causing t-r",  title_rev_log_sim
        #print "desc rev-log",     desc_rev_log_sim
        #print "cr area",          cr_area_top_level_sim   
        #print "titel file",       title_file_name_sim
    
        total_sim_reg_causing =  w1*title_rev_log_sim + w2*desc_rev_log_sim + w3*cr_area_top_level_sim + w4*title_file_name_sim
        #print sim_matrix
        rank = pu.get_rank(title_rev_log_sim_matrix, desc_rev_log_sim_matrix, cr_area_top_level_sim_matrix,title_file_name_sim_matrix, threshold, total_sim_reg_causing,w1, w2, w3, w4)
        if rank<=threshold:
            total_revids_found = total_revids_found +1
               
            print " @debug total revids found=", total_revids_found
               

    print "Total bug found=", total_testing_bugs
    print  "total revids =", total_revids_found
    precision =  (total_revids_found*100)/total_bugs
    print "precsion = ", precision
    
    insert_str =  "insert into "+result_table_all+   " values ('"+project+"','"+model+"',"+(str)(days)+","+ (str)(w1)+","+ (str)(w2)+","+(str)(w3)+","+(str)(w4)+","+(str)(threshold)\
                        +","+(str)(precision)+","+(str)(total_testing_bugs)+","+(str)(total_revids_found)+ ")" 
        
    #print "insert str=", insert_str
    insert_cursor.execute(insert_str)
    db1.commit()
    
    
#===========#
print " doing training.......... to stop training comment the training function....."
#training()

print " doing testing............ check the w1, w2, w3 and w4 weights............."
testing()                   

                    
    
                      
               
    
            

                    