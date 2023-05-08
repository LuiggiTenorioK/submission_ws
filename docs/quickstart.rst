.. _quickstart:

Quick Start
=============

DRMAAtic provides a Docker container to quickly test its features. You can use it by using Docker Compose::
    
    $ cd submission_ws/docker
    $ ./drmaatic-compose.sh

After this you should have the submission web server at http://localhost:4821/. This will build one SLURM controller, one SLURM worker, and a MySQL instance.