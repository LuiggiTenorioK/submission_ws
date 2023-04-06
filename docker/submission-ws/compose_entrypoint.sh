#!/bin/bash

submission-ws-setup
submission-ws-manage createsuperuser --noinput --username admin --email admin@admin.com
submission-ws --port 4821