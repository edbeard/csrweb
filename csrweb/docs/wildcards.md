# Wildcard Results

When [pyosra](https://github.com/edbeard/pyosra) cannot resolve a node in a chemical diagram, it assign a __wildcard character__ `*` to the appropriate position in the output SMILES string.

ChemSchematicResolver allows the user to __ignore__ or __include__ these results using the `allow_wildcards` parameter in any `extract_` function.
 
For example:

    >>> result = csr.extract_image('<path/to/image/file>', allow_wildcards=True)
    
This will now include any outputted structures that were not completely resolved:

    >>> print(result)
    [(['1a'], 'C1CCCCC1'), (['1b'], 'CC1CCCCC1'), (['1c'], 'CC1CCCCC1*')]
    
Please note that `allow_wildcards=False` is the __default__ setting in ChemSchematicResolver.
