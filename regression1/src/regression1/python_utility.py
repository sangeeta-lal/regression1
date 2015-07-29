import urllib2
import re
import xml.etree.ElementTree
import pandas 
from nltk.stem.porter import PorterStemmer
from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math
from nltk.corpus import stopwords

#@===To Compute the ngram of a string=====#
def compute_ngram(string1, n1, n2):
    ngram_str1 = list()
    while n1<=n2:
        temp= [string1[i:i+n1] for i in range(len(string1)-n1+1)]
        for t in temp:
            ngram_str1.append(t) 
         
        n1= n1+1    
    
    return ngram_str1

#@====To computer length of the ngram list====#
def compute_len(ngram_list):
    counts = Counter(ngram_list)
    value= 0.0
        
    print "counter=", counts
    for val in counts.values():
        value= value + val*val
     
        
    length= math.sqrt(value) 
    print "len=", length   , "  value =", value
    return length
        
##======@Compute the similiarity using Khattar Matrix==============#
def calculate_normalized_ngram_and_khattar_sim(string1, string2, size1, size2):
    n1= size1
    n2= size2
    
    sim = 0.0  #sim value
    
    ngram_str1_list = compute_ngram(string1, n1, n2)
    ngram_str2_list = compute_ngram(string2, n1, n2)
 
    for t1 in ngram_str1_list:
        for t2 in ngram_str2_list:
            if t1==t2:
                sim = sim+ len(t1)
    
    len_ngram_str1 = compute_len(ngram_str1_list)
    len_ngram_str2 = compute_len(ngram_str2_list)
    
   
    print "sim=", sim 
    sim = sim/(len_ngram_str1* len_ngram_str2) 
           
    print "str1", ngram_str1_list
    print "str2", ngram_str2_list
    
    print " final sim=", sim
    
    return sim  

#e===============@This fuction will return the similiarity matrix==========$
def compute_normalized_khattar_sim_matrix(string_list, initial_size, final_size):
    final_sim_matrix = []
    temp_sim_matrix=   []
    
    first_string=" "
    for temp in string_list:
        first_string = temp
        break
    
    for temp in string_list:
        sim_val = calculate_normalized_ngram_and_khattar_sim(first_string, temp,initial_size, final_size)
        temp_sim_matrix.append(sim_val)
    
    final_sim_matrix.append(temp_sim_matrix)    
    
    return final_sim_matrix 
        
##======@Compute khattar sim Matrix==============#
def create_khattar_all_sim_matrix_normalized(title_rev_log, desc_rev_log, cr_area_top_level, title_file_name, initial_size, final_size):
        
   # tfidf_vectorizer = TfidfVectorizer(stop_words='english',decode_error='ignore')
    tfidf_vectorizer = TfidfVectorizer()
                         
    title_rev_log_sim_matrix      = compute_normalized_khattar_sim_matrix(title_rev_log,   initial_size, final_size)
    desc_rev_log_sim_matrix       = compute_normalized_khattar_sim_matrix(desc_rev_log,    initial_size, final_size)
    cr_area_top_level_sim_matrix  = compute_normalized_khattar_sim_matrix(cr_area_top_level,initial_size, final_size)
    title_file_name_sim_matrix    = compute_normalized_khattar_sim_matrix(title_file_name,  initial_size, final_size)

    return  title_rev_log_sim_matrix , desc_rev_log_sim_matrix , cr_area_top_level_sim_matrix, title_file_name_sim_matrix
    
temp = list()
temp.append("anan")
temp.append("san")
output = create_khattar_all_sim_matrix_normalized(temp, temp, temp, temp,  2, 4)
print "output", output


#####@=========== get rank()======================================================================================================================================#######
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


