from flask import Blueprint, request, render_template, Response
from flask import session as login_session

import random
import string
import flask
import httplib2

from flask import request
from werkzeug.utils import secure_filename
from apiclient import discovery
from oauth2client import client, crypt
from the_organizer.models import User
from flask_login import login_required, login_user, logout_user
from the_organizer.webapp import database as db, app

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
# login_manager.login_view = "login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.args.get('state') != login_session['state']:
            token = request.args.get('idtoken')
            client_id = app.config['CLIENT_ID']
            try:
                idinfo = client.verify_id_token(token, client_id)
                print idinfo
                # Or, if multiple clients access the backend server:
                #idinfo = client.verify_id_token(token, None)
                # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
                #    raise crypt.AppIdentityError("Unrecognized client.")

                if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise crypt.AppIdentityError("Wrong issuer.")

                email = idinfo['email']
                image_url = idinfo['picture']
                name = idinfo['name']
                first = idinfo['given_name']
                last = idinfo['family_name']
                at_hash = idinfo['at_hash']
                iss = idinfo['iss']
                locale = idinfo['locale']

                # If auth request is from a G Suite domain:
                # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
                #    raise crypt.AppIdentityError("Wrong hosted domain.")
            except crypt.AppIdentityError:
                # Invalid token
                print "Invalid"
                return render_template('login.html', error=401)

            try:
                user = db.session.query(User).filter(User.email == email).one()
                print "Found User"
            except:
                print "Create New User"
                user = User.add(name, image_url, email)
                user.insert()

            login_user(user)
            return flask.redirect(flask.url_for('index'))
        else:
            return render_template('login.html', error=401)

    else:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state
        print state
        return render_template('login.html', state=state, client_id = app.config['CLIENT_ID'])


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))
