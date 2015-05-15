
package regression1;
import com.google.gdata.client.projecthosting.*;
import com.google.gdata.data.*;
import com.google.gdata.data.projecthosting.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.Timestamp;
import java.util.List;


//@Uses: This will download the bug report features only 
public class download_bug_feature_report_data 
  {


    private String dbName ="regression1" ;
    private String driver = "com.mysql.jdbc.Driver";
      
    private ProjectHostingService myService = null;
    private Connection conn = null;
    
    private String project = "chromium";
    /*
    private String url = "jdbc:mysql://localhost:3306/";
    private String userName = "root";
    private String password = "1234";
    //*/
    
    ///*
    private String url = "jdbc:mysql://localhost:3307/";
    private String userName = "sangeetal";
    private String password = "sangeetal";
    //*/
    private String TABLE =project+ "_bug_report_features";
    private String bugid_table = project  +"_bugid_previous_30day_revids";
  //  private preprocess pobj =  new preprocess();

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

private void closedb(){ 
try 
  {
     if(conn!=null) 
     conn.close();
   } catch (Exception e)
  {
    e.printStackTrace();
  }
} 

 
private void insert(int issueID, String state, String status, Timestamp reported, Timestamp closed,  String title, String description, String area, String cr, String type,  double timediffhrs)
{
//title = "title";
//description="desc";
//comments = "";
String insertString = "insert into " + TABLE + " VALUES (" + issueID + ",'" + state + "','" + status + "','" + reported + "','" + closed + "','" +  title + "','" + description +
"','"+ area +"','"+cr + "','" + type + "',"+ timediffhrs  + ")";

System.out.println("Insert String:="+insertString); 
try {
Statement stmt = conn.createStatement();
stmt.executeUpdate(insertString);
stmt.close();
} catch(Exception e) {
System.out.println(e);
e.printStackTrace();
//interupt();
}
}

public String getArea(List<Label> labels)
{
String result = "";
for(int i=0;i<labels.size();i++){
Label l = labels.get(i);
String label = l.getValue();
//System.out.println("Label : " + label);
if(label.contains("Area")){
result = label.substring(label.indexOf("Area-")+5, label.length());
//System.out.println("Area : " + label + " : " + result); 
} 
}  
return result;
}

public String getPri(List<Label> labels){
String result = "";
for(int i=0;i<labels.size();i++){
Label l = labels.get(i);
String label = l.getValue();
//System.out.println("Label : " + label);
if(label.contains("Pri-")){
        result = label.substring(label.indexOf("Pri-")+4, label.length());
        //System.out.println("Area : " + label + " : " + result); 
      } 
    }  
    return result;
  }
  
  public String getType(List<Label> labels){
    String result = "";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.contains("Type-")){
        result = label.substring(label.indexOf("Type-")+5, label.length());
        //System.out.println("Area : " + label + " : " + result); 
      } 
    }  
    return result;
  }

public String getCr(List<Label> labels){
String result = "";
for(int i=0;i<labels.size();i++){
Label l = labels.get(i);
String label = l.getValue();
//System.out.println("Label : " + label);
if(label.contains("Cr-")){
        result = label.substring(label.indexOf("Cr-")+3, label.length());
        //System.out.println("Area : " + label + " : " + result); 
      } 
    }  
    return result;
  }
 
  
  public String getRegression(List<Label> labels){
    String result = "0";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.equalsIgnoreCase("Regression") || label.equalsIgnoreCase("Type-Regression")){
        result = "1";
      } 
    }  
    return result;
  }
    
  public String getCrash(List<Label> labels){
    String result = "0";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.equalsIgnoreCase("Crash") || label.equalsIgnoreCase("Type-Crash") || label.equalsIgnoreCase("Stability-Crash")){
        result = "1";
      } 
    }   
    return result;
  } 
  
  