"""#######========================@Tf-idf sim matrix=====================================================####
#=======================================================================================================# """
def create_tf_idf_sim_matrix( title_rev_log, desc_rev_log, cr_area_top_level, title_file_name):
    #print "Title- rev", title_rev_log
    #print "Desc-rev", desc_rev_log
    #print "cr_area_top_level", cr_area_top_level
    #print "title_file_name", title_file_name
    
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
    
    #print "sim title-rev log", title_rev_log_sim_matrix    
    #print "desc rev log", desc_rev_log_sim_matrix      
    #print "cr area top", cr_area_top_level_sim_matrix 
    #print "title file name", title_file_name_sim_matrix
    
    return   title_rev_log_sim_matrix, desc_rev_log_sim_matrix, cr_area_top_level_sim_matrix, title_file_name_sim_matrix



def check_for_show_all(web_page_data, revid):
    start_index =  web_page_data.index("Changed paths:")
    end_index = web_page_data.index("</tr>", start_index)
    substring = web_page_data[start_index:end_index]
    flag = substring.find("show all")
    if flag!=-1:
        return 1
    else:
        return 0

def get_log_message_and_comitter(web_page_data):
    index1 =  web_page_data.find("vc_log\">")
    index2 = web_page_data.find("</pre>", index1)
    log_message  =  web_page_data[index1+8:index2]
    #print "log messge= ", log_message
    
    index1 = web_page_data.find("<th>Author:</th>")
    auth_index1 =  web_page_data.find("<td>", index1)
    auth_index2 = web_page_data.find("</td>", auth_index1)
    comitter =  web_page_data[auth_index1+4:auth_index2]
    comitter =  comitter.strip()

    return log_message, comitter
 
def remove_html_tags(rev_log_message):     
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr,'', rev_log_message)
   #print "clean text = ", cleantext
   return cleantext   

def remove_operator_camel_stem(input_str):
    #====remove operator====#
    input_str = re.sub(r"[\+\*%-/&|^=!]", " ", input_str)
    input_str = re.sub(r"[<>\{\}\(\)\[\]]", " ", input_str)
    input_str = re.sub(r"[@#$_\\\'\":;\.,\?0-9]", " ", input_str)
    input_str = re.sub(r" +"," ", input_str)
    
    """
    #====camel casing=======#
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_str)
    s1= re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    s2 = s1.split("_")
    
    final= " "
    for s in s2:
        final = final+" "+s
    final = final.strip()
    """    
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_str)
    s1= re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    final = " ".join(word for word in s1.split("_"))
    
    #===stemming==========#
    temp = " ".join(PorterStemmer().stem_word(word) for word in final.split(" "))
    #print "temp=", temp
    
    #========stop words============#
    stop = stopwords.words('english')
    new_temp =" ".join(i for i in temp.split() if i not in stop)
     
    #======@ remove hexa decimal===========#
    re.sub('\\\\x\d\d', ' ', new_temp)
       
    return new_temp 

#print remove_operator_camel_stem("HelloSangeeta")   

def remove_quote_new_line(rev_log_message):     
   rev_log_message =  rev_log_message.replace("'", " ")
   rev_log_message =  rev_log_message.replace("\""," ")
   rev_log_message =  rev_log_message.replace("\n"," ")
   return rev_log_message

def contains_bug_fix(web_page_data):
    start_index =  web_page_data.index("Log Message:")
    end_index = web_page_data.index("</tr>",start_index)
    log_message =  web_page_data[start_index:end_index]
    log_message= log_message.lower()
    
    #print "log message=", log_message
    if  re.search(r'bug(\s*):?=?:?[0-9]+', log_message):
        return 1
    elif re.search(r'issue(\s*):?=?:?[0-9]+', log_message):
        return 1
    elif re.search(r'bug(\s*):?=?:?=<a href="http://crbug.com/[0-9]+">', log_message):
        return 1
    elif re.search(r'<a href="http://crbug.com/[0-9]+">', log_message):
        return 1
    else:
        return 0

