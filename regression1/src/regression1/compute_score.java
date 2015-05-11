package regression1;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import com.aliasi.tokenizer.Tokenizer;


/*@Author: Sangeeta
 * This file is used to compute the score of a revision commit with respect to bug report feature
 * 
 * */
public class compute_score 
{
	
	 private String url = "jdbc:mysql://localhost:3306/";
	 private String driver = "com.mysql.jdbc.Driver";	    
	 private String dbName ="regression1" ;   
	 private String project = "chromium";
	 private String bug_feature_table = project  +"_bug_report_features";  
	 private String revid_feature_table= project+"_revids_feature";
	 private String bugid_previous_30_days_revids_table = project+"_bugid_previous_30day_revids";
	 private String score_table = project  +"_score_table";
	 private String userName = "root";
	 private String password = "1234";  
	 /* 
	 private String userName = "sangeetal";
	 private String password = "sangeetal";
	  */
	  	 
	 private Connection conn = null;
     private Statement stmt = null;
	 String description = "";
	 String title = "";
	 String cr= "";
	 String area = "";	
	 String log_message = ""; 
	
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
			  
			  String bug_feature =  "select title, description from " + bug_feature_table +"  where bugid = "+bugid;
			  Statement stmt2 =  null;
			  ResultSet rs2 =  null;
			  String title = "";
		      String desc = "";			  
			  stmt2 =  conn.createStatement() ; 
			  stmt2.executeQuery(bug_feature);
			  rs2 =  stmt2.getResultSet();
			  
			  while(rs2.next())
			  {
				title =  rs2.getString("title") ;
				desc = rs2.getString("description");
				
				title= uti.pre_process(title);
				desc = uti.pre_process(desc);
			  }
			  
			  String[] title_arr =  uti.getngram(title);
			  String[] desc_arr =  uti.getngram(desc);
			  
			  Statement stmt3 = null;
			  String revid_str  = "select revid from "+ bugid_previous_30_days_revids_table +"  where  bugid="+bugid;
			  stmt3= conn.createStatement();
			  stmt3.executeQuery(revid_str) ;
			  ResultSet revid_rs  = stmt3.getResultSet();
			  
			  while(revid_rs.next())
			  {
				  int revid = revid_rs.getInt("revid");
				  double revid_size_score = compute_size_score(revid);
				  
				  String rev_feature_str = "select  rev_log_message from " + revid_feature_table +  "  where revid = "+revid;
				  Statement stmt4  = null;
				  stmt4 =  conn.createStatement();
				  stmt4.executeQuery(rev_feature_str);
				  ResultSet rev_feature_val  =  stmt4.getResultSet();
				  
				  String log_mess = "";
				  String change_patth = "";
				  
				  while(rev_feature_val.next())
				  {
					  log_mess =  rev_feature_val.getString("rev_log_message");
					  log_mess =  uti.pre_process(log_mess);
				  }
				  
				  String[]  log_mess_arr = uti.getngram(log_mess);
				  
				  double title_log_sim_score = uti.compute_similiarity(title_arr, log_mess_arr);
				  double desc_log_mess_score  =  uti.compute_similiarity(desc_arr, log_mess_arr);
				  double combined_score = 0.0;
				  
				  String insert_str = "insert into "+ score_table + "  values("+ bugid+","+ revid+","+ revid_size_score+ ","+ title_log_sim_score+","+desc_log_mess_score+","+combined_score+")";
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

   // This will be used to combine the scores calcuated by individual componenet
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

