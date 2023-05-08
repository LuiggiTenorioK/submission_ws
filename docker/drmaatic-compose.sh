#!/bin/bash

echo "Building staging image..."
cd slurm-drmaa-master
./build.sh
cd ..

echo "Building server image..."
cd submission-ws
./build.sh
cd ..

echo "Building docker compose..."
cd test-compose
./compose.sh