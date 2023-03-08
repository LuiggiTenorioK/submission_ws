# Configuration

Enviroment variables:

* DRMFUL_CONFIG_PATH
* DJANGO_SECRET_KEY (optional)

## CLUSTER

### TYPE

Specify cluster provider

### DRMAA_LIBRARY_PATH

Path of the DRMAA C implementation

## DATABASE

Provide details about the database

```json
{
    ...
    "DATABASE": {
        "NAME"    : "database_name",
        "USER"    : "username",
        "PASSWORD": "password",
        "HOST"    : "localhost",
        "PORT"    : "3306"
    },
    ...
}
```
