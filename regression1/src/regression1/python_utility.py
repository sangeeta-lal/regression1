import urllib2
import re
import xml.etree.ElementTree 




def get_log_message(web_page_data):
    index1 =  web_page_data.find("vc_log\">")
    index2 = web_page_data.find("</pre>", index1)
    log_message  =  web_page_data[index1+8:index2]
    print "log messge= ", log_message
    return log_message
 
def remove_html_tags(rev_log_message):     
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr,'', rev_log_message)
   print "clean text = ", cleantext
   return cleantext   

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
           

def no_of_files_modified(web_page_data):
    index =  web_page_data.index("Changed paths:")
    index = web_page_data.index("<strong>",index)
    start_index = web_page_data.index(">", index)
    end_index = web_page_data.index("</", index)
    file_changed_count = web_page_data[start_index+1:end_index] 
    #print "file changed=", file_changed_count
    return file_changed_count

def test_file_count(web_page_data):
   
   test_file_count = 0    
   index= web_page_data.rfind("Path")
   #print "index = ", index
   start_index =web_page_data.find("<tbody>", index) 
   end_index = web_page_data.find("</tbody>", start_index)
   change_path =web_page_data[start_index:end_index+8]
   #print "change path", change_path
   index1 = change_path.find("<tr")
   count=0
   while index1!=-1:
       count=count+1
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
   vc_diff_add_count_total=0
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
                print "new url in added = ", new_file_url
                modif_page_info =  urllib2.urlopen(new_file_url)
                modif_page_data =  modif_page_info.read()
                #print "I can read "
        
                modif_content_start_index=modif_page_data.find("<table cellspacing") 
                modif_content_end_index = modif_page_data.find("</table>", modif_content_start_index) 
                modif_content = modif_page_data[modif_content_start_index:modif_content_end_index]
           
                vc_diff_add_count =get_desired_string_count("vc_diff_add", modif_content)           
                vc_diff_add_count_total =  vc_diff_add_count_total + vc_diff_add_count
                      
       index1 = change_path.find("<tr", index2)

   print "vc diff add total = ", vc_diff_add_count_total
   return vc_diff_add_count_total

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
               print "new url = ", new_file_url
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
                print "new url = ", new_file_url
                modif_page_info =  urllib2.urlopen(new_file_url)
                modif_page_data =  modif_page_info.read()
        
                modif_content_start_index=modif_page_data.find("<table cellspacing") 
                modif_content_end_index = modif_page_data.find("</table>", modif_content_start_index) 
                modif_content = modif_page_data[modif_content_start_index:modif_content_end_index]
           
                vc_diff_change_count =get_desired_string_count("vc_diff_change", modif_content)           
                vc_diff_change_count_total =  vc_diff_change_count_total + vc_diff_change_count
                      
       index1 = change_path.find("<tr", index2)

   vc_diff_change_count_total =  vc_diff_change_count_total/2  #Intetinaly making it half because the desired regular expression is present two times
   print "vc diff change total = ", vc_diff_change_count_total
   return vc_diff_change_count_total
 


def get_desired_string_count(string, content):
    count =0
    index1= content.find(string)

    while index1!=-1:
        count= count +1
        index2=  index1
        index1= content.find(string,index2+1)
          
    return count        

