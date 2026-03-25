#!/bin/bash

# Project folder name
PROJECT_NAME=${1}

echo "Launching build for: $PROJECT_NAME"

# Execute build commands inside the docker container
# Source oneapi-vars.sh to load the compiler environments and fpga_vars
docker exec -t intel_builder bash -c "
    source /opt/intel/oneapi/2025.0/oneapi-vars.sh --force && \
    source /opt/intel/oneapi/2025.0/opt/oclfpga/fpgavars.sh --force && \
    cd $PROJECT_NAME && \
    mkdir -p build && cd build && \
    cmake .. && \
    make report
"

echo "Build complete for project: $PROJECT_NAME. Check report.html for results."
