# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from app import db, login, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class BuildHistory(db.Model):
    __tablename__ = 'build_history'
    build_date = db.Column(db.Date, nullable=False)
    build_version = db.Column(db.Text, primary_key=True, nullable=False, unique=True)
    build_branch = db.Column(db.Text, nullable=False)
    build_platform = db.Column(db.Text, db.ForeignKey('build_platform.platform_id'), nullable=False)
    build_server = db.Column(db.Text, db.ForeignKey('build_server.server_id'), nullable=False)
    last_commit = db.Column(db.Text, nullable=False)
    commit_details = db.Column(db.Text)
    package_repo = db.Column(db.Text)


class BuildPlatform(db.Model):
    __tablename__ = 'build_platform'
    platform_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    os_type = db.Column(db.Text, nullable=False)
    cpu_type = db.Column(db.Text, nullable=False)


class BuildBranch(db.Model):
    __tablename__ = 'build_branch'
    branch_id = db.Column(db.Text, primary_key=True, nullable=False, unique=True)
    branch_name = db.Column(db.Text, nullable=False)


class BuildServer(db.Model):
    __tablename__ = 'build_server'
    server_id = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    cpu_info = db.Column(db.Text)
    memory_info = db.Column(db.Text)
    os_version = db.Column(db.Text)
    kernel_version = db.Column(db.Text)
    gcc_version = db.Column(db.Text)
    rocksdb_version = db.Column(db.Text)

class Permissions:
    USER_MANAGE = 0X01
    UPDATE_PERMISSION = 0x02
    ADMIN = 0x80

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def init_roles():
        role_name_list = ['User', 'Administrator']
        roles = {
            'User': [Permissions.USER_MANAGE],
            'Administrator': [Permissions.USER_MANAGE, Permissions.UPDATE_PERMISSION, Permissions.ADMIN]
        }
        try:
            for r in role_name_list:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                role.reset_permissions()
                for perm in roles[r]:
                    role.add_permission(perm)
                db.session.add(role)
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()


    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    # role = db.relationship('Role', back_populates='users')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['APP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permissions.ADMIN)

    def set_role_id(self, role_id):
        self.role_id = role_id


    def __repr__(self):
        return '<User {}>'.format(self.username)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
login.anonymous_user = AnonymousUser

class Sprint(db.Model):
    __tablename__ = 'sprint'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    start_time = db.Column(db.DateTime(), default=datetime.now())
    end_time = db.Column(db.DateTime(), default=datetime.now())
    description = db.Column(db.Text())
    status = db.Column(db.Enum('0', '1', '2', '3'), index=True, default='0') #0:Not start; 1:Going; 2:Finish; 3:Close

    tasks = db.relationship('Task', backref='sprint', lazy='dynamic')

    def __repr__(self):
        return '<Sprint %r>' % self.name



class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    owner = db.Column(db.String(64), index=True)
    start_time = db.Column(db.DateTime(), default=datetime.now())
    end_time = db.Column(db.DateTime(), default=datetime.now())
    man_hour = db.Column(db.String(64))
    description = db.Column(db.Text())
    status = db.Column(db.Enum('0', '1', '2', '3', '4'), index=True, default='0') #0:Not start; 1:Start; 2:Doing; 3:Done

    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id'))

    def __repr__(self):
        return '<Task %r>' % self.name

    # def task_json_data(self):
    #     jsondata = {
    #         'id': self.id,
    #         'name': self.name,
    #         'owner': self.owner,
    #         'start_time': self.start_time,
    #         'end_time': self.end_time,
    #         'man_hour': self.man_hour,
    #         'description': self.description,
    #         'status': self.status,
    #         'sprint_id': self.sprint_id
    #
    #     }
    #     return jsondata

class TaskSchema(ma.Schema):
    class Meta:
        model = Task

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

