# Advanced

This section outlines a few advanced options for using ChemSchematicResolver.

### Large-scale Extraction

ChemSchematicResolver can be used for high-throughput data extraction using two methods:

    >>> ide.extract_diagrams('<path/to/img/dir>')
    >>> ide.extract_documents('<path/to/docs/dir>')  
    
These run the `extract_image` and `extract_document` methods sequentially on every file in the target directory.

ChemSchematicResolver also supports `.zip`, `.tar` and `.tar.gz` inputs.

### Using ChemSchematicResolver in workflows

*Could add some information here on how to use the SMILES stuff for further analysis?*
