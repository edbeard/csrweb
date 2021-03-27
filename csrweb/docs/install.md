# Installation

This section outlines the steps required to install ChemSchematicResolver.

Both methods use [**conda**](https://docs.conda.io/en/latest). First, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html), which contains a complete Python distribution alongside the conda package manager.

Next, go to the command line terminal and create a **working environment** by typing

    conda create --name <my_env> python=3.6
    
Once this is created, enter this environment with the command

    conda activate <my_env> 

### Option 1 - Installation via anaconda cloud

The recommended installation procedure uses the [anaconda cloud](https://anaconda.org/). Simply enter:

    conda install -c edbeard chemschematicresolver
    
This command installs ChemSchematicResolver and all its dependencies from the author's channel.
This includes [**pyosra**](https://github.com/edbeard/pyosra), the Python wrapper for the OSRA toolkit, and [**ChemDataExtractor-CSR**](https://github.com/edbeard/chemdataextractor-csr), the bespoke version of ChemDataExtractor containing diagram parsers.

Finally, download the **data files** for [ChemDataExtractor](http://chemdataextractor.org). These files contain the machine learning models, dictionaries and word clusters that ChemDataExtractor uses. This is done with the following command:

    cde data download
    
And you should have everything installed!

    
*This method of installation is currently supported on linux machines only.*


### Option 2 - Installation from source

We **strongly recommend** installation via the anaconda cloud whenever possible as all the dependencies are automatically handled. 
If this cannot be done, users are invited to compile the code from source. The easiest way to do this is using **conda build** with the recipes [here](www.github.com/edbeard/conda-recipes). 

The following packages will need to be built from a recipe, in the order below:

1. **Pyosra**: [[recipe](https://github.com/edbeard/conda-recipes/recipe/pyosra), [source code](https://github.com/edbeard/pyosra)]

2. **ChemDataExtracor-CSR**: [[recipe](https://github.com/edbeard/conda-recipes/recipe/ChemDataExtrator-CSR), [source code](https://github.com/edbeard/chemdataextractor-csr)]

3. **ChemSchematicResolver**: [[recipe](https://github.com/edbeard/conda-recipes/recipe/ChemSchematicResolver), [source code](https://github.com/edbeard/ChemSchematicResolver)]
 
For each, enter the directory and run:

    conda build .
    
to create a compressed tarball file, which contains the instructions for installing the code *(Please note that this can take up to 30 minutes to build)*.
 
Move all compressed tarballs to a single directory, enter the directory and run:

    conda index .

This changes the directory to a format emulating a conda channel. To install all code and dependencies, then simply run

    conda install -c <path/to/tarballs> chemschematicresolver
    
Finally, download the **data files** for [ChemDataExtractor](http://chemdataextractor.org). These files contain the machine learning models, dictionaries and word clusters that ChemDataExtractor uses. This is done with the following command:

    cde data download    
    
And you should have everything installed!
