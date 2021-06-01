from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Jinja2 as the template engine
    return render_template('index.html', todos=[{
        'description': 'Todo 1'
    }, {
        'description': 'Todo 2'
    }, {
        'description': 'Todo 3'
    }])

if __name__ == '__main__':
    app.run(debug=True)