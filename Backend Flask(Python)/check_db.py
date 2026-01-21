import mysql.connector

# Database settings same as your webhook
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fyp_chatbot_db'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Check columns in 'courses' table
    cursor.execute("DESCRIBE courses")
    columns = cursor.fetchall()
    
    print("\n--- TUMHARE 'COURSES' TABLE KE COLUMNS ---")
    for col in columns:
        print(col[0])  # Prints column name
    print("------------------------------------------\n")

    conn.close()
except Exception as e:
    print("Error:", e)