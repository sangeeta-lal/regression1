

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

project   = "chromium"
model =  "VCB"

#"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
#bug_report_feature_table = project + "_bug_report_features"
#bugid_previous_30_days_revids_table = project +"_bugid_previous_30day_revids"
#revid_feature_table = project+"_revids_feature"
#train_bugid_revid_table = project+"_train_bugid_reg_revids"
#test_bugid_revid_table = project+"_test_bugid_reg_revids"

bug_report_feature_table             = "temp"  + "_bug_report_features"
bugid_previous_30_days_revids_table  = "temp"  +"_30_day"
revid_feature_table                  = "temp"  +"_revid_feature"
train_bugid_revid_table              = "temp"  
learning_table = project +"_"+model+"weight_learning"
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
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()

precision_percentage = 0
threshold = 50
total_bugs = 0
total_revids_found = 0


def get_rank(title_rev_log_sim_matrix, desc_rev_log_sim_matrix, cr_area_top_level_sim_matrix, title_file_name_sim_matrix, threshold, reg_causing_revid_sim, w1, w2, w3, w4):
    rank = 0
    #print  " get rank=", sim_matrix 
    
    #turn  = 1  # because on first position bug report-bug report similiarrity is store which is "1.0" and will always be greater than bug report-revision log similiarity
    matrix_len=  len(title_rev_log_sim_matrix[0]) 
    
    ##@Not starting from 1 at ist position we have bug report it self
    for i in range(1, matrix_len): 
        temp_title_rev_log_sim = title_rev_log_sim_matrix[0][i]
        temp_desc_rev_log_sim = desc_rev_log_sim_matrix[0][i]
        temp_cr_area_top_level_sim = cr_area_top_level_sim_matrix[0][i]
        temp_title_file_name_sim = title_file_name_sim_matrix[0][i]
        total_temp_sim =  w1*temp_title_rev_log_sim + w2*temp_desc_rev_log_sim+ w3*temp_cr_area_top_level_sim + w4*temp_title_file_name_sim
        
        if total_temp_sim > reg_causing_revid_sim:
            rank =  rank+1
        
    return rank
  
  
#========================TRAINING PART==============================#
#===================================================================#        
w1=-0.1
w2 =- 0.1
w3 =-0.1
w4=-0.1

