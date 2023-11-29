from flask import Blueprint, abort, request, jsonify
from app import Task, db

task_api = Blueprint('task_api', __name__)

# Task Functions
@task_api.route('/tasks', methods=['POST'])
def add_task():
    req_body = request.get_json(force=True)
    new_task = Task(task=req_body.get('task'), time=req_body.get('time')) # not sure if this works
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "task": new_task.task, "time": new_task.time})

@task_api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    selected_task = Task.query.get_or_404(task_id)
    db.session.delete(selected_task)
    db.session.commit()
    return "Task with ID:" + str(task_id) + " has been deleted."

@task_api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    req_body = request.get_json(force=True)
    rows_counted = Task.query.filter_by(id = task_id).update(req_body)
    if rows_counted == 0:
        abort(404)
    db.session.commit()
    return "Task with ID:" + str(task_id) + " has been updated."