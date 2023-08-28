from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

        
@app.route('/', methods=['POST', 'GET'])

def index():
    
    if request.method == 'POST':
        task_content = request.form['content'] #JUST THE INPUT
        new_task = Todo(content=task_content) # NEW_TASK HAS ID, CONTENT AND DATE_CREATED
        if new_task.content == '': #NULLABLE DIDNT WORK, HAD TO DO THIS
            return 'You cant add a NULL value'
        try:
            db.session.add(new_task)
            db.session.commit() # COMMITING THE DATA
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # RETURN ALL DATA ORDERED BY DATE
        return render_template('index.html', tasks=tasks)

    
@app.route('/delete/<int:id>') #CREATING DELETE ROUTE

def delete(id):
    task_to_delete = Todo.query.get_or_404(id) 

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') #ALWAYS GOTTA GO BACK HOME WHEN U FINISH SHIT LIKE THAT
    
    except:
        return 'There was a problem deleting your task'

@app.route('/update/<int:id>', methods=['GET','POST']) #UPDATE ROUTE

def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error updating your task'
    else:
        return render_template('update.html', task=task)



if __name__ == '__main__':
    app.run(debug=True)
