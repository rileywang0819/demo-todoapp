import psycopg2

# Establish a connection, starting a session, begins a transaction
conn = psycopg2.connect('dbname=example user=postgres password=xxxxxxxx')
# Set a cursor to begin executing commands
cursor = conn.cursor()

# Open a cursor to perform database operations
cur = conn.cursor()

# Drop to table if it already exited
cur.execute('DROP TABLE IF EXISTS table1;')
# cur.rollback()

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cur.execute("""
  CREATE TABLE table1 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
""")


# 2 ways to compose SQL query using strings:
# 1. use tuple
cur.execute('INSERT INTO table1 (id, completed) VALUES (%s, %s);', (1, True))
cur.execute('INSERT INTO table1 (id, completed) VALUES (2, false);')
cur.execute('INSERT INTO table1 (id, completed) VALUES (3, false);')
cur.execute('INSERT INTO table1 (id, completed) VALUES (4, false);')

# 2. use dictionary
SQL = 'INSERT INTO table1 (id, completed) VALUES (%(id)s, %(completed)s);'
data = {
    'id': 5, 
    'completed': False
}
cur.execute(SQL, data)

cur.execute('SELECT * FROM table1;')


""" How to fetch the result? """
# 1
print('.fetchone:', cur.fetchone())  # fetches the first result in the result sets


# 2
print('.fetchmany(2):', cur.fetchmany(2))

# 3
results = cur.fetchall()
# print(results)  # --> [(1, True), (2, False)]
for result in results:
  print('Print by line:', result)


# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()