# Classify Single Cell Phenotypes From Images

**CytoData Society**

Image-based profiling can be used to detect mechanism of action (MOA) of small molecules.
Here, we use single cell data from [Breinig et al. 2015](https://doi.org/10.15252/msb.20156400) to classify MOA for each single cell.

Traditionally, MOAs are predicted based on well-aggregated profiles.
Here, we attempt to classify MOA of each individual single cell.

The following repository stores analytical code, data, computational environments, and pipelines to reproduce the full analysis.

## Data

Pre-processed raw data is available at: https://doi.org/10.6084/m9.figshare.10247531.v1

## (Windows users only) Set up wsl

In case you want to run the project on windows you need to setup wsl first:

### installing ubuntu
- Open 'microsoft store' and install 'ubuntu 18.04 LTS'
- Read the instruction given with this ubuntu app
- - Go in setting to 'Turn windows features on or off'
- - Check the box before 'windows Subsystem for Linux'
- - Reboot your machine

### install anaconda 
- Open the Ubuntu app
- wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
- bash Miniconda3-latest-Linux-x86_64.sh
- source ~/.bashrc
- rm Miniconda3-latest-Linux-x86_64.sh

### connect your code via vscode
- open vscode
- install extension 'remote wsl'
- In the left bottom a green box appears
- - Click it
- - Hit 'Remote WSL Reopen folder in WSL'
- - If all files have changed according to git discards these. It might change everything from unix to dos. You do NOT want that.

## Computational Environment

We use [conda](https://docs.conda.io/en/latest/) as an environment manager.
Follow [these instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to download conda.

To initialize the compute environment used in this project, run:

```bash
# Using conda version > 4.7.12
# Step 1: Create the environment
conda env create --force --file environment.yml

# Step 2: Activate the environment
conda activate cytodata-single-cell
```

## Analysis Pipeline

The analysis modules should be executed in order.
Ensure that the `cytodata-single-cell` conda environment is activated.

See [`analysis.sh`](analysis.sh) for more details.
