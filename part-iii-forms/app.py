# Application file
#
# Simple application to add a business and list businesses

from flask import Flask, url_for

from flask import request, render_template, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, utils

import forms
from forms import BizForm, AddBiz


# Create app and load the config
app = Flask(__name__)
app.config.from_object('config')

# connect to the database
db = SQLAlchemy(app)


# the "models" import SHOULD be after the above "db" assignment
import models
# 'from models import *' works but 'from models import Business' does NOT work
# dont know why!
from models import *


# run db.create_all before running the app to create DB Tables

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/add/',methods=['GET','POST'])
def new_biz():
    form = AddBiz(csrf_enabled=True)

    if form.validate_on_submit():

        new_biz = Business(
                    	form.name.data,
                    	form.description.data,
                    	form.added_date.data
                    )

        db.session.add(new_biz)
        db.session.commit()
        return redirect(url_for('biz_list'))
    return render_template('biz.html',form=form)

@app.route('/bizlist',methods=['GET','POST'])
def biz_list():
    """ Query Business object and list businesses
    """
    biz_list = Business.query.all()
    return render_template('biz_list.html', bizs=biz_list)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=int('8080'),
        debug=app.config['DEBUG']
    )
