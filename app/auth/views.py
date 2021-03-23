# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from flask import render_template, flash, redirect, url_for, request
from . import auth
from .forms import LoginForm, RegistrationForm, EditUserForm
from flask_login import current_user, login_user, logout_user, login_required
from .decorators import permission_required, admin_required
from werkzeug.urls import url_parse
from app.models import User, Role, Permissions
from app import db, create_app


app = create_app()
with app.app_context():
    Role.init_roles()

@auth.app_context_processor
def inject_permissions():
    return dict(Permission=Permissions)


# Role.init_roles()
# @auth.route('/')
# @auth.route('/index')
# @login_required
# def index():
#     user = {'username': 'Miguel'}
#     return render_template("index.html", title='Home Page')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('kanban.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('kanban.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('kanban.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('kanban.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('kanban.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_role_id(1)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('.login'))
    return render_template('register.html', title='Register', form=form)


@auth.route('/user/<username>')
def user(username):
    users = User.query.all()
    return render_template('user.html', users=users)

@auth.route('/edit-user-profile/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.role = Role.query.get(form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('The user has been updated')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.role.data = user.role_id
    return render_template('edit_user_profile.html', form=form, user=user)



