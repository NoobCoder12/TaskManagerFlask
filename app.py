from flask import Flask, render_template, request, redirect
from logic.task_manager import TaskManager
import os


app = Flask(__file__)
manager = TaskManager()
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_name = request.form.get('content')
        if task_name:
            manager.add_task(task_name)

        return redirect('/')
    
    tasks = manager.task_list
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<task_name>')
def remove_task(task_name):
    manager.remove_from_list(task_name)
    return redirect('/')

@app.route('/update/<task_name>', methods=['GET', 'POST'])
def update_task(task_name):
    manager.complete_task(task_name)
    return redirect('/')

@app.route('/save/', methods=['GET', 'POST'])
def save_list():
    if manager.task_list:
        manager.save_list()
        flash('List was saved.', 'success')
        return redirect('/')
    else:
        flash('Cannot save list - add a task first.', 'error')
        return redirect('/')


@app.route('/load/', methods=['GET', 'POST'])
def load_list():
    manager.load_list()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
