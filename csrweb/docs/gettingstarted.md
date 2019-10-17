# Getting Started

This page gives a introduction on how to get started with ChemSchematicResolver. This assumes you already have
ChemSchematicResolver and all dependencies [installed](install).

## Extract Image
It's simplest to run ChemSchematicResolver on an image file.

Open a python terminal and import the library with: 

    >>> import chemschematicresolver as csr
    
Then run:

    >>> csr.extract_diagram('<path/to/image/file>')
    
to perform the extraction. 

This runs ChemSchematicResolver on the image and returns a list of tuples. Each tuple consists of a SMILES string and a list of label candidates, where each tuple identifies a unique structure.

## Extract Document

To automatically extract the structures and labels of diagrams from a HTML or XML article, use the `extract_document` method instead:
 
    >>> csr.extract_document('<path/to/document/file>')
    
ChemSchematicResolver will return the complete chemical records from the document extracted with [ChemDataExtractor](www.chemdataextractor.org), enriched with extracted diagram structure and label. 

The tool currently supports HTML documents from the [Royal Society of Chemistry](https://www.rsc.org/) and [Springer](https://www.springer.com), as well as XML files obtained using the [Elsevier Developers Portal](https://dev.elsevier.com/index.html) .
