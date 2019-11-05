# Wildcard Results

When [pyosra](https://github.com/edbeard/pyosra) cannot resolve a node in a chemical diagram, it assign a wildcard character `*` to the appropriate position in the output SMILES string.

ChemSchematicResolver allows the user to ignore or include these results using the `allow_wildcards` parameter in any `extract_` function (`extract_image`, `extract_images`, `extract_document` and `extract_documents`). For example:

    >>> result = csr.extract_image('<path/to/image/file>', allow_wildcards=True)
    
This will now include any outputted structures that were not completely resolved:

    >>> print(result)
    [(['1a'], 'C1CCCCC1'), (['1b'], 'CC1CCCCC1'), (['1c'], 'CC1CCCCC1*')]
    
It is worth noting that `allow_wildcards=False` is the default setting in ChemSchematicResolver. This decision was made with the high-throughput options in mind, where there is an abundance of input data and the user is likely to want maximum precision.
