# Import flask dependencies
from flask import Blueprint, request, render_template
from flask import session as login_session


# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_items = Blueprint('items', __name__, url_prefix='/items')

# Set the route and accepted methods

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('uploads/' + secure_filename(f.filename))
    else:
        return "Please Upload Something"