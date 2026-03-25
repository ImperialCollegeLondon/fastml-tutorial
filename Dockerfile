FROM intel/oneapi-basekit:2025.0.1-0-devel-ubuntu24.04

# Install basic build tools and python prerequisites
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3-pip \
    python3-venv \
    && apt update \
    && apt install -y intel-oneapi-compiler-fpga \
    && rm -Rf /var/lib/apt/lists/* \
    && apt-get clean

# Create python environment
RUN python3 -m venv /opt/venv

# Use venv python by default
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN pip install --upgrade pip && \
    pip install jupyter && \
    pip install numpy pandas scikit-learn && \
    pip install keras tensorflow jax && \
    pip install matplotlib mplhep && \
    pip install hls4ml[profiling] da4ml hgq2 && \
    pip install tqdm h5py ndjson && \
    pip install ipykernel && \
    python3 -m ipykernel install --user --name fastml_intel --display-name "Python (fastml_intel)"


# Set the working directory
WORKDIR /workspace

EXPOSE 8888