def get_time(web_page_data):
    index =  web_page_data.find("Date:</th>")
    start_index = web_page_data.find("<td>", index)
    end_index =  web_page_data.find(" UTC", start_index)
    timestamp =  web_page_data[start_index+4:end_index]
    #print "timestamp= ",timestamp
    t = pandas.tslib.Timestamp(timestamp)
    day = t.day 
    month = t.month
    weakday = t.weekday()
    hour= t.hour
    return day,month, weakday, hour    

def no_of_files_modified(web_page_data):
    index =  web_page_data.index("Changed paths:")
    index = web_page_data.index("<strong>",index)
    start_index = web_page_data.index(">", index)
    end_index = web_page_data.index("</", index)
    file_changed_count = web_page_data[start_index+1:end_index] 
    #print "file changed=", file_changed_count
    return file_changed_count

def get_changed_files(web_page_data):
   changed_files = ""
   index= web_page_data.rfind("Path")
   #print "test index = ",(long)(index)
   start_index = web_page_data.find("<tbody>", index) 
   end_index   = web_page_data.find("</tbody>", start_index)
   change_path = web_page_data[start_index:end_index+8]
   #print "change path", change_path, "start=", start_index, " end index=", end_index
   index1 = change_path.find("<tr class")
   count=0
   while index1!=-1:
       count  = count+1
       index2 = change_path.find("</tr>",  index1)
       substring  =  change_path[index1:index2]
                  
       start_index = substring.find("/>")
       end_index =  substring.find("</a>")
       
       substring = substring[start_index+2:end_index]
       if changed_files=="":
           changed_files =  substring
       else:    
           changed_files = changed_files +"\n" + substring
            
       index1 = change_path.find("<tr", index2)
     
   change_files =  changed_files.strip()       
   change_files =  changed_files.lstrip()
   return changed_files

def test_file_count(web_page_data):   
   test_file_count = 0    
   index= web_page_data.rfind("Path")
   #print "test index = ",(long)(index)
   start_index = web_page_data.find("<tbody>", index) 
   end_index   = web_page_data.find("</tbody>", start_index)
   change_path = web_page_data[start_index:end_index+8]
   #print "change path", change_path, "start=", start_index, " end index=", end_index
   index1 = change_path.find("<tr")
   count=0
   while index1!=-1:
       count  = count+1
       index2 = change_path.find("</tr>",  index1)
       substring  =  change_path[index1:index2]
                  
       start_index = substring.find("/>")
       end_index =  substring.find("</a>")
       
       substring = substring[start_index+2:end_index]
       #print "file path",count,"=", substring
       file_depth= len(substring.split("/"))
       file_name = substring.split("/")[file_depth-1]
       #print "files=", file_name
       have_test_file = file_name.find("test")
       
       if have_test_file!=-1:
           test_file_count = test_file_count+1
       
       index1 = change_path.find("<tr", index2)
       
   #print "test file count = ",test_file_count    
   return test_file_count
