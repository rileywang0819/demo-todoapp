from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
db_info = 'postgresql://postgres:password@localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = db_info
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.completed}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

# db.create_all() don't use anymore since we use migration instead

""" Creates a new list. """
@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        new_list = TodoList(name=name)
        db.session.add(new_list)
        db.session.commit()
        body['name'] = new_list.name
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)

""" Sets list completed. """
@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def update_list(list_id):
    error = False
    try:
        completed = request.get_json()['completed']
        list = TodoList.query.get(list_id)
        list.completed = completed
        for todo in list.todos:

            todo.completed = completed
        db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        # return redirect(url_for('index'))
        return jsonify({'success': True})

""" Deletes list. """
@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        todos = list.todos
        for todo in todos:
            db.session.delete(todo)
        db.session.delete(list)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})

""" controller listens to the view '/todos/create' : creates a new todo """
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        desc = request.get_json()['description']
        list_id = request.get_json()['list-id']
        new_todo = Todo(description=desc, list_id=list_id)
        db.session.add(new_todo)
        db.session.commit()
        body['description'] = new_todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    if not error:
        # jsonify:return json data to the client
        return jsonify(body)

""" Sets todo completed. """
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def update_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        # return redirect(url_for('index'))
        return jsonify({'success': True})

""" Delete a todo item. """
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    error = False
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        # return redirect(url_for('index'))  # 405 error
        ''' either is ok '''
        return jsonify({'success': True})
        # return render_template('index.html', todos=Todo.query.order_by('id').all())

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('hp.html', 
    lists=TodoList.query.all(),
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())  # fix the ordering

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))
