# Getting Started

This page gives a introduction on how to get started with ChemSchematicResolver. This assumes you already have
ChemSchematicResolver and all dependencies [**installed**](install).

## Extract Image
It's simplest to run ChemSchematicResolver on an **image** file.

Open a python terminal and import the library with: 

    >>> import chemschematicresolver as csr
    
Then run:

    >>> result = csr.extract_image('<path/to/image/file>')
    
to perform the extraction. 

This runs ChemSchematicResolver on the image and returns a list of tuples to `output`. Each tuple consists of a **SMILES string** and a list of **label candidates**, where each tuple identifies a unique structure. For example:

    >>> print(result)
    [(['1a'], 'C1CCCCC1'), (['1b'], 'CC1CCCCC1')]

## Extract Document

To automatically extract the structures and labels of diagrams from a HTML or XML article, use the `extract_document` method instead:
 
    >>> result = csr.extract_document('<path/to/document/file>')
    
If the user has permissions to access the full article, this function will download all relevant images locally to a directory called *csr*, and extract from them automatically. The *csr* directory with then be deleted.

The tool currently supports HTML documents from the [Royal Society of Chemistry](https://www.rsc.org/) and [Springer](https://www.springer.com), as well as XML files obtained using the [Elsevier Developers Portal](https://dev.elsevier.com/index.html) .

ChemSchematicResolver will return the  **chemical records** extracted by [ChemDataExtractor](www.chemdataextractor.org), enriched with structure and raw label from the image. For example:

    >>> print(result)
    {'labels': ['1a'], 'roles': ['compound'], 'melting_points': [{'value': '5', 'units': '°C'}], 'diagram': { 'smiles': 'C1CCCCC1', 'label': '1a' } }

Alternatively, if you just want the structures and labels extracted from the images without the ChemDataExtractor output, include the `extract_all` flag:

    >>> result = csr.extract_document('<path/to/document/file>', extract_all=False)
    
which, for the above example, will return:

    >>> print(output)
    [(['1a'], 'C1CCCCC1')]
