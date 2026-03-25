# Fast ML UK tutorial
This repository contains the code for the Fast ML UK tutorial. The tutorial is available at [https://indico.cern.ch/event/1641573/](https://indico.cern.ch/event/1641573/).

## Installation and setup instructions
The installation process for this tutorial is not super straightforward and depends on your operating system (Linux/Windows vs MacOS). The main bottleneck is the installation of Intel's oneAPI toolkit, which provides the FPGA toolchain (including high-level synthesis compilers and libraries) needed to translate Machine Learning (ML) models into hardware descriptions and to build/emulate them for FPGA deployment. Unfortunately, the oneAPI toolkit is not natively supported on MacOS, which means that Mac (with Apple Silicon) users will need to use a Docker container with a emulated Linux environment to run the build. In any case, all operating systems will require the installation of Docker.

**You will also need around 30-40Gb of free disk space to install the necessary software and dependencies!**

Please complete the installation and setup instructions (for your operating system) before the tutorial. If you have any issues with the installation, please feel free to ask for help in the tutorial session or to add your issue in this running gDocs document: [https://docs.google.com/document/d/1IDD6wGrUueK47ZF0X4CQM1UNCoearA33r29EQwyrjSc/edit?usp=sharing](https://docs.google.com/document/d/1IDD6wGrUueK47ZF0X4CQM1UNCoearA33r29EQwyrjSc/edit?usp=sharing).

You should be able to get through the installation and setup instructions and run the test scripts. If you are able to do this, then you are all set to run the tutorial notebooks without any issues.

### WSL installation for Windows users
For Windows users, you will need to install the Windows Subsystem for Linux (WSL) to run the Docker container with the oneAPI toolkit. You can follow the instructions at [https://docs.microsoft.com/en-us/windows/wsl/install](https://docs.microsoft.com/en-us/windows/wsl/install) to install WSL on your system.

### Docker installation
For those of you who don't have Docker installed, you need to download it and then follow the instructions for installation (ChatGPT is helpful for this if you get stuck!).
For Linux users, you can follow the instructions at [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) to install Docker on your system. For Windows and MacOS users, you can download Docker Desktops from the following link and follow the instructions for installation: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).

You can verify that Docker is installed correctly by running the following command in your terminal:

```bash
docker --version
```
This should output the version of Docker that you have installed.

### Cloning the repository and downloading the data files
You will need to clone this repository and download the data files that we will use for the tutorial. Everything will be ran from the root directory of this repository, so it important that you clone the repo in a suitable location on your machine where you have read/write permissions and enough disk space. 
First `cd` to a directory where you want to clone the repository, and then run the following command:

```bash
git clone https://github.com/ImperialCollegeLondon/fastml-tutorial.git
cd fastml-tutorial
```
At this point you should also download the data files we will use for the tutorial (~100Mb) using the following commands, and place them in the `data` directory:
```bash
mkdir data

# For linux/windows users:
wget -P data/ https://www.hep.ph.ic.ac.uk/~llaatu/Collide_X.npy
wget -P data/ https://www.hep.ph.ic.ac.uk/~llaatu/Collide_y.npy

# For MacOS users:
cd data
curl -O https://www.hep.ph.ic.ac.uk/~llaatu/Collide_X.npy
curl -O https://www.hep.ph.ic.ac.uk/~llaatu/Collide_y.npy
cd ..
```

Please now follow the instructions for your operating system below to set up the environment for the tutorial.
* [Instructions for Linux/Windows users](#instructions-for-linuxwindows-users)
* [Instructions for MacOS users](#instructions-for-macos-users)


### Instructions for Linux/Windows users
You lucky folks can do everything within a single docker container. This means you can run the hls4ml build and emulation steps within the tutorial notebooks without any issues.

1. First, let's build the Docker image using the provided Dockerfile:

    ```bash
    docker build -t intel-oneapi-hls4ml .
    ```

    If you open the Dockerfile, you will see that it installs the oneAPI toolkit and a bunch of other python libraries within a virtual environment in the container. These python libraries include keras (with jax backend) for training ML models, hls4ml for translating ML models into hardware descriptions, and a few other libraries for data manipulation and visualization. You will also see the  (high granularity quantization) library which is used for optimizing the ML models for FPGA deployment.

3. Run the Docker container:

    ```bash
    docker run -d -t -p 127.0.0.1:8888:8888 --name intel_builder -v "$PWD:/workspace" -w /workspace intel-oneapi-hls4ml bash
    ```
    This will start a Docker container (running in the background)   named `intel_builder` and map port 8888 from the container to your local machine, allowing you to access Jupyter notebooks. It also mounts the current directory (`$PWD`) to `/workspace` in the container, so you can access the tutorial files. 

4. Enter an interactive shell in the running container. This will allow you to run commands and start the Jupyter notebook server:

    ```bash
    docker exec -it intel_builder bash
    ```
    **You must always** setup the oneAPI environment variables before running any commands related to the FPGA toolchain. You can do this by running the following commands in the interactive shell:

    ```bash
    source /opt/intel/oneapi/2025.0/oneapi-vars.sh --force
    source /opt/intel/oneapi/2025.0/opt/oclfpga/fpgavars.sh --force
    ```

5. Test that everything is working by running:

    ```bash
    python test_hls4ml.py proj_test
    ```
    This will run a test script that imports keras and hls4ml, builds a (tiny) ML model, coverts it to an FPGA implementation using hls4ml, and runs the emulation of the build. If everything is working correctly, you should see a print message of the FPGA resource usage for this simple design. You can also find a more detailed build report by opening `proj_test/build/myproject.report.prj/reports/report.html` in a web browser.

    **Ignore the segmentation fault warning**. This is a known issue with the oneAPI toolchain and does not affect the functionality of the build or emulation.

If you are able to run the test script successfully, then you should be all set to run the tutorial notebooks. You can start the Jupyter notebook server by running the following command in the container:

```bash
jupyter notebook --ip=0.0.0.0 --port 8888 --allow-root
```

You can then access the notebooks by opening a web browser and navigating to the URL provided in the terminal. Alternatively, you can run the notebooks within VS Code by installing the "Remote - Containers" extension and attaching to the running container.

When finishing a session, you can exit the container by running `exit` in the terminal. You should then stop the running container with:

```bash
docker rm -f intel_builder
```

Any files that you created or modified within the `/workspace` directory in the container will be saved to your local machine, so you can easily access them after stopping the container.

Just remember that when you come to the tutorial, you will need to repeat step 2 to start the container running and step 3 to enter the interactive shell before you can run any commands or start the Jupyter notebook server.

### Instructions for MacOS users
*Note: This is the case for MacOS users with Apple Silicon (M1-M4 chips). We **think** that for MacOS users with Intel chips (check "About This Mac" if you are not sure) you should be able to follow the same instructions as Linux/Windows users, but we have not tested this ourselves.*

Unfortunately, the oneAPI toolkit is not natively supported on MacOS, which means that Mac users will need to use a Docker container with an emulated Linux environment to run the build. 

This add an extra complication... running jupyter notebooks within the emulated environment does not work, or at least, it is extremely slow and not responsive. This means we will set up a local python environment on the MacOS host machine for training the ML models, and then use the (emulated) Docker container for the hls4ml build and emulation steps. In fact, this is more similar to the standard workflow for FPGA development, where you would typically train your ML models on a separate machine and then use a separate build server with the FPGA toolchain installed to run the build and emulation steps.

In practice, you will run the Jupyter notebooks on your local machine until you get to the hls4ml build steps. At that point, you will run the build steps as bash/python scripts within the Docker container, and then you can visualize the results (e.g. resource usage) back on your local machine. This is a bit more cumbersome than running everything within the container, but unfortunately it is the only way (we have found) to get this tutorial working on MacOS (with Apple Silicon).

#### Setting up the local python environment
We have tested this for `python 3.11.9`. We therefore recommend that you use this version of python for the local environment on your MacOS machine. You can use a tool like `pyenv` to manage multiple python versions on your machine. You can install `pyenv` by following the instructions at [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv), or by asking ChatGPT if you prefer.

Once you have `pyenv` installed, you can install python 3.11.9 with the following command:

```bash
pyenv install 3.11.9
```

You can then create a virtual environment for the tutorial and activate it:

```bash
pyenv shell 3.11.9
python -m venv fastml
source fastml/bin/activate
```

Next, you will need to install the necessary python libraries for the tutorial. You can do this with the following commands:

```bash
pip install --upgrade pip
pip install -r requirements_macos.txt
pip install ipykernel
python -m ipykernel install --user --name fastml --display-name "Python (fastml)"
```

This includes (see `requirements_macos.txt`) keras (with jax backend) for training ML models, and a few other libraries for data manipulation and visualization. It will also install hls4ml, but this will only be used for writing the models out in a format that can be read by the oneAPI toolchain in the Docker container. You will also see the hqg (high granularity quantization) library which is used for optimizing the ML models for FPGA deployment. This is done before the build step, so it can be run on the local machine without any issues.

You can test that the local environment is working by running the following command:

```bash
python test_hls4ml_write.py proj_test_macos
```

This will run a test script that imports keras and hls4ml, builds a (tiny) ML model, and writes it out in a format that can be read by the oneAPI toolchain in the Docker container. If everything is working correctly, you should see a print message confirming that the model was written successfully.

When it comes to running the Jupyter notebooks in the tutorial, you can start the Jupyter notebook server on your local machine with the following command:

```bash
jupyter notebook
```

You can then access the notebooks by opening a web browser and navigating to the URL provided in the terminal. Alternatively, you can run the notebooks within VS Code by installing the "Python" extension and selecting the "Python (fastml)" kernel for the notebooks. When you get to the hls4ml build steps in the notebooks, you will need to run those steps using separate bash/python scripts within the Docker container, as described in the next section.

#### Setting up the Docker container for the build
You will also need to set up the Docker container with the emulated linux environment for the hls4ml build. 

1. Let's start with the Docker build step:

    ```bash
    docker build --platform linux/amd64 -t intel-oneapi-hls4ml .
    ```
    If you open the Dockerfile, you will see that it installs the oneAPI toolkit and a bunch of other python libraries within a virtual environment in the container. These python libraries overlap with the ones you installed on your local machine, as they are needed for the performance evaluation later in the tutorial.

    The `--platform linux/amd64` flag is needed to build an image that can run on the emulated linux environment on MacOS with Apple Silicon. This will allow us to run the oneAPI toolchain within the Docker container, which is necessary for the hls4ml build and emulation steps.

2. Run the Docker container:

    ```bash
    docker run -d -t --platform linux/amd64 --name intel_builder -v "$PWD:/workspace" -w /workspace intel-oneapi-hls4ml bash
    ```
    This will start a Docker container (running in the background) named `intel_builder` and mount the current directory (`$PWD`) to `/workspace` in the container, so you can access the tutorial files. Note, in this case (comparing to the linux/Windows installation) we are not mapping any ports from the container to the local machine, since we will not be running the Jupyter notebook server within the container. 

3. We have set up some wrapper scripts to run the build and emulation steps within the container. These scripts will automatically set up the oneAPI environment variables and run the necessary commands.

    **Option 1**:To run (only the build step) for a given project, you can use the following command:

    ```bash
    ./build_report.sh proj_test_macos
    ```
    This will run the build step within a `docker exec` command for the project `proj_test_macos`, which is the same project that we used to test the local python environment. You can replace `proj_test_macos` with any of the other projects (in the tutorial) to run the build for those projects. A summary of the resource usage can be printed to the screen with:
    ```bash
    python print_report_summary.py proj_test_macos
    ```
    You can also find a more detailed build report by opening `proj_test_macos/build/myproject.report.prj/reports/report.html` in a web browser.

    Ignore the segmentation fault warning. This is a known issue with the oneAPI toolchain and does not affect the functionality of the build or emulation.

    **Option 2**: If you want to run any command within the docker container (e.g. to run python scripts) you can use the following command:

    ```bash
    ./run_in_container.sh "python test_hls4ml_build.py proj_test_macos"
    ```
    This will run the command `python test_hls4ml_build.py proj_test_macos` within the container, which will run an emulation of the build for project `proj_test_macos` using hls4ml. If everything is working correctly, you should see a print message of the FPGA resource usage for this simple design.
    Again ignore the segmentation fault warning. 
    
    You can replace the command in the quotes with any other command that you want to run within the container. 

When finishing a session, you should then stop the running container with:

```bash
docker rm -f intel_builder
```
Any files that you created or modified within the `/workspace` directory in the container will be saved to your local machine, so you will still be able to access them after stopping the container.

Just remember that when you come to the tutorial, you will need to repeat step 2 to start the container running before you can run any commands related to the build or emulation steps. 

Key takeaway for MacOS users: you can run the Jupyter notebooks and train the ML models on your local machine, and then use the wrapper scripts to run the build and emulation steps within the Docker container when you get to those parts of the tutorial.
