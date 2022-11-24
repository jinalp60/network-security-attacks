import os
import json
from flask import Flask,request, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from serializers import AlchemyEncoder

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'flask_mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)
connection = db.session.connection()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

#db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/insecure-pofile-details',methods=['GET','POST'])
def insecure():
    ret = []

    if request.method == 'POST':
        user = request.form['username']
        stmt = 'select * from user where username = "'+ user +'"'
        print(stmt)
        res = connection.execute(stmt)
        output = []
        for obj in res:
            single = {}
            single['id'] = obj[0]
            single['username'] = obj[1]
            single['email'] = obj[2]
            output.append(single)
        return json.dumps(output)

@app.route('/secure-profile-details',methods=['GET','POST'])
def secure():

    if request.method == 'POST':
        username = request.form['username']
        res = User.query.filter_by(username=username).all()
        ret = []
        for user in res:
            ret.append(
                {
                    'username': user.username,
                    'email': user.email
                }
            )
        return json.dumps(ret)
    
@app.route('/secure-nonorm-profule-details',methods=['GET','POST'])
def secure_nonorm():

    if request.method == 'POST':
        user = request.form['username']
        stmt = text("select * from user where username = :s")
        res = connection.execute(stmt, s=user)
        output = []
        for obj in res:
            single = {}
            single['id'] = obj[0]
            single['username'] = obj[1]
            single['email'] = obj[2]
            output.append(single)
        return json.dumps(output)




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)