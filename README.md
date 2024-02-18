# django-rest-votings

Democratic voting is a Django app to conduct web-based votes. For each vote,
voters can choose between a fixed number of options.

Detailed documentation is in the "docs" directory.


## How to run using Docker

Docker files (Dockerfile, docker-compose.yml, .env.dev) are ready to use.

To run the containers: `docker compose up -d --build`

Now, wait for Docker to finish the command, and go to http://localhost:8000/reusable_app/my_model_list/ to check if it runs correctly.

To stop and remove everything: `docker compose down -v --rmi "local"`

To stop and don't remove the data in the database for the next compose up: `docker compose down --rmi "local"`

That's it, docker makes things easy.

## Quick start to develop (Using just a python virtual environment)

1. Install requirements using pip (Remember to create your virtual environment):

    pip install -r requirements.txt
    
    pip install -r requirements.dev.txt

2. Copy-paste env-variables-example.txt inside "wrapper" folder, and change the name to ".env"

3. Edit ".env" file, adapting it to your local context

4. Run  ``python manage.py makemigrations`` and ``python manage.py migrate`` to create the tables in the data base.

5. Start the development server and visit this link (http://localhost:8000/reusable_app/my_model_list/) to check everything is running ok.


## How to add this app inside your Django project as a git submodule

This sections assumes that the repo https://github.com/username/django-reusable-app exists and have the code of this repo. You would have to create it and put the code there before doing the steps. (Of course, change "username" to the proper one)

Add this repository in you `.gitmodules` file, like this: 
```git
[submodule "reusable_app"]
	path = path/to/external/apps/django-rest-votings
	url = https://github.com/carlos-m-a/django-rest-votings
    branch = master
```

You can create a soft link to the app folder.
Inside the same folder where `manage.py` is, do this (linux):
```bash
ln -s path/to/external/apps/django-rest-votings/votings votings
```

Remember to modify the next files: 

In `settings.py`:
```python
INSTALLED_APPS = (
    "votings",
    # If you did't create a soft link, use this:
    #"django-rest-votings.votings",
)
```

In `urls.py`:
```python
urlpatterns = [
    path("votings/", include(votings)),
    # If you didn't create a soft link, use this:
    #path("votings/", include(django-rest-votings.votings)),

]
```

4. (Optional) You can add 'votings.context_processors.base_data' in settings,py -> TEMPLATES -> context_processors. (it is not needed, you can skip this step)

4. Run  ``python manage.py makemigrations`` and ``python manage.py migrate`` to create the tables in the data base.

5. Run `python manage.py collectstatic` if necessary.

6. Start the development server and visit this link (http://localhost:8000/reusable_app/my_model_list/) to check that everything is running ok.


## How to generate a python package using a building system (And import it to your django project)

Since this repo only uses the `pyproject.toml`, remember to use at least the version 61.0.0 of setuptools, or other package managers or build systems like hatchling, poetry, etc., that only needs `pyproject.toml`. (Modern python packers only needs pyproject.toml, there is no need of setup.py or setup.cfg) 

Remember to modify `pyproject.toml`, remplacing data for your package data. The file is prepared to be used by "setuptools" library. If you want to use other build system, remember to edit the `[build-system]` part.

For building the package (setuptools):
```bash
python -m pip install --upgrade pip setuptools wheel
python -m build

# And to install the package in your project (See next section)
python -m pip install --user dist/django-rest-votings-0.0.1.tar.gz
```


## Quick start to use in your project when you packed this project

Fist you need to check the last section "How to generate a python package using a building system"

1. Install the app (you need a dist version of the app):

    python -m pip install --user dist/django-rest-votings-0.0.1.tar.gz

    *If you are using a virtual env, maybe you have to modify "venv/pyvenv.cfg" to allow user packages.

2. Add "votings" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'votings',
        ...
    ]

3. Include the votings URLconf in your project urls.py like this::

    path('votings/', include('votings.urls')),

4. (Optional) You can add 'votings.context_processors.base_data' in settings,py -> TEMPLATES -> context_processors. (it is not needed, you can skip this step)

4. Run  ``python manage.py makemigrations`` and ``python manage.py migrate`` to create the tables in the data base.

5. Run `python manage.py collectstatic` if necessary.

6. Start the development server and visit this link (http://localhost:8000/reusable_app/my_model_list/) to check that everything is running ok.
