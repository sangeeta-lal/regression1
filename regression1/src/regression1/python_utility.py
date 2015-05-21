import urllib2
import re
import xml.etree.ElementTree 

def check_for_show_all(web_page_data, revid):
    start_index =  web_page_data.index("Changed paths:")
    end_index = web_page_data.index("</tr>", start_index)
    substring = web_page_data[start_index:end_index]
    flag = substring.find("show all")
    if flag!=-1:
        return 1
    else:
        return 0

def get_log_message(web_page_data):
    index1 =  web_page_data.find("vc_log\">")
    index2 = web_page_data.find("</pre>", index1)
    log_message  =  web_page_data[index1+8:index2]
    #print "log messge= ", log_message
    return log_message
 
def remove_html_tags(rev_log_message):     
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr,'', rev_log_message)
   #print "clean text = ", cleantext
   return cleantext   
def remove_quote(rev_log_message):     
   rev_log_message =  rev_log_message.replace("'", " ")
   rev_log_message =  rev_log_message.replace("\""," ")
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
   # t = pandas.tslib.Timestamp.now()
    return 1,  2       

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
   index1 = change_path.find("<tr")
   count=0
   while index1!=-1:
       count  = count+1
       index2 = change_path.find("</tr>",  index1)
       substring  =  change_path[index1:index2]
                  
       start_index = substring.find("/>")
       end_index =  substring.find("</a>")
       
       substring = substring[start_index+2:end_index]
       changed_files = changed_files+"\n"+substring
            
       index1 = change_path.find("<tr", index2)
     
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
#Extract the lines which got addded in the  SVN   
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
   print "vc diff add total = ", vc_diff_added_count_total, " remove count=", vc_diff_removed_count_total, "vc_diff_change_count=",  vc_diff_changed_count_total
   return vc_diff_added_count_total, vc_diff_removed_count_total, vc_diff_changed_count_total, total_chunks_added, total_chunks_removed, total_chunks_changed

def get_desired_chunk_count(string, file_content):
   # print  "desired string in chunks count= ", content
    
    chunk_count = 0
    flag = 0
    index1= file_content.find(string)
   
    if index1!= -1:
        flag = 1
        chunk_count =1
        
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
               
        index2=  index1
        index1= file_content.find(string,index2+1)
     
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

"""      
#Extract the lines which got changed in the  SVN   
def get_lines_changed_count(web_page_data, web_page_url, project_basic_url):
   index= web_page_data.rfind("Path")
   
   start_index =web_page_data.find("<tbody>", index) 
   end_index = web_page_data.find("</tbody>", start_index)
   change_path =web_page_data[start_index:end_index+8]
   #print "change path", change_path
   index1 = change_path.find("<tr")
   count=0
   vc_diff_change_count_total=0
   while index1!=-1:
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
                #print "new url in chnaged= ", new_file_url
                modif_page_info =  urllib2.urlopen(new_file_url)
                modif_page_data =  modif_page_info.read()
        
                modif_content_start_index=modif_page_data.find("<table cellspacing") 
                modif_content_end_index = modif_page_data.find("</table>", modif_content_start_index) 
                modif_content = modif_page_data[modif_content_start_index:modif_content_end_index]
           
                vc_diff_change_count =get_desired_string_count("vc_diff_change", modif_content)  
                #print "vc dif change in change", vc_diff_change_count         
                vc_diff_change_count_total =  vc_diff_change_count_total + vc_diff_change_count
                      
       index1 = change_path.find("<tr", index2)

   vc_diff_change_count_total =  vc_diff_change_count_total/2  #Intetinaly making it half because the desired regular expression is present two times
   print "vc diff change total = ", vc_diff_change_count_total
   return vc_diff_change_count_total 


#Extract the lines which got deleted in the  SVN   
def get_lines_deleted_count(web_page_data, web_page_url, project_basic_url):
   index= web_page_data.rfind("Path")
   
   start_index =web_page_data.find("<tbody>", index) 
   end_index = web_page_data.find("</tbody>", start_index)
   change_path =web_page_data[start_index:end_index+8]
   #print "change path", change_path
   index1 = change_path.find("<tr")
   count=0
   vc_diff_remove_count_total=0
   while index1!=-1:
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
               #sprint "new url = ", new_file_url
               modif_page_info =  urllib2.urlopen(new_file_url)
               modif_page_data =  modif_page_info.read()
        
               modif_content_start_index=modif_page_data.find("<table cellspacing") 
               modif_content_end_index = modif_page_data.find("</table>", modif_content_start_index) 
               modif_content = modif_page_data[modif_content_start_index:modif_content_end_index]
           
               vc_diff_remove_count =get_desired_string_count("vc_diff_remove", modif_content)           
               vc_diff_remove_count_total =  vc_diff_remove_count_total + vc_diff_remove_count
                      
       index1 = change_path.find("<tr", index2)

   print "vc diff remove total = ", vc_diff_remove_count_total
   return vc_diff_remove_count_total
   """   