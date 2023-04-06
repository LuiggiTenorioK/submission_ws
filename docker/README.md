# Setup

## Test compose

```
cd slurm-drmaa-master && ./build.sh && cd ..
cd submission-ws && ./build.sh && cd ..
cd test-compose && ./compose.sh
```

After this you should have the submission web server at http://localhost:4821/