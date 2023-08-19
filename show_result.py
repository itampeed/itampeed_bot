import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySqlpassword@77890",
    database="quiz_app"
)

mycursor = mydb.cursor()

# Retrieve user marks and results from the user_marks table
select_marks_query = "SELECT username, marks, result FROM user_marks"
mycursor.execute(select_marks_query)
user_marks_data = mycursor.fetchall()

# Display user marks and results
print("Username\tMarks\tResult")
print("----------------------------")
for username, marks, result in user_marks_data:
    print(f"{username}\t{marks}\t{result}")

mycursor.close()
mydb.close()
