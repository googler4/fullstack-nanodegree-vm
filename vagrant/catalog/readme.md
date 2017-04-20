Let's keep this as short as possible.


This instance REQUIRES venv, venv and flask are like peanut butter and jelly. They always go together.
`pip install virtualenv` for venv, then `virtualenv the_organizer`. IF it's not already there, once it's in place `cd the_organizer` to enter the root folder and `. venv/bin/activate` and your inside our virtual env!!

We are using PIP-TOOLS `pip install pip-tools`. To compile a list of dependencies, use `pip-compile` then `pip-sync`. MAKE SURE PYTHON IS SETUP CORRECTLY, included the permissions. There's no sudo requirement, vagrant seems to believe otherwise.

For the moment we are leveleraging SQL LITE, so no DB setup.

`python manage.py init_db` will build a DB from scratch

`python manage.py runserver` to run the dev server.
`python manage.py runserver --host=0.0.0.0` from inside vagrant.


Finally my client_id is redacted from the config (config.py). Insert any valid google client config to get /login function.