public void extractInformation(ProjectHostingService service, String issueId){
  try{ 
      URL feedUrl = new URL("https://code.google.com/feeds/issues/p/chromium/issues/full/" + issueId);
      IssuesEntry entry = service.getEntry(feedUrl, IssuesEntry.class);
      
      System.out.println("-------------------------------------------------------------");
      Id id = entry.getIssueId();
      int issueID = id.getValue();
      List<Label> labels =  entry.getLabels();
      for(int i=0;i<labels.size();i++){
        Label l = labels.get(i);
        l.getValue();
        System.out.println("i="+labels.get(i));
      }
      //interupt();
      String state = entry.getState().getValue().name();
      String status = entry.getStatus().getValue();
     
       
        if(state.equalsIgnoreCase("CLOSED"))
          {
         if( (status.equalsIgnoreCase("Fixed")) || (status.equalsIgnoreCase("Verified")) || (status.equalsIgnoreCase("Duplicate")))
            {
            System.out.println("*************************************************************");
            System.out.println("ISSUE ID : " + issueID);
            System.out.println("STATE : " + state);
            System.out.println("STATUS : " + status);
            java.sql.Timestamp reported = new Timestamp(entry.getPublished().getValue());
            System.out.println("REPORTED : " + reported);
           
            java.sql.Timestamp closed = new Timestamp(entry.getClosedDate().getValue().getValue());
            System.out.println("CLOSED : " + closed);
            
            double diff = closed.getTime() - reported.getTime();
            System.out.println("TIME DIFFERENCE (NOR) : " + diff);
            
            diff = diff / (60 * 60 * 1000);
            System.out.println("TIME DIFFERENCE HOURS : " + diff);                    
            
            String title = entry.getTitle().getPlainText();
            title = title.replaceAll("'", ""); 
            System.out.println("TITLE : " + title);  
            
            String description = entry.getTextContent().getContent().getPlainText();
            //System.out.println("DESCRIPTION : " + description);
            description = description.replaceAll("'", "");
            String area = getArea(labels);
            System.out.println("AREA : " + area);
            
            String cr =  getCr(labels);
            System.out.println("Cr="+cr);
            
            String type = getType(labels);
            System.out.println("TYPE : " + type);           
         
        
            String regression = getRegression(labels);
            System.out.println("REGRESSION : " + regression);
                   
         
            System.out.println("*************************************************************");
            
            /*description = pobj.clean(description);//@NoT A COMMENT
            title = pobj.clean(title);
            IssueComments = pobj.clean(IssueComments);*/
            description = description.replaceAll("[,\'\" \n]", " ");
            title = title.replaceAll("[,\'\n\"]", " ");
           
             System.out.println("Title="+title);
            System.out.println("DES="+description);       
         
			insert(issueID, state, status, reported, closed, title, description, area, cr,  type, diff ); 
            //(issueID,  state, status, reported, closed, owner,  title,  description,  area, cr, type, imediffhrs)
       }//if
        }//if
    }catch(Exception e){
      System.out.println(e);
      //interupt();
    }
  }
      
  public void process()
  {
    try{
      myService = new ProjectHostingService("Sample Application");
      //printAllIssues(myService, project);
      
     String bugid_str = "select distinct bugid from "+  bugid_table;
     Statement stmt =  conn.createStatement();
     stmt.executeQuery(bugid_str);
      ResultSet result = stmt.getResultSet();
      while(result.next())
      {
    	  System.out.println("Results"+ result.getInt("bugid"));
    	  int bugid=  result.getInt("bugid");
    	 
    	  extractInformation(myService, Integer.toString(bugid)); 
      }
      
    }catch(Exception e){
      System.out.println(e);
    }
  }
  
  public void interupt()
  {
    
    BufferedReader br =  new BufferedReader(new InputStreamReader(System.in));
    System.out.println("Intr");
    try {
      br.readLine();
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    
  }
 
public static void main(String[] args){
	download_bug_feature_report_data ite = new download_bug_feature_report_data();
	ite.initdb();
ite.process();
ite.closedb();
}
}

