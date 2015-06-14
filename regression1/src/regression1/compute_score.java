package regression1;

import java.awt.List;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Arrays;

import com.aliasi.tokenizer.Tokenizer;

/*@Author: Sangeeta
 * This file is used to compute the score of a revision commit with respect to bug report feature
 * 
 * */
public class compute_score 
{
	 private String driver = "com.mysql.jdbc.Driver";	     
	
	 /*
	 private String url = "jdbc:mysql://localhost:3306/";
	 private String userName = "root";
	 private String password = "1234"; 
	 private String dbName ="regression1" ;   
	 private String project = "chromium"; */
	
	// /* 
	 private String url = "jdbc:mysql://localhost:3307/";
	 private String dbName ="regression1" ;   
	 private String project = "chromium";
	 private String userName = "sangeetal";
	 private String password = "sangeetal";
	 // */
	  	 
	 private String bug_feature_table = project  +"_bug_report_features";  
	 private String revid_feature_table= project+"_revids_feature";
	 private String bugid_previous_30_days_revids_table = project+"_bugid_previous_30day_revids";
	 private String score_table = project  +"_score_table";
	 private Connection conn = null;
     private Statement stmt = null;
     
	 String description = "";
	 String title = "";
	 String cr= "";
	 String area = "";	
	
	
	String stop_words []= {"hard", "what", "instead","being", "do", "you", "will", "well", "reproduce", "something", "properly", "getting", "basically" };
	String stop_phrases[]= {"Report ID", "Cumulative Uptime", "Other Browsers Tested", "Meta Information", "Thank You"};
	String stop_sentences[] = {"What steps will reproduce the problem","What is the expected output", "What do you see instead","Kindly refer the screencast for reference"};
			
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
	 
   
   //This function will compute the score of the revision and bug report and will insert in the table
   public void compute_initial_score()
   {
	   utill uti  =  new utill();
	   String bugid_str  = "select distinct bugid from "+ bugid_previous_30_days_revids_table;
	   
	   try
	   {
		  stmt  = conn.createStatement();
		  stmt.executeQuery(bugid_str);
		  ResultSet bugid_rs =  stmt.getResultSet();
		  while(bugid_rs.next())
		  {
			  int bugid = bugid_rs.getInt("bugid");
			  System.out.println("Bugid = "+bugid);
			  
			  String bug_feature =  "select title, description,cr,area from " + bug_feature_table +"  where bugid = "+bugid;
			  Statement stmt2 =  null;
			  ResultSet rs2 =  null;
			  String title = "";
		      String desc = "";	
		      String cr = "";
		      String area = "";
		      ArrayList<String>   cr_plus_area = new ArrayList<String>();
		      //String cr_plus_area = "";
		      
			  stmt2 =  conn.createStatement() ; 
			  stmt2.executeQuery(bug_feature);
			  rs2 =  stmt2.getResultSet();
			  
			  while(rs2.next())
			  {
				title =  rs2.getString("title") ;
				desc = rs2.getString("description");
				
				title= uti.pre_process(title);
				desc = uti.pre_process(desc);
				
				cr = rs2.getString("cr");
				area =  rs2.getString("area");
				 //System.out.println("CR="+cr+  " Area"+area);
				//cr_plus_area = cr+" "+area;
			  }
			  
			  String[] title_ngram =  uti.getngram(title);
			  String[] desc_ngram =  uti.getngram(desc);
			  
			  String [] cr_ngram = uti.getngram(cr);
			  String [] area_ngram = uti.getngram(area);
			 
			  cr_plus_area.addAll(Arrays.asList(cr_ngram));
			  cr_plus_area.addAll(Arrays.asList(area_ngram));
			  Object cr_plus_area_obj_ngram[] = cr_plus_area.toArray();
			  String cr_plus_area_ngram[] = Arrays.copyOf(cr_plus_area_obj_ngram, cr_plus_area_obj_ngram.length, String[].class);
			 
			  //System.out.println("CR="+cr+  " Area"+area);
			  //uti.print_ngrams(cr_plus_area_ngram);
			  
			  Statement stmt3 = null;
			  String revid_str  = "select revid from "+ bugid_previous_30_days_revids_table +"  where  bugid="+bugid;
			  stmt3= conn.createStatement();
			  stmt3.executeQuery(revid_str) ;
			  ResultSet revid_rs  = stmt3.getResultSet();
			  
			  while(revid_rs.next())
			  {
				 
				  int revid = revid_rs.getInt("revid");
				  System.out.println("Bugid="+ bugid+ " Revid = "+ revid);
				  
				  double revid_size_score = compute_size_score(revid);				  
				  String rev_feature_str = "select  rev_log_message, changed_files from " + revid_feature_table +  "  where revid = "+revid;
				  //System.out.println("rev feature str = "+ rev_feature_str);
				  
				  Statement stmt4  = null;
				  stmt4 =  conn.createStatement();
				  stmt4.executeQuery(rev_feature_str);
				  ResultSet rev_feature_val  =  stmt4.getResultSet();
				  
				  String log_mess = "";
				  String top_change_path = "";
				  String change_path_str = "";
				  
				
				  while(rev_feature_val.next())
				  {
					  
					  log_mess =  rev_feature_val.getString("rev_log_message");
					  change_path_str = rev_feature_val.getString("changed_files");
					  //System.out.println("Log message = "+ log_mess);
					  log_mess =  uti.pre_process(log_mess);
					 
				  }
				  
				  String[]  log_mess_arr = uti.getngram(log_mess);
				  
				  String change_path_arr[]= change_path_str.split("\n");
				  ArrayList<String> change_path_list = new ArrayList<String>();
				  ArrayList<String> change_path_top_level_list = new ArrayList<String>();
				  
				  
				  String[] change_path_ngram = null;
				  Object [] change_path_obj_ngram =null;
				  
				  String [] change_path_top_level_ngram = null;
				  Object [] change_path_top_level_obj_ngram = null;
				  
				  
				  for(int i=0; i<change_path_arr.length; i++)
				  {
					  String line =  change_path_arr[i];
					  //System.out.println("  line="+line);
					  String []temp_line_ngram  = uti.getngram(line);
					  change_path_list.addAll(Arrays.asList(temp_line_ngram));
					  
					  //calculation for top level
					  String new_line = "";
					  if (null != line && line.length() > 0 )
					  {
					      int endIndex = line.lastIndexOf("/");
					      if (endIndex != -1)  
					      {
					          new_line = line.substring(0, endIndex); // not forgot to put check if(endIndex != -1)
					      }
					  					      
					  } 
					  
					  //System.out.println("new line = "+ new_line);
					  String []temp_line_top_level_ngram  = uti.getngram(new_line);
					  change_path_top_level_list.addAll(Arrays.asList(temp_line_top_level_ngram));					  
					  
				  }
				  
				  change_path_obj_ngram = change_path_list.toArray();
				  change_path_ngram = Arrays.copyOf(change_path_obj_ngram, change_path_obj_ngram.length, String[].class);
				  
				  change_path_top_level_obj_ngram = change_path_top_level_list.toArray();
				  change_path_top_level_ngram = Arrays.copyOf(change_path_top_level_obj_ngram, change_path_top_level_obj_ngram.length, String[].class);
				  
				  //System.out.println("cr ="+ cr);
				 // uti.print_ngrams(cr);
				  
				  double title_log_sim_score = uti.compute_similiarity(title_ngram, log_mess_arr);
				  double desc_log_mess_score  =  uti.compute_similiarity(desc_ngram, log_mess_arr);
				  double title_change_path_score = uti.compute_similiarity(title_ngram, change_path_ngram);
				  double cr_area_top_level_change_path_score = uti.compute_similiarity(cr_plus_area_ngram, change_path_top_level_ngram);
				  
				  double combined_score = 0.0;
				  
				  String insert_str = "insert into "+ score_table + "  values("+ bugid+","+ revid+","+ revid_size_score+ ","+ title_log_sim_score+","+desc_log_mess_score+","+ title_change_path_score+","+
				  +cr_area_top_level_change_path_score+","+combined_score+","+"''"+","+0+","+0+","+0+","+0+","+0+","+0+","+0+","+0+","+0+","+"''"+","+0+","+0+","+0+","+0+","+0+","+0+","+0+","+0.0+")";
			
				  
				  stmt4.execute(insert_str);
				  
				  rev_feature_val.close();
				  stmt4.close();
			  }
			  
			  
			  rs2.close();
			  revid_rs.close();
			  stmt2.close();
			  stmt3.close();
		  }//while
	   
          bugid_rs.close();	   
		  stmt.close();
	   } catch (SQLException e) 
	     {
             e.printStackTrace();
	     }
	   
	   
   }
    
