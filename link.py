from flask import Blueprint, abort, request, jsonify
from app import Link, db
import re

link_api = Blueprint('link_api', __name__)

url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

@link_api.route('/links', methods = ['POST'])
def add_link():
    req_body = request.get_json(force=True)
    new_link = Link(url = req_body.get('url'), name= req_body.get('name'))
    if re.match(url_pattern, new_link.url) != True: # TODO: testing
        abort(400, "The URL entered is invalid.")
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"id": new_link.id, "url": new_link.url, "name": new_link.name})

@link_api.route('/links/<int:link_id>', methods = ['PUT'])
def update_link(link_id):
    req_body = request.get_json(force=True)
    rows_counted = Link.query.filter_by(id = link_id).update(req_body)
    if rows_counted == 0:
        abort(400)
    db.session.commit()
    return "Link with ID:" + str(link_id) + " has been updated"

@link_api.route('/links/<int:id>', methods = ['DELETE'])
def delete_link(link_id):
    selected_link = Link.query.get_or_404(link_id)
    db.session.delete(selected_link)
    db.session.commit()
    return "Link with ID:" + str(link_id) + " has been deleted."