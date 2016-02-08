from flask import Flask

from flask import request, render_template, flash, redirect
from forms import BizForm, AddBiz
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, utils
from contextlib import closing

import forms
import models
from models import Bizs, db

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)



@app.route('/add/',methods=['GET','POST'])
def new_biz():
    form = AddBiz(csrf_enabled=True)
    #form_biz = Bizs()
    if form.validate_on_submit():

        new_biz = Bizs(
                    	form.name.data,                     
                    	form.description.data,
                    	form.added_date.data
                    )

        db.session.add(new_biz)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('biz.html',form=form)

'''
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
'''

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=int('8080'),
        debug=app.config['DEBUG']
    )