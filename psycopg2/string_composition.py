import psycopg2

conn = psycopg2.connect('dbname=example user=postgres password=xxxxxxxx')

# Open a cursor to perform database operations
cur = conn.cursor()

# Drop table if it already exited
cur.execute('DROP TABLE IF EXISTS table1;')

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

# 2. use dictionary
SQL = 'INSERT INTO table1 (id, completed) VALUES (%(id)s, %(completed)s);'
data = {
    'id': 3, 
    'completed': False
}
cur.execute(SQL, data)

# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()