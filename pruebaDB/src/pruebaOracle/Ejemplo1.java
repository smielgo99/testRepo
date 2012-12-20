package pruebaOracle;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class Ejemplo1 {
	private Connection conexion = null;
    private PreparedStatement statement = null;

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		new Ejemplo1();

	}
	public Ejemplo1(){
		try{
			estableceConexion();
			
			//getAllUsers();
			//getUser(1);
			//getAllEntries();
			//getEntry(1);
			//getEntryUser(1);
			//getEntryUserJoin(2);
			//getComment();
			getCommentJoin(1, 4, 5);
		} catch (Exception e) {
			// TODO: handle exception
		} finally{
			closeConexion();
		}
	}
	
	public void estableceConexion(){
		try{
			Class.forName("oracle.jdbc.driver.OracleDriver");
			conexion=DriverManager.getConnection(
		        "jdbc:oracle:thin:@enviro-db:1521:ENVIRO",
		        "mibsprod",
		        "mibsprod");

		     
		} catch (Exception e) {
			e.printStackTrace();
		}

	}
	public void closeConexion(){
		try{
			statement.close();
			conexion.close();
		}catch (Exception e) {
			// TODO: handle exception
		}
	}
	public void truncate(){
		try {
			statement = conexion.prepareStatement("truncate table TEST_COMMENT drop storage");
			statement.executeQuery();
			statement = conexion.prepareStatement("truncate table TEST_ENTRY drop storage");
			statement.executeQuery();
			statement = conexion.prepareStatement("truncate table TEST_USER drop storage");
			statement.executeQuery();
		} catch (SQLException e) {
        	
        	
            e.printStackTrace();
        } 	
	}
	public void getAllUsers(){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_user");
	        }
	        
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 
	  /*      while (rs.next()) {
	            System.out.println("user_id=" + rs.getInt(1) + " msisdn="
	                    + rs.getString(2) + " nick=" + rs.getString(3)
	                    + " email=" + rs.getString(4)+ " score=" + rs.getString(5));
	        }*/
	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getAllUsers diffTotal "+diffTotal);
	        System.out.println("getAllUsers diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        closeConexion();
	    }
	}
	
	public void getUser(int id){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_user where user_id = ?");
	        }
	        statement.setInt(1, id);
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 
	        while (rs.next()) {
	            System.out.println("user_id=" + rs.getInt(1) + " msisdn="
	                    + rs.getString(2) + " nick=" + rs.getString(3)
	                    + " email=" + rs.getString(4)+ " score=" + rs.getString(5));
	        }
	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getUser diffTotal "+diffTotal);
	        System.out.println("getUser diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        
	    }
	}
	public void getAllEntries(){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_entry");
	        }
	        
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 
	  /*      while (rs.next()) {
	            System.out.println("user_id=" + rs.getInt(1) + " msisdn="
	                    + rs.getString(2) + " nick=" + rs.getString(3)
	                    + " email=" + rs.getString(4)+ " score=" + rs.getString(5));
	        }*/
	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getAllEntries diffTotal "+diffTotal);
	        System.out.println("getAllEntries diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        closeConexion();
	    }
	}
	public void getEntry(int id){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_entry where entry_id = ?");
	        }
	        statement.setInt(1, id);
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 

	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getEntry diffTotal "+diffTotal);
	        System.out.println("getEntry diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        
	    }
	}
	public void getEntryUser(int id){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_entry where user_id = ?");
	        }
	        statement.setInt(1, id);
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 

	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getEntryUser diffTotal "+diffTotal);
	        System.out.println("getEntryUser diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        
	    }
	}
	public void getEntryUserJoin(int id){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_entry e, test_user u where e.user_id = u.user_id and u.user_id = ?");
	        }
	        statement.setInt(1, id);
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 

	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getEntryUserJoin diffTotal "+diffTotal);
	        System.out.println("getEntryUserJoin diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        
	    }
	}
	public void getComment(){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_comment e");
	        }
	        
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 

	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getComment diffTotal "+diffTotal);
	        System.out.println("getComment diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        
	    }
	}
	public void getCommentJoin(int id, int id2, int id3){
		try {
			java.util.Date date_begin = null;
	        if (null == statement) {
	        	 date_begin = new java.util.Date(); 
	        	  

	            statement = conexion
	                    .prepareStatement("select * from test_entry e, test_comment c," +
	                    		"test_user u where c.user_id = u.user_id  and e.user_id = u.user_id and u.user_id in( ?, ?,?)");
	        }
	        statement.setInt(1, id);
	        statement.setInt(2, id2);
	        statement.setInt(3, id3);
	        ResultSet rs = statement.executeQuery();
	        java.util.Date date_get = new java.util.Date(); 

	        java.util.Date date_end = new java.util.Date(); 
	        long diffTotal = date_end.getTime() - date_begin.getTime();
	        long diffGet = date_get.getTime() - date_begin.getTime();
	        System.out.println("getCommentJoin diffTotal "+diffTotal);
	        System.out.println("getCommentJoin diffGet "+diffGet);
	        rs.close();
	        
	    } catch (SQLException e) {
	        e.printStackTrace();
	        
	    }
	}
	private void insertaPreparedStatement() {
		PreparedStatement ps;
        try {
        	System.out.println("insertando en test_user");
            ps = conexion
                    .prepareStatement("insert into test_user values (?,?,?,?,?)");
            for(int i=1; i<=2000; i++){
            	System.out.println("insertando en test_user" +i);
            	ps.setInt(1, i);
	            
	            String token = "user" + i;
	            
	            ps.setString(2, token);
	            ps.setString(3, token);
	            ps.setString(4, token);
	            ps.setString(5, token);
	            ps.executeUpdate();
	            
            }
            System.out.println("Commit test_user");
            conexion.commit();
            System.out.println("insertando en test_entry");
            ps = conexion
            .prepareStatement("insert into test_entry values (?,?,?,?,?)");
            for(int i=1; i<=2000; i++){
            	System.out.println("insertando en test_user" +i);
            	for(int j=1; j<=100; j++){
            		System.out.println("insertando en test_entry" +j);
            		ps.setInt(1, j);
		            String token = "entry" +j;
		            
		            ps.setInt(2, i);
		            ps.setString(3, token);
		            ps.setString(4, token);
		            ps.setInt(5, 1);
		            ps.executeUpdate();
		           
            	}
            	 System.out.println("Commit test_entry 1");
            	 conexion.commit();
            }
            System.out.println("Commit test_entry b");
            conexion.commit();
            System.out.println("insertando en test_comment");
            ps = conexion
            .prepareStatement("insert into test_comment values (?,?,?,?)");
            for(int i=1; i<=2000; i++){
            	System.out.println("insertando en test_user" +i);
            	for(int j=1; j<=100; j++){
            		System.out.println("insertando en test_entry" +j);
            		for(int k=1; j<=50; j++){
            			System.out.println("insertando en test_comment" +k);
			            String token = "comment" + k;
			            
			            ps.setString(1, token);
			            ps.setInt(2, j);
			            ps.setInt(3, i);
			            ps.setInt(3,k);
			            ps.executeUpdate();
            		}
            		 conexion.commit();
            		 System.out.println("Commit test_comment 1");
            	}
            	 conexion.commit();
            	 System.out.println("Commit test_comment 2");
            }
            conexion.commit();
            System.out.println("Commit test_comment 3");
            ps.close();
            conexion.close();
        } catch (SQLException e) {
        	
        	
            e.printStackTrace();
        } 
    }

}
