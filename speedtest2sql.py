import os
import subprocess
import json
import mysql.connector

# Speedtest command
command = "speedtest --json"

# Run speedtest and parse output
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

# Convert the output to JSON
data = json.loads(output)

# Connect to the database
db = mysql.connector.connect(
    host= "localhost",
    user= "speedtester",
    password= "sp33dt#st",
    database= "speedtest"
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    download DOUBLE,
    upload DOUBLE,
    ping DOUBLE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Insert data into the database
query = """
INSERT INTO tests (download, upload, ping)
VALUES (%s, %s, %s)
"""
values = (data["download"], data["upload"], data["ping"])
cursor.execute(query, values)

# Commit the transaction
db.commit()

# Close the connection
cursor.close()
db.close()
