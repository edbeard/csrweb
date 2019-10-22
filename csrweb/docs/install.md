# Installation

This section outlines the steps required to install ChemSchematicResolver. The simplest way is to do this through [conda](https://docs.conda.io/en/latest). 

### Option 1 - Installation via Conda

Anaconda Python is a self-contained Python environment that is useful for scientific applications.

First, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html), which contains a complete Python distribution alongside the conda package manager.

Next, go to the command line terminal and create a working environment by typing

    conda create --name <my_env> python=3.6
    
Once this is created, enter this environment with the command

    conda activate <my_env>

and install ChemSchematicResolver by typing

    conda install -c edbeard chemschematicresolver
    
This command installs ChemSchematicResolver and all it's dependencies from the author's channel.
This includes [pyosra](https://github.com/edbeard/pyosra), the Python wrapper for the OSRA toolkit, and [ChemDataExtracor-CSR](https://github.com/edbeard/chemdataextractor-csr), the bespoke version of ChemDataExtractor containing diagram parsers.

*This method of installation is currently supported on linux machines only*

**NOTE: GET THIS TO WORK ON WINDOWS / MAC BEFORE PUBLICATION?**

### Option 2 - Installation from source

We strongly recommend installation via conda whenever possible as all the dependencies are automatically handled. 
If this cannot be done, users are invited to compile the code from source. These code repositories can be found at the locations below:

1. [Pyosra](https://github.com/edbeard/pyosra)

2. [ChemDataExtracor-CSR](https://github.com/edbeard/chemdataextractor-csr)

3. [ChemSchematicResolver](https://github.com/edbeard/ChemSchematicResolver)
