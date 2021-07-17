from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# standard way for creating a flask application
app = Flask(__name__)

# connect to database from the Flask application by setting configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xxxxxxxx@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # db: instance of database

# inherit from db.Model enables us to map class to table
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)  # column constraints
    name = db.Column(db.String(), nullable=False)

    # useful for debugging: customized show
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

db.create_all()  # create table

@app.route('/')
def index():
    # person = Person.query.first()
    person = Person.query.filter(Person.name == 'chengcheng').first()
    return 'Hello ' + person.name

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()


"""
in terminal Python's interactive mode

~$ python

>>> from flask_hello_app import Person, db
>>> person = Person(name='rourou')
>>> db.session.add(person)
>>> db.session.commit()
>>> query = Person.query.all()
>>> print(query)
[<Person ID: 1, name: PuPu>, <Person ID: 2, name: chengcheng>, <Person ID: 3, name: rourou>]
"""