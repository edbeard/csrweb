# Wildcard Results

When [pyosra](https://github.com/edbeard/pyosra) cannot resolve a node in a chemical diagram, it assigns a __wildcard character__ `*` to the appropriate position in the output SMILES string.

ChemSchematicResolver allows the user to __ignore__ or __include__ these results using the `allow_wildcards` parameter in any `extract_` function.
 
For example:

    >>> result = csr.extract_image('<path/to/image/file>', allow_wildcards=True)
    
This will now include any outputted structures that were not completely resolved:

    >>> print(result)
    [(['1a'], 'C1=CC=CC=C1'), (['1b'], 'C1=CC=CC(=C1)C'), (['1c'], 'C1=CC=CC(=C1)C*')]
    
Please note that `allow_wildcards=False` is the __default__ setting in ChemSchematicResolver.
