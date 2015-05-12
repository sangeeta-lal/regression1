package regression1;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;

import com.google.gdata.client.projecthosting.ProjectHostingService;
import com.google.gdata.data.projecthosting.Id;
import com.google.gdata.data.projecthosting.IssuesEntry;
import com.google.gdata.data.projecthosting.Label;


/*
 * @Uses: This program is used to download the other revision ids that are committed within  30 days of the reported bug. 
 * */
public class identify_training_revids 
{

   
    private String driver = "com.mysql.jdbc.Driver";
    
    private String dbName ="regression1" ;   
	private String project = "chromium";
    private String bugid_table = project  +"_bugid_reg_revids";  
    private String bugid_previous_30_days_revids_table = project+"_bugid_previous_30day_revids";
   /*
    private String userName = "root";
    private String password = "1234"; 
    private String url = "jdbc:mysql://localhost:3306/"; */
    
   // /*
    private String userName = "sangeetal";
    private String password = "sangeetal"; 
    private String url = "jdbc:mysql://localhost:3307/";
    // */
    
    private ProjectHostingService myService = null;
    private Connection conn = null;


  private void initdb()
   {
     try {
	     Class.forName(driver).newInstance();
	     conn = DriverManager.getConnection(url+dbName,userName,password);
	    } 
       catch (Exception e) 
        {
            e.printStackTrace();
        }
   }
  private void closedb()
  { 
	  try 
	  {
		  if(conn!=null) 
			  	conn.close();
	  } catch (Exception e) 
	  	{
		  e.printStackTrace();
	  	}
	} 
  

private void extract_and_insert_ground_truth_info() 
	{
	   URL revid_url;
	   Date date;
	   String revid_content = "";
	   int reg_causing_commit = 1;
	   java.sql.Timestamp bug_report_time_T2 = null;
	   java.sql.Timestamp  bug_report_30_day_before_T1  =null;
	   double bugid_revid_day_diff= 0.0 ;
	try {
	      myService = new ProjectHostingService("Sample Application");	      
	      String bugid_str = "select bugid, revid from "+  bugid_table;
	      Statement stmt =  conn.createStatement();
	      stmt.executeQuery(bugid_str);
	      ResultSet result = stmt.getResultSet();
	      while(result.next())
	      {
	    	  DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.0");
	    	  System.out.println("Bugid="+ result.getInt("bugid"));
	    	  int bugid=  result.getInt("bugid");
	    	  int revid = result.getInt("revid");
	    	 	  
	    	  bug_report_time_T2 = extract_reported_time(myService, Integer.toString(bugid)); 
	    	  date = bug_report_time_T2;
	    	  Calendar cal = Calendar.getInstance();
	    	  cal = Calendar.getInstance(TimeZone.getDefault());
	          cal.setTime(date);
	          cal.add(Calendar.DATE, -30);
	    	  bug_report_30_day_before_T1 = new Timestamp( cal.getTime().getTime());
	    	  	    	
	    	  revid_url   =new URL("http://src."+project+".org/viewvc/chrome?revision="+revid+"&view=revision");
	    	  BufferedReader in = new BufferedReader(new InputStreamReader(revid_url.openStream()));
              
	    	  String inputline;
	    	  revid_content = "";
	    	  while ((inputline = in.readLine()) != null)
	    	     {
	    		  
	    		     revid_content = revid_content + inputline;
	    	     
	    	     }	    	   
	    	//  System.out.println("revid="+revid+ "   Revid content  =" + revid_content);
	    	  java.sql.Timestamp revid_commit_time =  get_revid_timestamp(revid_content);
	    	  bugid_revid_day_diff  = bug_report_time_T2.getTime() - revid_commit_time.getTime();
	          bugid_revid_day_diff = bugid_revid_day_diff / (24*60 * 60 * 1000);
	          
	    	  in.close();
	    	  insert_infor_in_db(bugid, revid, bug_report_time_T2, bug_report_30_day_before_T1, revid_commit_time, reg_causing_commit, bugid_revid_day_diff);
	    	  
	      }
	      
	    }
	   catch (Exception e){System.out.println(e);}
		
	}
  
   
//This function will be used 
private void extract_other_revids()
{	
	
	 String bugid_str = "select bugid, revid, bug_report_time_T2, bug_report_time_minus_30_day_T1  from "+  bugid_previous_30_days_revids_table;
     Statement stmt =null;
     try 
      {
    	 stmt=  conn.createStatement();
    	 stmt.executeQuery(bugid_str);
    	 ResultSet result = stmt.getResultSet();
    	 while(result.next())
    	 	{
    		 	DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.0");
    		 	System.out.println("Bugid="+ result.getInt("bugid"));
    		 	int bugid=  result.getInt("bugid");
    		 	
    		 	int revid = result.getInt("revid");
    		 	
    		 	java.sql.Timestamp  bug_report_time_T2 = result.getTimestamp("bug_report_time_T2");
    		 	java.sql.Timestamp  bug_report_30_day_before_T1 =  result.getTimestamp("bug_report_time_minus_30_day_T1");
    		 	boolean flag =  true;
    		 	int temp_revid = revid-1;
    		 	while(flag)
    		 	{
    		 		////
    		 		 // System.out.println("bugid"+bugid+"  temp revid"+temp_revid);	
    		 		  ////
    		 		  URL revid_url   =new URL("http://src."+project+".org/viewvc/chrome?revision="+temp_revid+"&view=revision");
    		    	  BufferedReader in = new BufferedReader(new InputStreamReader(revid_url.openStream()));
    	              
    		    	  String inputline;
    		    	  String temp_revid_content = "";
    		    	  while ((inputline = in.readLine()) != null)
    		    	     {
    		    		  
    		    		     temp_revid_content = temp_revid_content + inputline;
    		    	     
    		    	     }	    	   
    		    	
    		    	  in.close();
    		    	  
    		    	  java.sql.Timestamp temp_revid_commit_time =  get_revid_timestamp(temp_revid_content);
    		    	  int reg_causing_commit = 0;
    		    	  
    		    	  double temp_bugid_revid_day_diff  = bug_report_time_T2.getTime() - temp_revid_commit_time.getTime();
    		          temp_bugid_revid_day_diff = temp_bugid_revid_day_diff / (24*60 * 60 * 1000);
    		         
    		          /*
    		          System.out.println("revid commit time = "+  temp_revid_commit_time);
    		          System.out.println(" bug report time ="+ bug_report_time_T2);
    		          if(temp_revid_commit_time.before(bug_report_time_T2) )
    		    	  {
    		        	  System.out.println("condition satisfied");
    		    	  }*/
    		          
    		    	  if((temp_revid_commit_time.before(bug_report_time_T2) )&&(temp_revid_commit_time.after(bug_report_30_day_before_T1)))
    		    	  {
    		    		  
    		    		  insert_infor_in_db(bugid, temp_revid, bug_report_time_T2, bug_report_30_day_before_T1, temp_revid_commit_time, reg_causing_commit, temp_bugid_revid_day_diff);
    			    	  
    		    		  temp_revid--;
    		    		  
    		    	  }
    		    	  else
    		    	  {
    		    	  
    		 		     flag =  false;
    		    	  }
    		 	
    		 	}//while
    		 	
    		 	
    		 	//Now increment revid 
    		 	flag =  true;
    		 	temp_revid = revid+1;
    		 	while(flag)
    		 	{
    		 		 //System.out.println("bugid"+bugid+"  temp revid"+temp_revid);
    		 		
    		 		  URL revid_url   =new URL("http://src."+project+".org/viewvc/chrome?revision="+temp_revid+"&view=revision");
    		    	  BufferedReader in = new BufferedReader(new InputStreamReader(revid_url.openStream()));
    	              
    		    	  String inputline;
    		    	  String temp_revid_content = "";
    		    	  while ((inputline = in.readLine()) != null)
    		    	     {
    		    		  
    		    		     temp_revid_content = temp_revid_content + inputline;
    		    	     
    		    	     }	    	   
    		    	
    		    	  in.close();
    		    	  
    		    	  java.sql.Timestamp temp_revid_commit_time =  get_revid_timestamp(temp_revid_content);
    		    	  int reg_causing_commit = 0;
    		    	  
    		    	  double temp_bugid_revid_day_diff  = bug_report_time_T2.getTime() - temp_revid_commit_time.getTime();
    		          temp_bugid_revid_day_diff = temp_bugid_revid_day_diff / (24*60 * 60 * 1000);
    		          
    		          /*
    		          System.out.println("revid commit time = "+  temp_revid_commit_time);
    		          System.out.println(" bug report time ="+ bug_report_time_T2);
    		          if(temp_revid_commit_time.before(bug_report_time_T2) )
    		    	  {
    		        	  System.out.println("condition satisfied");
    		    	  }
    		          */
    		          
    		          if((temp_revid_commit_time.before(bug_report_time_T2) )&&(temp_revid_commit_time.after(bug_report_30_day_before_T1)))
    		    	  {
    		    		  
    		    		  insert_infor_in_db(bugid, temp_revid, bug_report_time_T2, bug_report_30_day_before_T1, temp_revid_commit_time, reg_causing_commit, temp_bugid_revid_day_diff);
    			    	  
    		    		  temp_revid++;
    		    		  
    		    	  }
    		    	  else
    		    	  {
    		    	  
    		 		   flag =  false;
    		    	  }
    		 	
    		 	}//while   		 	
    		 	
    	 	}// result.next
      }catch(Exception e)
     {
    	e.printStackTrace();  
     }
   	 	
}
   private void insert_infor_in_db(int bugid, int revid, Timestamp bug_report_time_T2, Timestamp bug_report_30_day_before_T1, Timestamp revid_commit_time, int reg_causing_commit,
		double bugid_revid_day_diff) 
   {
	
	String str = "insert into "+bugid_previous_30_days_revids_table + " values("+bugid+","+revid+",'"+bug_report_time_T2+"','"+ bug_report_30_day_before_T1+"','"+revid_commit_time+"',"+
	reg_causing_commit+","+bugid_revid_day_diff+")";
	Statement stmt = null;
	try {
		stmt =  conn.createStatement();
		stmt.executeUpdate(str);
	    stmt.close();  
	
	  } catch (SQLException e) 
	   {
           e.printStackTrace();
	   }
	
   }  
   
 
/*This method will return timestamp of revision*/
   private Timestamp get_revid_timestamp(String revid_content) 
   {
	   Date value = null;
	   java.sql.Timestamp rev_commit_time=null;
	   
	   int start_index =  revid_content.indexOf("Date:");
	   start_index = start_index+14;
	   int end_index = revid_content.indexOf("UTC<em>", start_index);
	   String date_str =  revid_content.substring(start_index, end_index);
	   date_str =  date_str.trim();

	   try 
	      {
	       
		   SimpleDateFormat oldformat = new SimpleDateFormat("EEE MMM dd HH:mm:ss yyyy");  
	       java.util.Date date2 = oldformat.parse(date_str);
	       //System.out.println("revid DATE 2="+ date2);
	       rev_commit_time= new java.sql.Timestamp(date2.getTime());
	   
 		   
	      } catch (Exception e)
 	       {
		     e.printStackTrace();
	       }
      
 	 return rev_commit_time;
   }
   
   
public Timestamp extract_reported_time(ProjectHostingService service, String issueId)
   {
     try
       { 
           URL feedUrl = new URL("https://code.google.com/feeds/issues/p/"+project+"/issues/full/" + issueId);
           IssuesEntry entry = service.getEntry(feedUrl, IssuesEntry.class);         
           Id id = entry.getIssueId();
           int issueID = id.getValue();
           java.sql.Timestamp reported = new Timestamp(entry.getPublished().getValue());
          //System.out.println("REPORTED : " + reported);           
           return reported;
               
       }catch(Exception e){
         System.out.println(e);
       
       }
	return null;
     }
   
public static void main(String args[])
    {
    	identify_training_revids itr = new identify_training_revids();
    	itr.initdb();
    //	itr.extract_and_insert_ground_truth_info();
    	itr.extract_other_revids();
    	
    	itr.closedb();
    }    
	
}// class



