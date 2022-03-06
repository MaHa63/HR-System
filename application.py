from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

# For Elastic Beanstalk
application = app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
db = SQLAlchemy(app)

class Gender(Enum):
    male   = 1
    female = 2


class Employee(db.Model):
    id         = db.Column(db.Integer,    primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name  = db.Column(db.String(25), nullable=False)
    gender     = db.Column(db.Integer,    nullable=False)
    birth_date = db.Column(db.DateTime)
    hire_date  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    """ if request.method == 'POST':
        fn  = request.form['first_name']
        ln  = request.form['last_name']
        gnd = request.form['gender']
        print(gnd)
        new_employee = Employee(first_name=fn, last_name=ln, gender=gnd)

        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding new employee'
    else:
        employees = Employee.query.order_by(Employee.hire_date).all()
        return render_template('index.html', employees=employees) """
    employees = Employee.query.order_by(Employee.hire_date).all()
    return render_template('index.html', employees=employees)

@app.route('/delete/<int:id>')
def delete(id):
    employee_to_delete = Employee.query.get_or_404(id)

    try:
        db.session.delete(employee_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        employee.first_name  = request.form['first_name']
        employee.last_name  = request.form['last_name']
        employee.gender = request.form['gender']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task' 

    else:
        return render_template('update.html', employee=employee)


@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        fn  = request.form['first_name']
        ln  = request.form['last_name']
        gnd = request.form['gender']
        print(gnd)
        new_employee = Employee(first_name=fn, last_name=ln, gender=gnd)
        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding new employee'
    else:
         return render_template('create.html')

@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)