

"""
@Sangeeta: This file is used to compute the similarity between regression bug report and revision causing commit

Link :
http://blog.christianperone.com/?p=2497

http://aimotion.blogspot.in/2011/12/machine-learning-with-python-meeting-tf.html
"""


import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

project   = "chromium"

#"""
port=3307
user="sangeetal"
password="sangeetal"
database="regression1"
bug_report_feature_table = project + "_bug_report_features"
bugid_previous_30_days_revids_table = project +"_bugid_previous_30day_revids"
revid_feature_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
#score_table= project+"_score_table"
combined_score_table = project+"_combined_score_table"
"""
port=3306
user="root"
password="1234"
database="regression1"
bug_report_feature_table = project + "_bug_report_features"
bugid_previous_30_days_revids_table = project +"_bugid_previous_30day_revids"
revid_feature_table = project+"_revids_feature"
bugid_revid_table = project+"_bugid_reg_revids"
#score_table= project+"_score_table"
combined_score_table = project+"_combined_score_table"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()

precision_percentage = 0
threshold = 100
total_bugs = 0
total_revids_found = 0


def get_rank(sim_matrix, threshold, reg_causing_revid_sim):
    rank = 0
    print  " get rank=", sim_matrix 
    
    turn  = 1  # becuase on first position bug report-bug report similiarrity is store which is "1.0" and will always be greater than bug report- revison log similiarity
    for sim_val in sim_matrix[0]:
       if turn!=1:       
           print "sim val=", sim_val
           if sim_val > reg_causing_revid_sim:
               rank  = rank + 1
       turn  = turn +1       
       
    return rank
        



str_bug = "select distinct bugid   from chromium_bugid_reg_revids"
select_cursor.execute(str_bug)
bug_data =  select_cursor.fetchall()

for id in bug_data:
    total_bugs =  total_bugs+1
    all_docs =  list()
    
    bugid = id[0]
    
    str_bug_info = "select title from  "+bug_report_feature_table+ " where bugid="+(str)(bugid)
    print "str bug str=", str_bug_info
    select_cursor.execute(str_bug_info)
    bug_title_info  =  select_cursor.fetchall()
    bug_title = bug_title_info[0][0]
       
    all_docs.append(bug_title)
     
    candidate_revid_list = list()   
    str_revs =   "select revid, reg_causing  from "+ bugid_previous_30_days_revids_table +"  where  bugid="+(str)(bugid)
    print "str revs=", str_revs
    select_cursor.execute(str_revs)
    temp_revs = select_cursor.fetchall()
    
    reg_causing_revid = 0
    for r in temp_revs:
        print "r is =",r
        candidate_revid_list.append(r[0])  
               
        if r[1]==1:
            reg_causing_revid = r[0]  
    
    #Identify reg-causing revids and their log message
    reg_causing_revid_pos = 0
    count = 0
    for temp_rev in candidate_revid_list:
       # temp_rev=3017
        str_rev_info = "select  rev_log_message from "+revid_feature_table+ " where revid="+(str)(temp_rev)
        print "str=", str_rev_info
        select_cursor.execute(str_rev_info)
        rev_log_mess_info  =  select_cursor.fetchall()
        
        rev_log_mess =  rev_log_mess_info[0][0]
        all_docs.append(rev_log_mess)
        
        count= count + 1
        if temp_rev == reg_causing_revid:
            reg_causing_revid_pos = count
                  
            
    print "all docs=", all_docs , " pos=", reg_causing_revid_pos
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_docs)
    #print tfidf_matrix.shape
    
    sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    reg_causing_revid_sim = sim_matrix[0][reg_causing_revid_pos]
    print sim_matrix
    
    rank = get_rank(sim_matrix, threshold, reg_causing_revid_sim)
    if rank<=threshold:
       total_revids_found = total_revids_found +1
    

    #break   

print "Total bug found=", total_bugs
print  "total revids =", total_revids_found
precision =  (total_revids_found*100)/total_bugs
print "precsion = ", precision
    

