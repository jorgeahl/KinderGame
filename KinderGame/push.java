import java.sql.*;

class push
{
	public static void main(String[] args)
	{
		String driver = "org.postgresql.Driver";
		String connectString = "jdbc:postgresql://c3.east1.stormdb.us:5432/k1382186238?ssl=0n";
		String user = "admin";
		String password = "baconPancakes#12345";

		try
		{
			Class.forName(driver);
			Connection con = DriverManager.getConnection(connectString, user , password);
			Statement stmt = con.createStatement();
			stmt.executeQuery("INSERT INTO answers VALUES ( "+args[0]+", "+args[1]+", "+args[1]+")");
			stmt.close();
			con.close();
		}
		catch( Exception e )
		{
			System.out.println("there was an error");
			System.out.println(e.getMessage());
			System.out.println("that was it");
			
		}
	
	}
}
