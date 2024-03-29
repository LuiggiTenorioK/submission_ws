.. _usage:

Usage
======


Initializing the web server
---------------------------

Once the server is correctly configured, is important to make the migrations of the Django application. This can be done running::

    $ python manage.py makemigrations submission
    $ python manage.py migrate

Then, you are free to follow the `Django Deployment Guide <https://docs.djangoproject.com/en/4.2/howto/deployment/>`_ or just run a basic development server with::

    $ python manage.py runserver

Once is initialized, you can follow the `Admin Usage guide <admin-usage.html>`_ to create your available scripts.


External user token exchange
-----------------------------

To use a protected resource, first, you need to get an authentication token from DRMAAtic. To get one, you need to exchange your external ORCID token for a DRMAAtic token. This can be done by calling the ``GET /token/{username}`` endpoint sending the token in the ``Authorization: Bearer <orcid_token>`` header and it will return the new token if it's successfully verified by ORCID. Then, further calls to protected resources should contain your new token in the ``Authorization: Bearer <drmaatic_token>`` header to get access.


Getting available script information
-------------------------------------

.. code-block:: python
    :linenos:

    import requests

    url = "http://<YOUR_WEB_SERVER_URI>/script"

    response = requests.request("GET", url)

    print(response.text)



Running a Task
---------------------------

.. code-block:: python
    :linenos:

    import requests

    url = "http://<YOUR_WEB_SERVER_URI>/task/"

    payload={'task_name': 'your_task_name'}
    files=[
        ('some_input_param',('your_filename',open('/your_file_path','rb'),'application/octet-stream'))
    ]

    response = requests.request("POST", url, data=payload, files=files)

    print(response.text)



Get Task Status
---------------------------

.. code-block:: python
    :linenos:

    import requests

    url = "http://<YOUR_WEB_SERVER_URI>/task/<your_task_id>"

    response = requests.request("GET", url)

    print(response.text)



Deleting a Task
---------------------------

.. code-block:: python
    :linenos:

    import requests

    url = "http://<YOUR_WEB_SERVER_URI>/task/<your_task_id>"

    response = requests.request("DELETE", url)

    print(response.text)


Downloading Task files
---------------------------

.. code-block:: python
    :linenos:

    import requests

    url = "http://<YOUR_WEB_SERVER_URI>/task/<your_task_id>/download"

    response = requests.request("GET", url)

    print(response.text)