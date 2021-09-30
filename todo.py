
"""

todo.py
Name: Ademir Vila
ID: 2299217
Email: vila@chapman.edu
Course: CPSC 230
Section: 10
Date: 12/5/2017
Assignment: Final Assignment

This creates a "Todo List" web application, that a user can 
use to manage tasks to do. The application is intended to help users 
keep track of a to-do list, where they can:
-view all of their tasks
-add new active tasks
-mark active tasks as completed
-clear all completed tasks

Less than 80 characters per line
"""

import flask
import matplotlib.pyplot as plt 

app = flask.Flask(__name__)

@app.route('/')
def mainpage():
    try:
        with open('active.txt', 'r') as f:
            active = f.read().split('\n')
            active = [ t for t in active if t != '']
        with open('completed.txt','r') as f:
            completed = f.read().split('\n')
    except FileNotFoundError:
        active = []
        completed = []
    return flask.render_template_string('''   
    
    <title>ToDo List</title>
    <h1>ToDo List</h1>
    
    <form action="/add" method="post">
        Enter a task: <input name="task"> <br>
        <input type="submit" value="Add">
    </form>

    <h2>Tasks</h2>

    <form action="/complete" method = "post">
        {% for t in active %}
            <input type="radio" name="task" value="{{t}}"> {{t}} <br>
        {% endfor %}
    <input type ="submit" value = "Complete Task">
    </form>

    {% for t in completed %}
        <i>{{t}}</i> <br>
    {% endfor %}

    <form action="/clear" method="post">
        <input type="submit" value="Clear Completed">
    </form>

    <img src="/pie.png">
    ''', **locals())
    




@app.route ("/add", methods = ['POST'])
def add():
    new_task = flask.request.form['task']
    with open('active.txt', 'a') as f:
        f.write("%s\n" % (new_task))
    return flask.redirect(flask.url_for("mainpage"))

@app.route("/complete", methods = ["POST"])
def complete():
    if 'task' in flask.request.form:
        is_completed = flask.request.form['task']
        with open('active.txt', 'r') as f:
            complete = f.read()
            complete = complete.split('\n')
            complete = [t for t in complete if t != '']
            complete.remove(is_completed)
        with open("active.txt", 'w') as f:
            for i in complete:
                f.write(i + "\n")
            if 'task' in flask.request.form:
                with open ('completed.txt', 'a') as f:
                    f.write('%s\n' % is_completed)
        return flask.redirect(flask.url_for("mainpage"))
    else:
        return flask.redirect(flask.url_for('mainpage'))

@app.route('/clear', methods = ['POST'])
def clear():
    with open('completed.txt' , "w") as f:
        f.write('')
    return flask.redirect(flask.url_for('mainpage'))

@app.route ('/pie.png')
def chart():
    with open('active.txt', 'r') as f:
        is_active = f.read()
        is_active = is_active.split('\n')
        is_active = [t for t in is_active if t != '']
    with open('completed.txt', 'r') as f:
        done = f.read()
        done = done.split('\n')
        done = [t for t in done if t != '']
    plt.clf()
    plt.pie([len(is_active), len(done)], labels = ["Active", "Complete"])
    plt.axis('equal')
    plt.title("Tasks Chart")
    plt.savefig('pie_export.png')
    return flask.send_file('pie_export.png', cache_timeout=0)

app.run()