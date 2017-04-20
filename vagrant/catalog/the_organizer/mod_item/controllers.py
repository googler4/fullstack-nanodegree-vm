# Import flask dependencies
from flask import Blueprint, request, render_template
from flask import session as login_session
from flask_login import login_required
from ..webapp import database as db



# Import the database object from the main app module
from the_organizer.models import Item


# Import module models (i.e. User)
# from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_items = Blueprint('items', __name__)

# Set the route and accepted methods
@mod_items.route('/items/', methods=['GET', 'POST'])
def items():
    from sqlalchemy.orm.exc import NoResultFound
    from sqlalchemy.orm.exc import MultipleResultsFound

    try:
        item_exist = db.session.query(Item).all()

    except:
        print "Error"
        # print e

    return render_template('item.html', items = item_exist)

@mod_items.route('/items/<id>/', methods=['GET', 'POST'])
def items_find(id):
    from sqlalchemy.orm.exc import NoResultFound
    from sqlalchemy.orm.exc import MultipleResultsFound

    try:
        item_exist = db.session.query(Item).filter(
                Item.id == id).one()

    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'no user, create one'

    return render_template('item_view.html', item = item_exist)

@mod_items.route('/items/<id>/edit', methods=['POST'])
@login_required
def items_edit_post(id):
    print request.method
    print request.form
    #Process Form Data
    print request.form['title']

    try:
        item_exist = db.session.query(Item).filter(
                Item.id == id).one()
    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'No Items'
    
    data = request.form

    item_exist.title = data['title']
    item_exist.headline = data['headline']
    item_exist.description = data['description']
    item_exist.url = data['url']

    db.session.commit()

    return render_template('item_view.html', item = item_exist)

@mod_items.route('/items/<id>/edit', methods=['GET'])
@login_required
def items_edit(id):
    from sqlalchemy.orm.exc import NoResultFound
    from sqlalchemy.orm.exc import MultipleResultsFound

    try:
        item_exist = db.session.query(Item).filter(
                Item.id == id).one()

    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'No Items'

    return render_template('item_edit.html', item = item_exist)


# Delete
@mod_items.route('/items/<id>/delete', methods=['GET', 'POST'])
@login_required
def items_delete(id):
    from sqlalchemy.orm.exc import NoResultFound
    from sqlalchemy.orm.exc import MultipleResultsFound

    try:
        item_exist = db.session.query(Item).filter(
                Item.id == id).one()

    except MultipleResultsFound, e:
        print e

    except NoResultFound, e:
        print 'no user, create one'

    return render_template('item_view.html', item = item_exist)