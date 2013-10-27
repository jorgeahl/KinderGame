import java.sql.*;
import java.io.PrintWriter;
import java.io.File;

class login
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
			Connection con = DriverManager.getConnection(connectString, user, password);
			Statement stmt = con.createStatement();

			ResultSet rs = stmt.executeQuery("SELECT * FROM login");

			File file = new File ("login.txt");
			PrintWriter writer = new PrintWriter("login.txt", "UTF-8");
			String s = " ";
			
			while (rs.next())
			{
				writer.println(rs.getString("user") + s +  rs.getString("password"));
			}
			
			writer.close();
			
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
