
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

 
public class download_bug_complete_report_data 
  {

	private String project = "chromium_";
    private String url = "jdbc:mysql://localhost:3306/";
    private String dbName ="regression1" ;
    private String driver = "com.mysql.jdbc.Driver";
    private String userName = "root";
    private String password = "1234";
    private String TABLE = "chromeDB_all_simple";
    private String bugid_table = project  +"bugid_reg_revids";
    
    private ProjectHostingService myService = null;
    private Connection conn = null;
    
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
try {
if(conn!=null) 
conn.close();
} catch (Exception e) {
e.printStackTrace();
}
} 
private void insert(int issueID, String state, String status, Timestamp reported, Timestamp closed, String owner, String title, String description, String area, String type,  double timediffhrs,  int numcomments, String comments){
//title = "title";
//description="desc";
//comments = "";
String insertString = "insert into " + TABLE + " VALUES (" + issueID + ",'" + state + "','" + status + "','" + reported + "','" + closed + "','" + owner + "','" + title + "','" + description +
"','"+ comments+"','" + area + "','" + type + "',"+ timediffhrs +","  + numcomments + ")";
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
public String getArea(List<Label> labels){
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
  
  public String getFeature(List<Label> labels){
    String result = "";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.contains("Feature-")){
        result = label.substring(label.indexOf("Feature-")+8, label.length());
        //System.out.println("Area : " + label + " : " + result); 
      } 
    }  
    return result;
  }
  
  public String getSecSeverity(List<Label> labels){
    String result = "";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.contains("SecSeverity")){
        result = label.substring(label.indexOf("SecSeverity-")+12, label.length());
        //System.out.println("Area : " + label + " : " + result); 
      } 
    }  
    return result;
  }
  
  public String getSecurity(List<Label> labels){
    String result = "0";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.equalsIgnoreCase("Security") || label.equalsIgnoreCase("Type-Security")){
        result = "1";
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
  
  public String getCleanup(List<Label> labels){
    String result = "0";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.equalsIgnoreCase("Cleanup") || label.equalsIgnoreCase("Type-Cleanup")){
        result = "1";
      } 
    }  
    return result;
  }
  
  public String getPerformance(List<Label> labels){
    String result = "0";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.equalsIgnoreCase("Performance") || label.equalsIgnoreCase("Type-Performance") || label.equalsIgnoreCase("Stability-Performance")){
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
  
  public String getUsability(List<Label> labels){
    String result = "0";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.equalsIgnoreCase("Usability") || label.equalsIgnoreCase("Type-Usability") || label.equalsIgnoreCase("Stability-Usability")){
        result = "1";
      } 
    }   
    return result;
  }
  
  public String getPolish(List<Label> labels){
    String result = "0";
    for(int i=0;i<labels.size();i++){
      Label l = labels.get(i);
      String label = l.getValue();
      //System.out.println("Label : " + label);
      if(label.equalsIgnoreCase("Polish") || label.equalsIgnoreCase("Type-Polish") || label.equalsIgnoreCase("Stability-Polish")){
        result = "1";
      } 
    }   
    return result;
  }
  
  public void printAllIssueComments(String IssueId) {
    try{
        URL feedUrl = new URL("https://code.google.com/feeds/issues/p/" + project + "/issues/" + IssueId + "/comments/full");
        IssueCommentsFeed resultFeed = myService.getFeed(feedUrl, IssueCommentsFeed.class);

        for (int i = 0; i < resultFeed.getEntries().size(); i++) {
          IssueCommentsEntry entry = resultFeed.getEntries().get(i);
       
          TextContent textContent = (TextContent) entry.getContent();
          if (textContent != null && textContent.getContent() != null) {
            HtmlTextConstruct htmlConstruct = (HtmlTextConstruct) textContent.getContent();
            System.out.println("\t" + htmlConstruct.getHtml());
          }
        }
        System.out.println();
    }catch(Exception e){
      System.out.println(e);
    }
  }
  
  public String getIssueComments(String IssueId)
  {
    int result = 0;
String IssueComments= "";

try{
	URL feedUrl = new URL("https://code.google.com/feeds/issues/p/" + project + "/issues/" + IssueId + "/comments/full");
        ///new
        IssuesQuery myQuery = new IssuesQuery(feedUrl);
        myQuery.setMaxResults(10000);
        IssueCommentsFeed resultFeed = myService.getFeed(myQuery, IssueCommentsFeed.class);
        ///new
        
        
       //@@NOT A COOMEN/ IssueCommentsFeed resultFeed = myService.getFeed(feedUrl, IssueCommentsFeed.class);
        result = resultFeed.getEntries().size();
       
              
        for (int i = 0; i < resultFeed.getEntries().size(); i++) {
          
          System.out.println("\n======================= i ="+(i+1)+"\n");
            IssueCommentsEntry entry = resultFeed.getEntries().get(i);
          
            TextContent textContent = (TextContent) entry.getContent();
          if (textContent != null && textContent.getContent() != null) 
             {
              HtmlTextConstruct htmlConstruct = (HtmlTextConstruct) textContent.getContent();
             // System.out.println("\t" + htmlConstruct.getHtml());
              IssueComments=IssueComments+htmlConstruct.getHtml()+"\n";
             }//if
          
           }//for      
        
        
    }catch(Exception e){
      System.out.println(e);
    }
    
    System.out.println("All Comments = "+ IssueComments);
    System.out.println("\n=======================\n");
    return IssueComments;
    
  }//fun  
  
    
  
  public int numIssueComments(String IssueId) 
  {
    int result = 0;
    try{
        URL feedUrl = new URL("https://code.google.com/feeds/issues/p/" + project + "/issues/" + IssueId + "/comments/full");
       
        ///new
        IssuesQuery myQuery = new IssuesQuery(feedUrl);
        myQuery.setMaxResults(10000);
        IssueCommentsFeed resultFeed = myService.getFeed(myQuery, IssueCommentsFeed.class);
        
        ///new
               
       //@@NOT A COOMEN/ IssueCommentsFeed resultFeed = myService.getFeed(feedUrl, IssueCommentsFeed.class);
        result = resultFeed.getEntries().size();
        for (int i = 0; i < resultFeed.getEntries().size(); i++) {
          
          System.out.println("\n======================= i ="+(i+1)+"\n");
          IssueCommentsEntry entry = resultFeed.getEntries().get(i);
          
          TextContent textContent = (TextContent) entry.getContent();
          if (textContent != null && textContent.getContent() != null) {
            HtmlTextConstruct htmlConstruct = (HtmlTextConstruct) textContent.getContent();
            System.out.println("\t" + htmlConstruct.getHtml());
          }//if
          
          System.out.println("\n=======================\n");
        }
        System.out.println();
        
    }catch(Exception e){
      System.out.println(e);
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
      //System.out.println("KIND : " + entry.getKind());
      //System.out.println(entry.getTextContent().getContent().getPlainText());
      //System.out.println("State : " + entry.getState().getValue().name());
      //System.out.println("Status : " + entry.getStatus().getValue());
      //System.out.println("Get Published : " + entry.getPublished());
      //System.out.println("Stars : " + entry.getStars());
      //System.out.println("Closed Date : " + entry.getClosedDate());
      //System.out.println("ISSUE ID : " + issueID);
      //System.out\.println("OWNER : " + entry.getOwner().getUsername().getValue());
      //System.out.println(entry.getVersionId()); 
        //System.out.println(entry.getTitle().getPlainText());
        //System.out.println("-------------------------------------------------------------");
       
       // if(state.equalsIgnoreCase("CLOSED")){
         //if( (status.equalsIgnoreCase("Fixed")) || (status.equalsIgnoreCase("Verified")) || (status.equalsIgnoreCase("Duplicate"))){
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
             
            List<Person> authors = entry.getAuthors();
            Object[] authors_o = authors.toArray();
            for(int i=0;i<authors_o.length;i++){
              Person p = (Person)authors_o[i];
              //System.out.println(p.getName() + " : " + p.getUri());
              System.out.println("REPORTER NAME : " + p.getName());
              System.out.println("REPORTER URI : " + p.getUri());
            }
            
            System.out.println("BLOCKEDONS : " + entry.getBlockedOns().size());
            System.out.println("BLOCKINGS : " + entry.getBlockings().size());
            System.out.println("NUMCC : " + entry.getCcs());
            
            
            String owner = "";
            if(entry.getOwner() != null){
              owner = entry.getOwner().getUsername().getValue();
              
            }
            
            
            System.out.println("OWNER : " + owner);
            
            String title = entry.getTitle().getPlainText();
            title = title.replaceAll("'", ""); 
            System.out.println("TITLE : " + title);  
            
            String description = entry.getTextContent().getContent().getPlainText();
            //System.out.println("DESCRIPTION : " + description);
            description = description.replaceAll("'", "");
            String area = getArea(labels);
            System.out.println("AREA : " + area);
            String type = getType(labels);
            System.out.println("TYPE : " + type);
            String pri = getPri(labels);
            System.out.println("PRI : " + pri);
            String feature = getFeature(labels);
            System.out.println("FEATURE : " + feature); 
            String secSeverity = getSecSeverity(labels);
            System.out.println("SECSEVERITY : " + secSeverity);
            
            String security = getSecurity(labels);
            System.out.println("SECURITY : " + security);
             
            String regression = getRegression(labels);
            System.out.println("REGRESSION : " + regression);
            
            String performance = getPerformance(labels);
            System.out.println("PERFORMANCE : " + performance);
            
            String cleanup = getCleanup(labels);
            System.out.println("CLEANUP : " + cleanup);
            
            String polish = getPolish(labels);
            System.out.println("POLISH : " + polish);
            
            String usability = getUsability(labels);
            System.out.println("USABILITY : " + usability);
            
            String crash = getCrash(labels);
            System.out.println("CRASH : " + crash);
            
            int stars = entry.getStars().getValue().intValue();
            System.out.println("STARS : " + stars); 
            
            int numIssueComments = numIssueComments(issueId);
            System.out.println("NUM ISSUE COMMENTS : " + numIssueComments); 
            
            String IssueComments = getIssueComments(issueId);
            System.out.println("*************************************************************");
            
            /*description = pobj.clean(description);//@NoT A COMMENT
            title = pobj.clean(title);
            IssueComments = pobj.clean(IssueComments);*/
            description = description.replaceAll("[,\'\" \n]", " ");
            title = title.replaceAll("[,\'\n\"]", " ");
            IssueComments = IssueComments.replaceAll("[,\'\" \n]", " ");
            
            System.out.println("Title="+title);
            System.out.println("DES="+description);
            System.out.println("Title="+IssueComments);
                       
            
            insert(issueID, state, status, reported, closed, owner, title, description, area, type, diff, numIssueComments, IssueComments); 
            //(issueID,  state, status, reported, closed, owner,  title,  description,  area,  type, imediffhrs,numcomments, comments){
                
         
       //}if
       // }if
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
      
     String bugid_str = "select bugid from "+  bugid_table;
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
  
  public void printAllIssues(ProjectHostingService myService, String project){
    try{
      URL feedUrl = new URL("https://code.google.com/feeds/issues/p/" + project + "/issues/full");
      IssuesFeed resultFeed = myService.getFeed(feedUrl, IssuesFeed.class);
      for (int i = 0; i < resultFeed.getEntries().size(); i++) {
        IssuesEntry entry = resultFeed.getEntries().get(i);
        System.out.println("-------------------------------------------------------------");
        System.out.println("\t" + entry.getId());
          System.out.println("\t" + entry.getTitle().getPlainText());
          System.out.println("-------------------------------------------------------------");
      }
      System.out.println();
    }catch(Exception e){
      System.out.println(e);
    }
  } 

public static void main(String[] args){
	download_bug_complete_report_data ite = new download_bug_complete_report_data();
	ite.initdb();
ite.process();
ite.closedb();
}
}

