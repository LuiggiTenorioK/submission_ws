Installation
============

Pre-requisites
----------------------

Before configuring and initialize the web server, there are some requisites that must be fulfilled. First, **the SLURM controller must be running in the same node where you going to run the web server**. As well, the DRMAA library C files should be available in that node. Is highly recommended to use the `PSNC DRMAA for SLURM <https://github.com/natefoo/slurm-drmaa>`_ (version >= 1.1.3) with our library to handle native specification of this implementation::
    
    $ pip install https://github.com/damiclem/submission_lib/archive/setup.zip

Additionally, **a MySQL instance must be active** to store the data of this server.


Installing using pip
----------------------

Using pip, it will install the DRMAAtic Python dependencies. You can do this by running::

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


* **DEBUG** (boolean): Same as the `Django DEBUG setting <https://docs.djangoproject.com/en/4.2/ref/settings/#debug>`_. 
* **MAX_PAGE_SIZE** (integer): Limits the maximum page size on the GET paginated responses.
* **CLUSTER.DRM_SYSTEM** (string): Defines the DRM system that is used. Only ``SLURM`` is supported.
* **CLUSTER.DRMAA_LIBRARY_PATH** (string): Path to the DRMAA C shared object at the controller node file system.
* **CLUSTER.SUBMISSION_SCRIPT_DIR** (string): Base path to the directory where the shell scripts will be stored at the worker node's distributed file system.
* **CLUSTER.SUBMISSION_SCRIPT_DIR** (string): Base path to the directory where the input/output files will be stored at the worker node's distributed file system.
* **CLUSTER.SUBMISSION_LOGGER_PTH** (string): Path to the log file at the controller node file system.
* **CLUSTER.REMOVE_TASK_FILES_ON_DELETE** (boolean): Specify if the output files should be deleted after task deletion.
* **SECURITY.CORS_ALLOWED_ORIGINS** (array[string]): Same as the `django-cors-headers setting <https://github.com/adamchainz/django-cors-headers>`_.
* **SECURITY.ALLOWED_HOSTS** (array[string]): Same as the `Django ALLOWED_HOSTS setting <https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts>`_. 
* **SECURITY.CSRF_COOKIE_SECURE** (boolean): Same as the `Django CSRF_COOKIE_SECURE setting <https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-cookie-secure>`_. 
* **SECURITY.SESSION_COOKIE_SECURE** (boolean): Same as the `Django SESSION_COOKIE_SECURE setting <https://docs.djangoproject.com/en/4.2/ref/settings/#session-cookie-secure>`_. 
* **SECURITY.CSRF_TRUSTED_ORIGINS** (array[string]): Same as the `Django CSRF_TRUSTED_ORIGINS setting <https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins>`_.
* **SECURITY.OAUTH_INTROSPECTION_ENDPOINT** (string): URI to the external authentication service endpoint to verify forwarded JWT tokens.
* **DATABASE.*** (string): Parameters to connect to the MySQL database. Same as the `Django DATABESES settings <https://docs.djangoproject.com/en/4.2/ref/settings/#databases>`_ for one database. Only MySQL backend is supported.

Then, is needed to set up two **enviroment variables**:

* ``DRMAATIC_CONFIG_PATH``: Contains the path to the previously defined configuration JSON file.
* ``DJANGO_SECRET_KEY``: Is highly recommended to set up this key and keep it secret.