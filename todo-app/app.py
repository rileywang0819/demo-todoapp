from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:pupu0819@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # link SQLAlchemy to the app

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}, {self.description}>'

db.create_all()

# controller listens to the view '/todos/create'
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # jsonify:return json data to the client
        return jsonify({
            'description': todo.description
        })
    else:
        # raise an HTTPException
        abort(400)

@app.route('/')
def index():
    # Jinja2 as the template engine
    return render_template('index.html', todos=db.session.query(Todo).all())

if __name__ == '__main__':
    app.run(debug=True)