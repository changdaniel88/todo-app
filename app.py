from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

# Initializ Database
db = SQLAlchemy(app)

# Create Model


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Nullable means you cannot put an empty task in the Todo App
    task = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "< Task % r >", self.id


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(task=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Problem adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_added).all()  # fetching all data
        return render_template('index.html', title="Todo App", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem in deleting your task"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.task = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating your task"
    else:
        return render_template('update.html', task=task, title="update")


if __name__ == "__main__":
    app.run(debug=True)
