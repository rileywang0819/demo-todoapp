from threading import active_count
from flask import Flask, json, render_template, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

from sqlalchemy.orm import backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:pupu0819@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # link SQLAlchemy to the app

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
    # list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True)

    def __repr__(self):
        return f'<Todo ID: {self.id}, description: {self.description}, complete: {self.complete}>'

# db.create_all()

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList ID: {self.id}, name: {self.name}, todos: {self.todos}>'


# controller listens to the view '/todos/create' : create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, completed=False, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


# controller listens to the view '/todos/<todo_id>/set-complete' : set todo completed
@app.route('/todos/<todo_id>', methods=['POST'])
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
        abort(500)
    else:
        return redirect(url_for('index'))



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
    if not error:
        # return redirect(url_for('index'))  # 405 error
        ''' either is ok '''
        return jsonify({'success': True})
        # return render_template('index.html', data=Todo.query.order_by('id').all())


# controller listens to the view '/lists/create' : create a new todo-list
@app.route('/lists', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name, completed=False)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
        body['completed'] = todolist.completed
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)  # raise an HTTPException
    else:
        return jsonify(body)   # jsonify:return json data to the client


# controller listens to the view '/lists/<list_id>/set-completed' : set todo-list completed
@app.route('/lists/<list_id>', methods=['POST'])
def set_completed_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        completed = request.get_json()['completed']
        print('completed: ', completed)
        list.completed = completed
        for todo in list.todos:
            todo.completed = True
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        # return redirect(url_for('index'))
        return jsonify({'completed': completed})


# controller listens to the view '/lists/<list_id>/delete' : delete the todo-list with list_id
@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)
        db.session.delete(list)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    # Jinja2 as the template engine
    return render_template('index.html', 
    lists=TodoList.query.all(),
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())

if __name__ == '__main__':
    app.run(debug=True)