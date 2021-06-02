from flask import Flask, json, render_template, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:pupu0819@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # link SQLAlchemy to the app

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}, {self.description}>'

# db.create_all()

# controller listens to the view '/todos/create'
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description, completed=False)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # jsonify:return json data to the client
        return jsonify(body)
    else:
        # raise an HTTPException
        abort(400)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        print('completed:', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return redirect(url_for('index'))
    else:
        abort(400)

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
        

@app.route('/')
def index():
    # Jinja2 as the template engine
    return render_template('index.html', todos=Todo.query.order_by('id').all())

if __name__ == '__main__':
    app.run(debug=True)