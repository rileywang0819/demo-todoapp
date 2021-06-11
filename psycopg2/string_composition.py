import psycopg2

conn = psycopg2.connect('dbname=example user=postgres password=pupu0819')

# Open a cursor to perform database operations
cur = conn.cursor()

# Drop table if it already exited
cur.execute('DROP TABLE IF EXISTS table2;')

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

# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()