   // Used to compute the score of revid using size score
   private double compute_size_score(int revid) 
   {
	
	return 1.0;
   }

   // This will be used to combine the scores calculated by individual component
	private void update_combine_score()
	{
		Statement stmt =  null;
		Statement stmt2 =  null;
		try
		  {
			  stmt =  conn.createStatement();
			  stmt2 =  conn.createStatement();
			  String str =  "select  bugid, revid, size_score, title_log_ngram_sim, desc_log_ngram_sim from " + score_table;
			  stmt.executeQuery(str) ; 
			  ResultSet rs =  stmt.getResultSet();
			  while(rs.next())
			  {
				  int bugid =  rs.getInt("bugid");
				  int revid=  rs.getInt("revid") ; 
				  
				  double size_score  = rs.getDouble("size_score");
				  double title_log_ngram_sim =  rs.getDouble("title_log_ngram_sim");
				  double desc_log_ngram_sim =  rs.getDouble("desc_log_ngram_sim");
				  double combined_score = calculate_combine_score(size_score, title_log_ngram_sim, desc_log_ngram_sim);
		          
				  String update_str =  "update  "+ score_table + " set combined_score = " + combined_score + " where bugid=" + bugid+" and revid = "+ revid;
				  stmt2.executeUpdate(update_str);
				  System.out.println("update str = "+ update_str);
				  
			  }//while
			  
			  stmt2.close();
			  rs.close();
			  stmt.close();
		   } catch (SQLException e) 
		    {
		      e.printStackTrace();
		    }
		
	}
   
	private double calculate_combine_score(double size_score,double title_log_ngram_sim, double desc_log_ngram_sim)
	  {
			double combined = 0.0;
			
			combined =  size_score + title_log_ngram_sim  + desc_log_ngram_sim;
			return combined;
		}
	public static void main(String args[])
     {
	   compute_score  sc =  new compute_score();
	   sc.initdb();
	   sc.compute_initial_score();
	   sc.update_combine_score( );
	   sc.closedb();
    }//main

}

