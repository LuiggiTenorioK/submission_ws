Installation
============

Installing using pip
----------------------

Using pip, DRMful will install all the needed dependencies and command line tools. You can do this by running::

    $ pip install https://github.com/LuiggiTenorioK/submission_ws/archive/main.zip


Cloning Git Repo
----------------------

Alternatively, you can clone the repository from GitHub and install the requirements::
    
    $ git clone https://github.com/LuiggiTenorioK/submission_ws.git
    $ cd submission_ws
    $ pip install -r requirements.txt



Configuration
---------------

The first step to configure the Django web server is to create the configuration JSON file like this


..  code-block:: json

    {
        "DEBUG": true,
        "MAX_PAGE_SIZE": 1000,
        "CLUSTER": {
            "DRM_SYSTEM": "SLURM",
            "DRMAA_LIBRARY_PATH": "/usr/local/lib/libdrmaa.so.1",
            "SUBMISSION_SCRIPT_DIR": "./scripts/",
            "SUBMISSION_OUTPUT_DIR": "./outputs/",
            "SUBMISSION_LOGGER_PTH": "logger.log",
            "REMOVE_TASK_FILES_ON_DELETE": true
        },
        "SECURITY": {
            "CORS_ALLOWED_ORIGINS": [
                "http://localhost:4200"
            ],
            "ALLOWED_HOSTS": [
                "*"
            ],
            "CSRF_COOKIE_SECURE": false,
            "SESSION_COOKIE_SECURE": false,
            "CSRF_TRUSTED_ORIGINS": [],
            "OAUTH_INTROSPECTION_ENDPOINT": "https://orcid.org/oauth/userinfo"
        },
        "DATABASE": {
            "NAME": "submission_ws",
            "USER": "root",
            "PASSWORD": "password",
            "HOST": "127.0.0.1",
            "PORT": "3306"
        }
    }


Then, is needed to set up two enviroment variables:

* ``DRMFUL_CONFIG_PATH``: Contains the path to the previously defined configuration JSON file.
* ``DJANGO_SECRET_KEY``: Is highly recommended to set up this key and keep it secret.