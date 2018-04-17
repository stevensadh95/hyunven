from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import tempfile
import os.path
from flask_login import LoginManager, login_user, login_required, logout_user,UserMixin


from forms import SignupForm


app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


app.secret_key = '2305thgwiovhewncry83ufcnnd0dci329yt8fbw'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.sqlite'


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username = username).first()

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

class User(db.Model,UserMixin):
    username = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username= username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return str(self.username)



@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/about')
def about(name=None):
    return render_template('about.html', name=name)

#Catalogue
#Variables
E4CYS_Table_Head = {'Engine Type':'4 Cycle, Vertical, Fresh Water Cooled Diesel Engine',
                    'No. of Cyl.':'4', 'Cylinder Bore x Stroke(mm)':'100x105',
                    'Engine Displacement(cc)':'3,298', 'Combustion Type':'Direct Injection',
                    'Fuel':'Diesel', 'Lub Oil Type':'API CD CLASS', 
                    'Cooling System':'Heat exchanger type forced circulating by centrifigal pump',
                    'Starting System':'DC 24V Electric Starting Type', 'Fuel Injection Pump':'BOSCH type with all speed control GOVERNOR', 'Standard Reduction Ratio':'1.64, 2.07, 2.52, 2.96, 3.32'}

E4CYS_Table_Models = {'E4CYS31':('70/2700', 'NA', '17.5', '360'), 'E4CYS31T':('100/2700', 'TC',                           '16.0', '368')}

E4CYS_Prices = {'E4CYS31':('$9,220', '$2,310', '$2,270', '$2,070', '$15,480'), 'E4CYS31T':('$10,100', '$2,310', '$2,460', '$2,070', '$16,520')}

E16CYS_Table_Head = {'Engine Type':'4 Cycle, Vertical, Fresh Water Cooled Diesel Engine',
                    'No. of Cyl.':'6', 'Cylinder Bore x Stroke(mm)':'118x115',
                    'Engine Displacement(cc)':'7,545', 'Combustion Type':'Direct Injection',
                    'Fuel':'Diesel', 'Lub Oil Type':'API CD CLASS', 
                    'Cooling System':'Heat exchanger type forced circulating by centrifigal pump',
                    'Starting System':'DC 24V Electric Starting Type', 'Fuel Injection Pump':'BOSCH type with all speed control GOVERNOR', 'Standard Reduction Ratio':'1.61, 2.06, 2.45, 2.82, 3.12, 3.46'}

E16CYS_Table_Models = {'E16CYS16A':('140/2200', 'NA', '17.5', '525'),
                       'E16CYS16T':('180/2200', 'TC', '15.5', '530'),
                       'E16CYS16TI':('210/2200', 'TCI', '15.5', '553')}

E16CYS_Prices = {'E16CYS16A':('$16,500', '$3,350', '$4,110', '$2,450', '$25,750'),
                 'E16CYS16T':('$17,780', '$3,750', '$4,530', '$2,450', '$27,805'),
                 'E16CYS16TI':('$19,880', '$3,750', '$5,140', '$2,450', '$30,440')}

E30CYS_Table_Head = {'Engine Type':'4 Cycle, Vertical, Fresh Water Cooled Diesel Engine',
                    'No. of Cyl.':'6', 'Cylinder Bore x Stroke(mm)':'130x140',
                    'Engine Displacement(cc)':'11,149', 'Combustion Type':'Direct Injection',
                    'Fuel':'Diesel', 'Lub Oil Type':'API CD CLASS', 
                    'Cooling System':'Heat exchanger type forced circulating by centrifigal pump',
                    'Starting System':'DC 24V Electric Starting Type', 'Fuel Injection Pump':'BOSCH type with all speed control GOVERNOR', 'Standard Reduction Ratio':'1.61, 2.06, 2.45, 2.82, 3.12, 3.46'}

E30CYS_Table_Models = {'E30CYS30T':('300/2100', 'TC', '17.0', '1050'),
                       'E30CYS30TO':('320/2100', 'TCI', '16.0', '1070'),
                       'E30CYS30TI':('360/2000', 'TCI', '15.5', '1250')}

E30CYS_Table_Prices = {'E30CYS30T':('$23,590', '$4,960', '$6,780', '$3,020', '$37,390'),
                       'E30CYS30TO':('$24,430', '$2,250', '$7,810', '$3,020', '$39,505'),
                       'E30CYS30TI':('$26,180', '$5,250', '$7,810', '$3,020', '$41,210')}
#End Variables

#Functions
'''Essentially, the Catalogue page is generated by passing in the variables 
listed above. Depending upon what Engine Series are being looked upon, 
one of the functions below is called (E4CYS is kept as default)'''

@app.route('/catalogue')
def catalogue(page = 'catalogue.html', table = E4CYS_Table_Head, models = E4CYS_Table_Models, prices = E4CYS_Prices):
    return render_template(page, table = table, models = models, prices = prices)


@app.route('/E4CYS')
def E4CYS():
    return catalogue('catalogue.html', E4CYS_Table_Head, E4CYS_Table_Models, E4CYS_Prices)

@app.route('/E16CYS')
def E16CYS():
    return catalogue('catalogue.html', E16CYS_Table_Head, E16CYS_Table_Models, E16CYS_Prices)

@app.route('/E30CYS')
def E30CYS():
    return catalogue('catalogue.html', E30CYS_Table_Head, E30CYS_Table_Models, E30CYS_Table_Prices)

#End Functions
#End Catalogue

@app.route('/register', methods=['GET','POST'])
def register():
    form = SignupForm()

    if request.method=='GET':
        return render_template("sign_up.html",form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                return "Already exists"
            else:
                new_user =  User(form.username.data,form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return "user added"

        else:
            return "form didn't validate"


@app.route('/login', methods=['GET','POST'])
def login():

    form = SignupForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return "User logged in"
                else:
                    return "Wrong password"
            else:
                return "No User with that username"
    else:
        return "form not validated"


if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='localhost', debug=True)


@app.route('/protected')
@login_required
def protected():
    return "protected area"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"

