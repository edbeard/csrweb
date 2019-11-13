# Large Scale Extraction

ChemSchematicResolver can be used for **high-throughput** data extraction using two methods.

### Extract Images

Extract all diagrams from a directory of images with `extract_images`:

    >>> result = csr.extract_images('<path/to/img/dir>')

This runs the `extract_image` method on every file in the target directory, and returns a list of the results. For example:

    >>> print(result)
    [[(['1a'], 'C1CCCCC1')], [(['1b'], 'CC1CCCCC1')]]    
    
### Extract Documents

Similarly, the `extract_documents` method can be used to extract from a directory containing multiple documents. 
    
    >>> csr.extract_documents('<path/to/docs/dir>')  
    
This also returns a list, where each element describes CSR-enriched chemical records of each article. For example:

    >>> print(result)
        [{'labels': ['1a'], 'roles': ['compound'], 'melting_points': [{'value': '5', 'units': '°C'}], 'diagram': { 'smiles': 'C1CCCCC1', 'label': '1a' } },
         {'labels': ['1b'], 'roles': ['compound'], 'melting_points': [{'value': '-126', 'units': '°C'}], 'diagram': { 'smiles': 'CC1CCCCC1', 'label': '1b' } }]
    
*The user may also use the `extract_all=False` argument with this method: see the [previous section](gettingstarted).*

ChemSchematicResolver also supports compressed directories with `.zip`, `.tar` and `.tar.gz` formats.
