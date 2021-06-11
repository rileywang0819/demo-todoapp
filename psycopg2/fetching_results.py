import psycopg2

# Establish a connection, starting a session, begins a transaction
conn = psycopg2.connect('dbname=example user=postgres password=pupu0819')
# Set a cursor to begin executing commands
cursor = conn.cursor()

# Open a cursor to perform database operations
cur = conn.cursor()

# Drop to table if it already exited
cur.execute('DROP TABLE IF EXISTS table2;')
# cur.rollback()

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cur.execute("""
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
""")


# 2 ways to compose SQL query using strings:
# 1. use tuple
cur.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))
# 2. use dictionary
SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'
data = {
    'id': 2, 
    'completed': False
}
cur.execute(SQL, data)

cursor.execute('SELECT * FROM table2;')

""" How to fetch the result? """
# 1
result = cursor.fetchall()
print(result)  # --> [(1, True), (2, False)]
# 2
print(cursor.fetchmany(3))
# 3
print(cursor.fetchone())  # fetches the first result in the result sets

# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()