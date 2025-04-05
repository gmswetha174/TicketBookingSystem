import mysql.connector

class DBConnUtil:
    @staticmethod
    def get_db_connection():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="TicketBookingSystem"
            )
            if conn.is_connected():
                print("✅ Connection Successful!")
            return conn
        except mysql.connector.Error as err:
            print(f"❌ Error: {err}")
            return None

# Run the connection check
if __name__ == "__main__":
    conn = DBConnUtil.get_db_connection()
    if conn:
        conn.close()