package regression1;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import com.google.gdata.client.projecthosting.ProjectHostingService;

/*
 * This will be used to compute the effectiveness of proposed approach
 * */
public class compute_metrics 
{
 
  private double precision;
  private double map;
  
 /* 
  private String url = "jdbc:mysql://localhost:3306/";
  private String dbName ="regression1" ;
  private String driver = "com.mysql.jdbc.Driver";  
  private String userName = "root";
  private String password = "1234";
  private String project = "chromium"; */
  
  private String url = "jdbc:mysql://localhost:3307/";
  private String dbName ="regression1" ;
  private String driver = "com.mysql.jdbc.Driver";  
  private String userName = "sangeetal";
  private String password = "sangeetal";
  private String project = "chromium";
  
  
  private int top10 = 10; 
  private int top20 = 20;  
  private int top30 = 30;  
  /*
  private String userName = "sangeetal";
  private String password = "sangeetal";
 
   * */
  private String bugid_table = project  +"_bugid_previous_30day_revids";
  private String  score_table = project + "_score_table";
  
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

private void compute_precision(int k)
{
	Statement stmt =  null;
	String select_str= "select distinct bugid from  "+ bugid_table;
	int total_count = 0;
	int reg_causing_match = 0;
	try 
	  {
		  stmt =  conn.createStatement();
		  stmt.executeQuery(select_str);		  
		  ResultSet rs =  stmt.getResultSet();
		  
		  while(rs.next())
		  {
			  int bugid =  rs.getInt("bugid");
			  total_count ++;
			  
			  String revid_str =  "select revid from " + bugid_table + " where bugid="+ bugid+" and reg_causing = 1";
			 // System.out.println (" revid str = "+revid_str);
			 
			  Statement stmt2 = conn.createStatement();
			  stmt2.execute(revid_str) ;
			  ResultSet rs2 =  stmt2.getResultSet();
			  int reg_causing_revid = 0;
			  
			  while(rs2.next())
			  {
				  reg_causing_revid =  rs2.getInt("revid");
				  
			  }
			  			  
			  String  get_ranked_revid =  "select revid , combined_score   from "  + score_table + " where bugid= "+ bugid +" order by combined_score desc limit 0,"+k;
			  stmt2.execute(get_ranked_revid);
			  rs2  =  stmt2.getResultSet();
			  //System.out.println(" ranked = "+ get_ranked_revid) ;
			  
			  boolean flag=  false;
			  double min_combined_score  = 0.0;  // This will be used in casemore than two revids have same score and one is not occuring just because we are extracting only top k 
			  while(rs2.next())
			  {
				  int temp_revid = rs2.getInt("revid");
				  min_combined_score = rs2.getDouble("combined_score");
				  if(temp_revid == reg_causing_revid)
				  {
					  flag = true;
					  break;
				  }
			  }
			  
			  if(flag==false)
			  {
				  //Is any other revid with that score exists
				  
				  String  get_other_revids = "select revid  from "+ score_table + " where bugid =  "+ bugid + " and combined_score = "+ min_combined_score;
				 // System.out.println(" ranked = "+ get_other_revids) ;
				  stmt2.execute(get_other_revids);
				  rs2 = stmt2.getResultSet();
				  while(rs2.next())
				  {
					  int temp_revid = rs2.getInt("revid");
					  if(temp_revid == reg_causing_revid)
					   {
						  flag = true;
						  break;
					   }
				  }
			  }
			  
			  if(flag==true)
			  {
				  reg_causing_match++;
			  }
			  
			 /* else @For debugging
			  {
				  System.out.println("false flag bugid="+ bugid);
			  }*/
			  rs2.close();
			  stmt2.close();
		  }
		  
		  rs.close();
		  stmt.close();
	   
	  } catch (SQLException e) 
	    {
		   e.printStackTrace();
	    }
	
	
	precision =  (reg_causing_match *100)/total_count;	
	System.out.println(" Precision for Top "+ k+" =  "+precision);
} 
public static void main(String args[])
  {
	  compute_metrics cm =  new compute_metrics();
	  cm.initdb();
	  cm.compute_precision(cm.top10);
	  cm.closedb();
	  
	  
  }


  
}
