# Import flask dependencies
from flask import Blueprint, request, render_template
from flask import session as login_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from flask_login import login_required
from ..webapp import database as db


# Import the database object from the main app module
from the_organizer.models import Group, Item, GroupMap


# Import module models (i.e. User)
# from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_groups = Blueprint('groups', __name__)

# Set the route and accepted methods


@mod_groups.route('/groups/', methods=['GET', 'POST'])
def groups():

    try:
        group_exist = db.session.query(Group).all()

    except:
        print "Error"
        # print e

    return render_template('group.html', groups=group_exist)


@mod_groups.route('/groups/<id>/', methods=['GET', 'POST'])
def groups_find(id):

    try:
        group_exist = db.session.query(Group).filter(
            Group.id == id).one()

    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'no user, create one'

    try:
        # print group_exist.group_maps.id
        item_exist = db.session.query(Item).join(GroupMap).filter(
            GroupMap.group_id == group_exist.id).all()
        print 'Item Exists'
        # print item_exist.group_maps

    except:
        print "Error"
        item_exist = db.session.query(Item).filter(Item.id == '').all()

    return render_template('group_view.html', group=group_exist, items=item_exist)


@mod_items.route('/groups/<id>/edit', methods=['POST'])
@login_required
def groups_edit_post(id):
    # Process Group Data

    try:
        group_exist = db.session.query(Group).filter(
            Group.id == id).one()
    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'No groups'

    data = request.form

    if data['title']:
        group_exist.title = data['title']

    if data['headline']:
        group_exist.headline = data['headline']

    if data['description']:
        group_exist.description = data['description']

    if data['url']:
        group_exist.url = data['url']

    group_exist.last_updater = data['user']

    db.session.commit()

    return render_template('group_view.html', group=group_exist)


@mod_groups.route('/groups/<id>/edit', methods=['GET'])
@login_required
def groups_edit(id):

    try:
        group_exist = db.session.query(Group).filter(
            Group.id == id).one()

    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'No groups'

    return render_template('groups_edit.html', group=group_exist)

# Delete


@mod_groups.route('/groups/<id>/delete', methods=['GET', 'POST'])
@login_required
def groups_delete(id):

    try:
        group_exist = db.session.query(Group).filter(
            Group.id == id).one()

    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'No user'

    db.session.delete(group_exist)
    db.session.commit()

    # Todo flash confirmation

    return render_template('group.html')
