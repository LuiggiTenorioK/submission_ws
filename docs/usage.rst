Usage
======


Initializing the web server
---------------------------

Once the server is correctly configured, is important to make the migrations of the Django application. This can be done running::

    $ python manage.py makemigrations submission
    $ python manage.py migrate

Then, you are free to follow the `Django Deployment Guide <https://docs.djangoproject.com/en/4.2/howto/deployment/>`_ or just run a basic development server with::

    $ python manage.py runserver


Admin User Interface
---------------------------

To enter to the Admin User Interface, you must first create a user for this with::

    $ python manage.py createsuperuser --noinput --username <your_admin_username> --email <your_email_address>

Then, you can access it through ``http://<YOUR_WEB_SERVER_URI>/admin```


External user token exchange
-----------------------------


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
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

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