#Extract the lines which got addded/ deleted /changed as well as chunkcount in the  SVN   
def get_lines_added_count(web_page_data, web_page_url, project_basic_url):
   index= web_page_data.rfind("Path")
   
   start_index =web_page_data.find("<tbody>", index) 
   end_index = web_page_data.find("</tbody>", start_index)
   change_path =web_page_data[start_index:end_index+8]
   #print "change path", change_path
   index1 = change_path.find("<tr")
   count=0
   vc_diff_added_count_total=0
   total_chunks_added=0
   vc_diff_removed_count_total = 0
   total_chunks_removed = 0
   vc_diff_changed_count_total =0
   total_chunks_changed  = 0
   
   while index1!=-1:
       #print "in while" 
       count=count+1
       index2 = change_path.find("</tr>",  index1)
       substring  =  change_path[index1:index2]
                  
       start_index = substring.find("/>")
       end_index =  substring.find("</a>")
       
       file_path = substring[start_index+2:end_index]
       #print "file path",count,"=", file_path
       
       file_depth= len(file_path.split("/"))
       file_name = file_path.split("/")[file_depth-1]
       #print "files=", file_name
      
       modified_index=substring.find(">modified<")
       
       if modified_index!=-1:
           modif_index1 = substring.find("href=", modified_index)
           if modif_index1!=-1 : 
                modif_index2 = substring.find("title=", modified_index)
                modif_file_url =  substring[modif_index1+6:modif_index2-2]
                #print "modif url = ", modif_file_url
           
                new_file_url = project_basic_url+modif_file_url           
                #print "new url in added = ", new_file_url
                modif_page_info =  urllib2.urlopen(new_file_url)
                modif_page_data =  modif_page_info.read()
                #print "I can read "
        
                modif_content_start_index=modif_page_data.find("<table cellspacing") 
                modif_content_end_index = modif_page_data.find("</table>", modif_content_start_index) 
                modif_content = modif_page_data[modif_content_start_index:modif_content_end_index]
                
            
                vc_diff_added_count =get_desired_string_count("vc_diff_add", modif_content)                       
                chunks_added_count = get_desired_chunk_count("vc_diff_add", modif_content)
                
                vc_diff_removed_count = get_desired_string_count("vc_diff_remove", modif_content)
                chunks_removed_count = get_desired_chunk_count("vc_diff_remove", modif_content)
                
               # print"modif content in added=", modif_content
                vc_diff_changed_count = get_desired_string_count("vc_diff_change", modif_content)
                chunks_changed_count = get_desired_chunk_count("vc_diff_change", modif_content)
                
                vc_diff_added_count_total =  vc_diff_added_count_total + vc_diff_added_count
                total_chunks_added = total_chunks_added + chunks_added_count
                
                vc_diff_removed_count_total  =  vc_diff_removed_count_total + vc_diff_removed_count
                total_chunks_removed =  total_chunks_removed + chunks_removed_count
                
                vc_diff_changed_count_total  =  vc_diff_changed_count_total + vc_diff_changed_count
                #print " total change in added=", vc_diff_changed_count_total
                total_chunks_changed =  total_chunks_changed + chunks_changed_count
                      
       index1 = change_path.find("<tr", index2)
   
   vc_diff_changed_count_total = vc_diff_changed_count_total/2
   #print "vc diff add total = ", vc_diff_added_count_total, " remove count=", vc_diff_removed_count_total, "vc_diff_change_count=",  vc_diff_changed_count_total
   return vc_diff_added_count_total, vc_diff_removed_count_total, vc_diff_changed_count_total, total_chunks_added, total_chunks_removed, total_chunks_changed

def get_desired_chunk_count(string, file_content):
    #print  "file content= ", file_content
    #print "chunk_type =", string
    #print "starting function with (", string,")"
    chunk_count = 0
    flag = 0
 
    index1 =  file_content.find("<tr>")
            
    while index1!=-1:
        tr_start_index =  file_content.find("<tr>", index1)
        tr_end_index = file_content.find("</tr>", tr_start_index)
        line_content = file_content[tr_start_index:tr_end_index]
        
        string_index = line_content.find(string)
        #print "line content = ", line_content 
        if string_index!=-1:
            if flag==0:
                flag = 1
                chunk_count =  chunk_count+1
        else:
            flag = 0
            #print "i am in else"
        
        #print "  \n chunk count=(",string,")", chunk_count, "flag=", flag     
        index2=  index1
        index1= file_content.find("<tr>",index2+1)
     
    #print "chunk count", chunk_count     
    return chunk_count 
def get_desired_string_count(string, file_content):
    count =0
    index1= file_content.find(string)

    while index1!=-1:
        count= count +1
        index2=  index1
        index1= file_content.find(string,index2+1)
          
    return count        

