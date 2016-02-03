# Demo of Flask-Security and Flask-Admin capabilities
# @akaak


from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import current_user, login_required, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from wtforms.fields import PasswordField

from flask.ext.admin import Admin

from flask_mail import Mail
from flask.ext.admin.contrib import sqla


app = Flask(__name__)

app.config['DEBUG']=True
app.config['SECRET_KEY'] = 'todo-app-secret-key'

# for postgresql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ID@localhost/flask_example'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'

# Config values for Flask-Security.
# We're using PBKDF2 with salt.
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
# Replace this with your own salt.
app.config['SECURITY_PASSWORD_SALT'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

app.config['SECURITY_EMAIL_SENDER'] = 'no-reply@example.com'
# SMTP Server settings (using https://github.com/ThiefMaster/maildump)
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

# for app registration, confirmation by email
app.config['SECURITY_REGISTERABLE'] = True 
app.config['SECURITY_CONFIRMABLE'] = True 
app.config['SECURITY_RECOVERABLE'] = True 


# Flask-Mail and SQLAlchemy initialization
mail = Mail(app)
db = SQLAlchemy(app)

# Users and Roles table
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    
    confirmed_at = db.Column(db.DateTime())
    
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def before_first_request():

    db.create_all()

    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Test Users
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('someone@example.com'):
        user_datastore.create_user(email='someone@example.com', password=encrypted_password)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password)

    db.session.commit()

    user_datastore.add_role_to_user('someone@example.com', 'end-user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()


@app.route('/')
@login_required
def index():
    return render_template('index.html')


class UserAdmin(sqla.ModelView):

    column_exclude_list = ('password',)

    form_excluded_columns = ('password',)

    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def scaffold_form(self):

        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):

        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)


class RoleAdmin(sqla.ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')

# Initialize Flask-Admin
admin = Admin(app)
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=int('8080'),
        debug=app.config['DEBUG']
    )
