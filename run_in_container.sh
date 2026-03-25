#!/bin/bash

# -----------------------------
# Generic Docker runner script
# -----------------------------
# Usage:
# ./run_in_container.sh "<command>"

# Name of the Docker container
CONTAINER_NAME=intel_builder

# Check that a command was provided
if [ -z "$1" ]; then
    echo "Usage: $0 \"<command>\""
    exit 1
fi

# Full command to run
USER_CMD="$1"

echo "Running command inside container '$CONTAINER_NAME':"
echo "  $USER_CMD"

# Execute command inside container
docker exec -t $CONTAINER_NAME bash -c "
    source /opt/intel/oneapi/2025.0/oneapi-vars.sh --force && \
    source /opt/intel/oneapi/2025.0/opt/oclfpga/fpgavars.sh --force && \
    cd /workspace && \
    $USER_CMD
"

echo "Command completed."
