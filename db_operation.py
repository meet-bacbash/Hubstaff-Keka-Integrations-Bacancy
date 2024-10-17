import sqlite3

# Step 1: Connect to the SQLite database (creates the DB if it doesn't exist)
connection = sqlite3.connect('db.sqlite3')

# Step 2: Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Step 3: Create a table (if it doesn't exist already)
cursor.execute('''
CREATE TABLE IF NOT EXISTS queue_count (
    id INTEGER PRIMARY KEY,
    count_value INTEGER
)
''')

# Step 4: Commit the changes
connection.commit()

# Step 5: Optionally, insert some data into the table
# cursor.execute('''
# INSERT INTO users("name","email","keka_id","hubstaff_id")
# VALUES ("Sanjay Sheladiya","sanjay.sheladiya@bacancy.com","11010","689824");
# ''')

# Commit after inserting data
# connection.commit()

# Step 6: Close the connection
connection.close()

print("Database created successfully!")
