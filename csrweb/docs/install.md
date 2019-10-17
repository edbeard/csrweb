# Installation

This section outlines the steps required to install ChemSchematicResolver. The simplest way is to do this through [conda](https://docs.conda.io/en/latest). 

### Option 1 - Installation via Conda

Anaconda Python is a self-contained Python environment that is useful for scientific applications.

First, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) which has a complete Python distribution and the conda package manager. We recommend using Python 3.6 at this point.

Once it is installed, go to the command line terminal and type

    conda install -c edbeard chemschematicresolver
    
This command installs *ChemSchematicResolver* from the author's channel, which automatically installs all dependencies.
This includes [pyosra](https://github.com/edbeard/pyosra), the Python wrapper for the OSRA toolkit, and [ChemDataExtracor-CSR](https://github.com/edbeard/chemdataextractor-csr), the bespoke version of ChemDataExtractor containing diagram parsers.

*This method of installation is currently supported on linux machines only*

### Option 2 - Installation from source

We strongly recommend installation via conda whenever possible as all the dependencies are automatically handled. 
If this cannot be done, users are invited to compile the code from source. To do this please follow the instructions in the README files for the following github repositories, in the order below:

1. Install [Pyosra](https://github.com/edbeard/pyosra)

2. Install [ChemDataExtracor-CSR](https://github.com/edbeard/chemdataextractor-csr)

3. Install [ChemSchematicResolver](https://github.com/edbeard/ChemSchematicResolver)
