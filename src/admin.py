import os
from flask_admin import Admin
from models import db, User, Planets, People, Favoritos
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators

class UserForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    is_active = BooleanField('Is Active')

class UserAdmin(ModelView):
    form = UserForm
    column_list = ('email', 'password','is_active')


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserAdmin(User, db.session))

    # You can duplicate that line to add mew models
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Favoritos, db.session))