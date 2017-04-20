import os

from flask_script import Manager, Server, prompt_bool

from the_organizer.webapp import app, database, setup_app
from the_organizer.service import db_init, csvload

# from organizer.api import configure_api


manager = Manager(app)


api = setup_app(os.getenv('ORGANIZER_CONFIG', 'default'), app, database)


manager.add_command('runlocal', Server(host='localhost', port=5000))


@manager.shell
def make_shell_context():
    """This saves quite a few imports."""
    return dict(app=app, db=database, api=api)




@manager.command
def init_db():
    """Initializes the database."""

    # from the_organizer.models import Program
    if prompt_bool('You sure you wanna create (recreate) the current tables?'):
        database.drop_all()
        database.create_all()
        db_init.init_db()
        csvload.runCSV()


@manager.command
def drop_tables():
    """Drops all the tables."""
    if prompt_bool('You sure you wanna destroy everything?'):
        database.drop_all()


if __name__ == '__main__':
    manager.run()