#Find maximum number of developers in a file
def get_max_no_of_devs_and_change_count_and_avg_comitter_expr(web_page_data, project, rev_comitter):
   changed_files = ""
   index= web_page_data.rfind("Path")
   #print "test index = ",(long)(index)
   start_index = web_page_data.find("<tbody>", index) 
   end_index   = web_page_data.find("</tbody>", start_index)
   change_path = web_page_data[start_index:end_index+8]
   #print "change path", change_path, "start=", start_index, " end index=", end_index
   index1 = change_path.find("<tr")
   count=0
   max_dev_count = 0
   max_change_count = 0
   total_rev_comitter_expr = 0.0
   file_count_modif_added=0
   only_deleted_files_flag = True
   while index1!=-1:
       rev_comitter_expr_file = 0.0
       dev_count = 0
       change_count = 0
       
       count  = count+1
       index2 = change_path.find("</tr>",  index1)
       substring  =  change_path[index1:index2]
            
       file_modified_index = substring.find(">modified<")
       if file_modified_index!=-1:
           dev_count,change_count, rev_comitter_expr_file   =  get_unique_dev_count_and_change_count_and_comitter_file_expr(substring, project, rev_comitter)
           file_count_modif_added = file_count_modif_added +1 
           only_deleted_files_flag =  False
           
       else:    
           file_added_index = substring.find(">added<")
        
           if file_added_index!=-1:
               dev_count=1  
               change_count = 1
               file_count_modif_added = file_count_modif_added +1 
               rev_comitter_expr_file = 100.0
               only_deleted_files_flag = False
              
               
       if dev_count >max_dev_count:
           max_dev_count = dev_count
       
       if change_count > max_change_count:
           max_change_count = change_count    
       
       total_rev_comitter_expr = total_rev_comitter_expr+ rev_comitter_expr_file 
       index1 = change_path.find("<tr", index2)
     
  # print "max_dev_coun = ", max_dev_count, "  max_change_count=", max_change_count
   if file_count_modif_added!=0:
       avg_rev_comitter_expr = total_rev_comitter_expr/file_count_modif_added
       #print " avg rev comitter expr=", avg_rev_comitter_expr
       
   else:
       if only_deleted_files_flag == True:
           avg_rev_comitter_expr = 100.0
               
   return max_dev_count , max_change_count, avg_rev_comitter_expr
#Rturns count of unique developers in a SVN
def  get_unique_dev_count_and_change_count_and_comitter_file_expr(row_detail,project, rev_comitter):
   # print "row detail = ", row_detail
    
    index= row_detail.rfind("<td")
    start_index = row_detail.find("<td><a href=\"",index)
    end_index =row_detail.find("title=\"View Log\">")
    link = row_detail[start_index+13:end_index-2]
    complete_file_link ="http://src."+project+".org/"+link
    
    
    diff_r =  urllib2.urlopen(complete_file_link)
    diff_data  =  diff_r.read()
    index1 = diff_data.find("by <em>")
    
    all_dev = list()
    rev_comitter_comits = 0
    change_count = 0
    while index1!=-1:
        change_count =  change_count+1
        
        start_index = index1
        end_index = diff_data.find("</em>", start_index)
        dev_name = diff_data[start_index+7:end_index]
        #print "dev name = ", dev_name
        if not all_dev:
            all_dev.append(dev_name)
        else:
            if dev_name not in all_dev:
                 all_dev.append(dev_name) 
        
        #Experince
        #print "dev name =", dev_name, " rev_comitter=", rev_comitter
        if dev_name ==  rev_comitter:
            rev_comitter_comits = rev_comitter_comits +1          
        
        index1 = diff_data.find("by <em>", end_index)
    #print "len =", len(all_dev), "change_count = ", change_count, "all dev=", all_dev
    
    rev_comitter_expr_file =  ((rev_comitter_comits*100)/ change_count)
    #print "modif comitter expr file=", rev_comitter_expr_file
    return len(all_dev),change_count, rev_comitter_expr_file