while w1 <=0.9:
    w1=w1+0.1
    w2=-0.1
    while w2 <=0.9:
        w2=w2+0.1
        w3=-0.1
        while w3<=0.9:
            w3=w3+0.1
            w4=-0.1
            while w4<=0.9:
                w4= w4+0.1
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
                        title_rev_log =  list()
                        desc_rev_log = list()
                        cr_area_top_level=list()
                        title_file_name = list()
    
                        bugid   = id[0]
    
                        str_bug_info  = "select title, description, cr, area from  "+bug_report_feature_table+ " where bugid="+(str)(bugid)
                        print "bugid=", bugid, "  total bugs=", total_bugs,  "  found=", total_revids_found
                        #break
                        select_cursor.execute(str_bug_info)
                        bug_feature_info  =  select_cursor.fetchall()
    
                        bug_title  =  bug_feature_info[0][0]
                        bug_desc   =  bug_feature_info[0][1]
                        bug_cr     =  bug_feature_info[0][2]
                        bug_area   =  bug_feature_info[0][3]
    
                        bug_cr_and_area =  bug_cr+ " "+ bug_area
                        #bug_all_features =  bug_title+ " "+ bug_description+ " "+ bug_cr+" "+ bug_area
                        #bug_all_feature =  utill.clean(bug_all_features)
                        print " title", bug_title, "  dec=", bug_desc, "  cr=",bug_cr, " area=", bug_area
    
                        ## utf 8 encoding
                        #bug_title = bug_title.encode('utf8')   @Not working
                        title_rev_log.append(bug_title)     
                        desc_rev_log.append(bug_desc)
                        cr_area_top_level.append(bug_cr_and_area)
                        title_file_name.append(bug_title)
    
                        candidate_revid_list = list()   
    
                        str_revs =   "select revid, reg_causing from "+ bugid_previous_30_days_revids_table +"  where  bugid="+(str)(bugid)
                        #print "str revs=", str_revs
                        select_cursor.execute(str_revs)
                        temp_revs = select_cursor.fetchall()
                        print  "total revids = ", len(temp_revs)
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
                            #temp_rev=3017
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
            
                            print "revid=", temp_rev,  "log mess", rev_log_mess, "  files=", changed_files_with_path,  " fie name=", changed_file_names, " \n top level=", top_level_names
                        
                            
                            title_rev_log.append(rev_log_mess)
                            desc_rev_log.append(rev_log_mess)
                            cr_area_top_level.append(top_level_names)
                            title_file_name.append(changed_file_names)
        
                            count= count + 1
                            if temp_rev == reg_causing_revid:
                                reg_causing_revid_pos = count
                            print "pos = ", reg_causing_revid_pos
                            
                        #print "all docs=", all_docs , " pos=", reg_causing_revid_pos
                        tfidf_vectorizer = TfidfVectorizer(stop_words='english',decode_error='ignore')
                        title_rev_log_tfidf_matrix     = tfidf_vectorizer.fit_transform(title_rev_log)
                        desc_rev_log_tfidf_matrix      = tfidf_vectorizer.fit_transform(desc_rev_log)
                        cr_area_top_level_tfidf_matrix = tfidf_vectorizer.fit_transform(cr_area_top_level)
                        title_file_name_tfidf_matrix   = tfidf_vectorizer.fit_transform(title_file_name)
    
                        #print  "size=", title_rev_log_tfidf_matrix.shape,  desc_rev_log_tfidf_matrix.shape,  cr_area_top_level_tfidf_matrix.shape, title_file_name_tfidf_matrix.shape
                        
                        #print  "Title Rev Log=",  title_rev_log_tfidf_matrix
                        #print "Desc rev log = ",  desc_rev_log_tfidf_matrix
                        #print "cr area top level=", cr_area_top_level_tfidf_matrix
                        #print  "title file name=", title_file_name_tfidf_matrix
                        
    
                        title_rev_log_sim_matrix      = cosine_similarity(title_rev_log_tfidf_matrix[0:1], title_rev_log_tfidf_matrix)
                        desc_rev_log_sim_matrix       = cosine_similarity(desc_rev_log_tfidf_matrix[0:1], desc_rev_log_tfidf_matrix)
                        cr_area_top_level_sim_matrix  = cosine_similarity(cr_area_top_level_tfidf_matrix[0:1], cr_area_top_level_tfidf_matrix)
                        title_file_name_sim_matrix    = cosine_similarity( title_file_name_tfidf_matrix[0:1],  title_file_name_tfidf_matrix)
    
                        print "sim title-rev log", title_rev_log_sim_matrix    
                        print "desc rev log", desc_rev_log_sim_matrix      
                        print "cr area top", cr_area_top_level_sim_matrix 
                        print "title file name", title_file_name_sim_matrix 
    
                        
                        title_rev_log_sim       =  title_rev_log_sim_matrix[0][reg_causing_revid_pos]
                        desc_rev_log_sim        =  desc_rev_log_sim_matrix[0][reg_causing_revid_pos]
                        cr_area_top_level_sim   =  cr_area_top_level_sim_matrix[0][reg_causing_revid_pos]
                        title_file_name_sim     =  title_file_name_sim_matrix[0][reg_causing_revid_pos]
                        
                        print "reg causing t-r",  title_rev_log_sim
                        print "desc rev-log",     desc_rev_log_sim
                        print "cr area",          cr_area_top_level_sim   
                        print "titel file",       title_file_name_sim
    
                        total_sim_reg_causing =  w1*title_rev_log_sim + w2*desc_rev_log_sim + w3*cr_area_top_level_sim + w4*title_file_name_sim
                        #print sim_matrix
    
                        rank = get_rank(title_rev_log_sim_matrix, desc_rev_log_sim_matrix, cr_area_top_level_sim_matrix,title_file_name_sim_matrix, threshold, total_sim_reg_causing,w1, w2, w3, w4)
                        if rank<=threshold:
                            total_revids_found = total_revids_found +1
    

                        #break   

                        print "Total bug found=", total_bugs
                        print  "total revids =", total_revids_found
                        precision =  (total_revids_found*100)/total_bugs
                        print "precsion = ", precision
                         
                        insert_str =  "insert into "+learning_table+   " values ("+ (str)(w1)+","+ (str)(w2)+","+(str)(w3)+","+(str)(w4)+","+ model+","+(str)(threshold)\
                        +","+(str)(precision)+","+(str)(total_bugs)+","+(str)(total_revids_found)+")" 

                    