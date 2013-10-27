import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
 
 
/**
 * The SimpleConnection class is a command line application that accepts 
 * the following command line:
 * java SimpleConnection DRIVER URL UID PASSWORD 
 * If the URL fits the specified driver, it will then load the driver and
 * get a connection.
 */
public class SimpleConnection 
{
	static public void main(String args[]) 
	{
		Connection connection = null;
	 
		// Process the command line
		if( args.length != 4 ) 
		{
			System.out.println("Syntax: java SimpleConnection " + "DRIVER URL UID PASSWORD");
			return;
		}
		try 
		{ 
			// load the driver 
			Class.forName(args[0]);
		}
		catch( Exception e ) 
		{ 
			// problem loading driver, class not exist?
			e.printStackTrace();
			return;
		}
		try 
		{
		  connection = DriverManager.getConnection(args[1], args[2], args[3]);
		  System.out.println("Connection successful!");
		  // Do whatever queries or updates you want here!!!
		}
		catch( SQLException e ) 
		{
		  e.printStackTrace();
		}
		finally 
		{
			try 
			{
				connection.close();
			}
			catch( SQLException e ) 
			{
				e.printStackTrace();
			}
		}
	}
}
