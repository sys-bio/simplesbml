# simplesbml

Thank you for downloading SimpleSBML!  This package supports easy SBML model construction and editing.

The documentation can be found at: http://simplesbml.readthedocs.io/en/latest/

libSBML documentation: http://sbml.org/Software/libSBML/docs/python-api/index.html

SBML main page: http://sbml.org/Main_Page

## Versions: 

The current version is 1.3.1. Compared to 1.2.x series, this adds 'get' functions to interrogate an existing SBML model.

The difference between 1.3.0 and 1.3.1 is that the later includes get supoprt for events and rules.

1.3.2 has enhanced documentation, support for user functions, and some bug fixes

1.3.3 adds new help functions for checking amounts and concentrations. Also the class name has been capitalized to match usesal conventions in Python, so the class name is now SbmlModel.

# How to install SimpleSBML

SimpleSBML can be installed via pip:

```
pip install simplesbml
```
# Python version support

SimpleSBML in theory supports Python versions 2.7, 3.3, 3.4, 3.5, and 3.6. It definitely supports Python 3.7 and most likely 3.8. SimpleSBML is a pure Python package, but relies on libSBML, which must be compiled for each supported version.

# Help

You can go to the package documentation to read about the package's classes and methods.  For an example of how to use sbmlModel() and writeCode(), look at 'example.py' in this folder.  For other issues, report them at github.com/sys-bio/simplesbml/issues.
