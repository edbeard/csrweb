# Getting Started

This page gives a introduction on how to get started with ImageDataExtractor. This assumes you already have
ImageDataExtractor and ChemDataExtractor-IDE [installed](install).

## Extract Image
It's simplest to run ImageDataExtractor on an image file.

Open a python terminal and import the library with: 

    >>> import imagedataextractor as ide
    
Then run:

    >>> ide.extract_image('<path/to/image/file>')
    
to perform the extraction. 

This runs ImageDataExtractor on the image and outputs all extracted results to a single directory.

By default, the output from each image is stored in current working directory in the format `<doc#>_<doi>_<figid>_<splitfig#>` 

## Extract Document

To automatically extract microscopy images from a HTML or XML article, use the `extract_document` method instead:
 
    >>> ide.extract_document('<path/to/document/file>')
    
And that's it!

*Please note that image download may fail if the user has insufficient permissions from the article's publisher (as `extract_document` downloads directly from the distributor).*
