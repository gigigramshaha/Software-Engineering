from flask import Flask, url_for
from flask import render_template
from flask import request
from flask import redirect


import os

# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy

# this is the database connection string or link 
# brokenlaptops.db is the name of database and it will be created inside 
# project directory. You can choose any other direcoty to keep it, 
# in that case the string will look different. 

# database = "sqlite:///brokenlaptops.db"

database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format (
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )

app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. thid db will be used in this project 
db = SQLAlchemy(app)

##################################################
# use python shell to create the database (from inside the project directory) 
# >>> from app import db
# >>> db.create_all()
# >>> exit()
# if you do not do this step, the database file will not be created and you will receive an error message saying "table does not exist".
###################################################

@app.route('/test')
def test():
    return 'App is running'

@app.route('/init_db')
def init_db():
    db.drop_all()
    db.create_all() 
    return 'DB initialized'

@app.route('/')
def index():
    brokenlaptop = BrokenLaptop.query.all()
    return render_template("index.html",brokenlaptop=brokenlaptop, title="All Broken Laptops")
    

@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        brokenlaptop = BrokenLaptop(brand=brand,price=price)
        
        db.session.add(brokenlaptop)
        db.session.commit()
        
    brokenlaptop = BrokenLaptop.query.all()
    return render_template("create.html", brokenlaptop = brokenlaptop, title="Create a Laptop")

    # now add two lines to retrieve all the BrokenLaptops from the database and display 
    # as it is done in '/' index route 
    
    
@app.route('/delete/<laptop_id>') # add id
def delete(laptop_id):
    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    db.session.delete(brokenlaptop)
    
    # add a line of code to commit the delete operation 
    db.session.commit()
    
    brokenlaptop = BrokenLaptop.query.all()
    return redirect(url_for('index'))
    # now add two lines to retrieve all the BrokenLaptops from the database and display 
    # as it is done in '/' index route 
    
@app.route('/update/<laptop_id>', methods=['GET','POST']) # add id 
def update(laptop_id):
    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    if request.form:
        
        brokenlaptop.brand = request.form.get("brand")
        brokenlaptop.price = request.form.get("price")
        db.session.commit()
        # return redirect("/", code = 302)
        # in this block, a modified instance of BrokenLaptop is coming in along with id
        # add few lines of code so that the modification is saved in the database 
        # for example, Brand of a laptop should be updated from 'Dell' to 'Dell Latitude'
        # code snippet will be similar to create() method 

    return render_template("update.html", brokenlaptop = brokenlaptop)
    # now add two lines to retrieve all the BrokenLaptops from the database and display 
    # as it is done in '/' index route 
    

# this class creates a table in the database named broken_laptop with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it
class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)
    

if __name__ == '__main__':
    app.run(debug=True)
