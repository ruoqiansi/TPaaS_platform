# -*- coding:utf-8 -*-
# Copyright: HoneycombData
# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from flask import render_template, flash, redirect, url_for, request, jsonify
from . import kanban
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Task, db, Sprint, TaskSchema
import datetime


@kanban.route('/addTask', methods=['GET','POST'])
@login_required
def create_task():
    sprints = db.session.query(Sprint).filter(Sprint.status!=3).all()
    if request.method == 'POST':
        task_name = request.form['taskName']
        print(task_name)
        owner = request.form['owner']
        start_time = request.form['startTime']
        start_time1 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        print(start_time1)
        end_time = request.form['endTime']
        end_time1 = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        print(end_time1)
        man_hour = request.form['man_hour']
        description = request.form['description']
        sprint_id = request.form['sprint_select']
        curr_task = Task.query.filter_by(name=task_name).first()
        if curr_task is not None:
            flash('The task name has existed.')
            return redirect(url_for('kanban.create_task'))
        else:
            task = Task(name=task_name,owner=owner,start_time=start_time1,end_time=end_time1,man_hour=man_hour,description=description,sprint_id=sprint_id)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('kanban.index'))
    return render_template('createTask.html', sprints=sprints)

@kanban.route('/', methods=['GET'])
@login_required
def index():
    tasks = Task.query.all()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    paginate = Sprint.query.order_by('id').paginate(page, per_page, error_out=False)
    sprints = paginate.items
    return render_template('index.html', tasks=tasks, paginate=paginate,sprints=sprints)

@kanban.route('/editTask/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.name = request.form['taskName']
        task.owner = request.form['owner']
        start_time_tmp = request.form['startTime']
        task.start_time = datetime.datetime.strptime(start_time_tmp, '%Y-%m-%d %H:%M:%S')
        end_time_tmp = request.form['endTime']
        task.end_time = datetime.datetime.strptime(end_time_tmp, '%Y-%m-%d %H:%M:%S')
        task.man_hour = request.form['man_hour']
        task.description = request.form['description']
        task.status = request.form['status']
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('kanban.index'))
    return render_template('editTask.html', task=task)

@kanban.route('/addSprint', methods=['GET','POST'])
@login_required
def create_sprint():
    if request.method == 'POST':
        sprint_name = request.form['sprintName']
        start_time = request.form['startTime']
        start_time1 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        print(start_time1)
        end_time = request.form['endTime']
        end_time1 = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        print(end_time1)
        description = request.form['description']
        curr_sprint = Sprint.query.filter_by(name=sprint_name).first()
        if curr_sprint is not None:
            flash('The sprint name has existed.')
            return redirect(url_for('kanban.create_sprint'))
        else:
            sprint = Sprint(name=sprint_name, start_time=start_time1, end_time=end_time1, description=description)
            db.session.add(sprint)
            db.session.commit()
            return redirect(url_for('kanban.index'))
    return render_template('createSprint.html')

@kanban.route('/editSprint/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sprint(id):
    sprint = Sprint.query.get_or_404(id)
    if request.method == 'POST':
        sprint.name = request.form['sprintName']
        start_time_tmp = request.form['startTime']
        sprint.start_time = datetime.datetime.strptime(start_time_tmp, '%Y-%m-%d %H:%M:%S')
        end_time_tmp = request.form['endTime']
        sprint.end_time = datetime.datetime.strptime(end_time_tmp, '%Y-%m-%d %H:%M:%S')
        sprint.description = request.form['description']
        sprint.status = request.form['status']
        db.session.add(sprint)
        db.session.commit()
        return redirect(url_for('kanban.index'))
    return render_template('editSprint.html', sprint=sprint)

@kanban.route('/taskTable/<int:sprint_id>', methods=['GET','POST'])
def get_task_table(sprint_id):
    print(sprint_id)
    sprint = Sprint.query.get_or_404(sprint_id)
    tasks = db.session.query(Task).filter_by(sprint_id=sprint_id)
    return render_template('taskTable.html', tasks=tasks, sprint=sprint)

@kanban.route('/sprintList/')
def sprint_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 2))
    paginate = Sprint.query.order_by('id').paginate(page, per_page, error_out=False)
    sprints = paginate.items
    # sprints = Sprint.query.all().order_by(Sprint.id.asc()).paginate(page=page, per_page=5)
    return render_template('test_page.html', paginate=paginate, sprints=sprints)















