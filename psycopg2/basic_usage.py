import psycopg2

conn = psycopg2.connect('dbname=example user=postgres password=xxxxxxxx')

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS table1;')

# create the todos table
# (note: triple quotes allow multiline text in python)
cur.execute("""
  CREATE TABLE table1 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
""")

cur.execute('INSERT INTO table1 (id, completed) VALUES (1, true);')
cur.execute('INSERT INTO table1 (id, completed) VALUES (2, false);')

# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()