# Installation

This section outlines the steps required to install ImageDataExtractor. 

We **strongly** advise the use of a virtual environment when installing ImageDataExtractor (Click [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) on how to do this.)

### Step 1: Install ChemDataExtractor-IDE

In order to use ImageDataExtractor first install the bespoke version of ChemDataExtractor, ChemDataExtractor-IDE. 

ChemDataExtractor-IDE is a text-mining tool that is used to identify microscopy images from scientific documents.

First clone the repository by running:

    $ git clone https://github.com/edbeard/chemdataextractor-ide.git
    
and install with:

    $ python setup.py install
    
Then download the required machine learning models with:

    $ cde data download
    
*See https://github.com/edbeard/chemdataextractor-ide for more details*

### Step 2: Install ImageDataExtractor

To install ImageDataExtractor and all it's remaining dependencies, simply run:

    $ pip install imagedataextractor