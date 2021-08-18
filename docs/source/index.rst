.. SimpleSBML documentation master file, created by
   sphinx-quickstart on Mon Mar 30 17:50:17 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. module:: simplesbml

=======================================================
Welcome to the SimpleSBML documentation: Version 2.0
=======================================================

This page describes the SimpleSBML package and its contents.  To install
SimpleSBML, go to
https://github.com/sys-bio/simplesbml
.

To see the documentation for libSBML, go to
http://sbml.org/Software/libSBML/docs/python-api/index.html
.

To read more about SBML (Systems Biology Markup Language), go to
http://sbml.org/Main_Page
.

--------
Overview
--------

SimpleSBML is a package that can be used to construct biological models in
SBML format using Python without interacting directly with the libSBML package.  Using
libSBML to build models can be difficult and complicated, even when the model
is relatively simple, and it can take time for a user to learn how to use the
package properly.  This package is intended as an intuitive interface for
users who are not already familiar with libSBML.  It can be used to construct
models with only a few lines of code, print out the resulting models in SBML
format, and edit existing models in SBML format.

--------
Examples
--------

Example models are taken from the SBML Level 3 Version 1 documentation.

Here is an example of a simple reaction-based model built with SbmlModel::

    import simplesbml
    model = simplesbml.SbmlModel()
    model.addCompartment(1e-14, comp_id='comp')
    model.addSpecies('E', 5e-21, comp='comp')
    model.addSpecies('S', 1e-20, comp='comp')
    model.addSpecies('P', 0.0, comp='comp')
    model.addSpecies('ES', 0.0, comp='comp')
    model.addReaction(['E', 'S'], ['ES'], 'comp*(kon*E*S-koff*ES)', local_params={'koff': 0.2, 'kon': 1000000.0}, rxn_id='veq')
    model.addReaction(['ES'], ['E', 'P'], 'comp*kcat*ES', local_params={'kcat': 0.1}, rxn_id='vcat')

In this example, reaction rate constants are stored locally with the reactions where they are used.  It is also possible to define global parameters and use them in reaction expressions.  Here is an example of using global parameters which is the most common use case::

    import simplesbml
    model = simplesbml.SbmlModel()
    model.addCompartment(1e-14, comp_id='comp')
    model.addSpecies('E', 5e-21, comp='comp')
    model.addSpecies('S', 1e-20, comp='comp')
    model.addSpecies('P', 0.0, comp='comp')
    model.addSpecies('ES', 0.0, comp='comp')
    model.addParameter('koff', 0.2)
    model.addParameter('kon', 1000000.0)
    model.addParameter('kcat', 0.1)
    model.addReaction(['E', 'S'], ['ES'], 'comp*(kon*E*S-koff*ES)', rxn_id='veq')
    model.addReaction(['ES'], ['E', 'P'], 'comp*kcat*ES', rxn_id='vcat')

SbmlModel also supports the use of events to change the system state under certain conditions, use of assignment rules and rate rules to explicitly 
define variable values as a function of the system state.  Here is an example of events and rate rules. In this example, the value of parameter G2 
is determined by the relationship between P1 and tau, and the rates of change of P1 and P2 are explicitly defined in equation form 
instead of with a reaction::

    import simplesbml
    model = simplesbml.SbmlModel()
    model.addCompartment(vol=1.0, comp_id='cell')
    model.addSpecies('[P1]', 0.0, comp='cell')
    model.addSpecies('[P2]', 0.0, comp='cell')
    model.addParameter('k1', 1.0)
    model.addParameter('k2', 1.0)
    model.addParameter('tau', 0.25)
    model.addParameter('G1', 1.0)
    model.addParameter('G2', 0.0)
    model.addEvent(trigger='P1 > tau', assignments={'G2': '1'})
    model.addEvent(trigger='P1 <= tau', assignments={'G2': '0'})
    model.addRateRule('P1', 'k1 * (G1 - P1)')
    model.addRateRule('P2', 'k2 * (G2 - P2)')

Users can edit existing models with the writeCode() method which accepts an SBML document and produces a script of 
SimpleSBML commands in string format.  This method converts the SBML document into a libSBML Model and scans through 
its elements, adding lines of code for each SimpleSBML-compatible element it finds.  The output can be saved to a .py file 
and edited to create new models based on the original import. This can be very useful for editing existing SBML models.  For instance,
here is an example of a short script that reproduces the SimpleSBML to reproduce an SbmlModel object::

    import simplesbml
    model = simplesbml.SbmlModel()
    model.addCompartment(1e-14, comp_id='comp')
    model.addSpecies('E', 5e-21, comp='comp')
    model.addSpecies('S', 1e-20, comp='comp')
    model.addSpecies('P', 0.0, comp='comp')
    model.addSpecies('ES', 0.0, comp='comp')
    model.addReaction(['E', 'S'], ['ES'], 'comp*(kon*E*S-koff*ES)', local_params={'koff': 0.2, 'kon': 1000000.0}, rxn_id='veq')
    model.addReaction(['ES'], ['E', 'P'], 'comp*kcat*ES', local_params={'kcat': 0.1}, rxn_id='vcat')

    # Load the sbml model and output the equivalent simplesbml scipt
    code = simplesbml.writeCodeFromString(model.toSBML())
    f = open('example_code.py', 'w')
    f.write(code)
    f.close()

The output saved to 'example_code.py' will look like this::

    import simplesbml
    model = simplesbml.SbmlModel(sub_units='')
    model.addCompartment(vol=1e-14, comp_id='comp')
    model.addSpecies(species_id='E', amt=5e-21, comp='comp')
    model.addSpecies(species_id='S', amt=1e-20, comp='comp')
    model.addSpecies(species_id='P', amt=0.0, comp='comp')
    model.addSpecies(species_id='ES', amt=0.0, comp='comp')
    model.addReaction(reactants=['E', 'S'], products=['ES'], expression='comp * (kon * E * S - koff * ES)', local_params={'koff': 0.2, 'kon': 1000000.0}, rxn_id='veq')
    model.addReaction(reactants=['ES'], products=['E', 'P'], expression='comp * kcat * ES', local_params={'kcat': 0.1}, rxn_id='vcat')

Examples of Interrogating an Existing Model
============================================

Verison 2.0 has a set of new 'get' methods that allows a user to easily interrogate a model for its contents.::

    import simplesbml
    mymodel = loadFromFile ('mymodel.xml')  # Load the model into a string variable
    model = simplesbml.loadSBMLStr(mymodel)

    # Or:

    model = simplesbml.loadSBMLFile('mymodel.xml')

    # Or if you're using the Tellurium package:

    model = simplesbml.loadSBMLStr(r.getSBML())    
  
    print ('Num compartmetns = ', model.getNumCompartmentIds())
    print ('Num parameters =', model.getNumParameters())
    print ('Num species =', model.getNumSpecies())
    print ('Num floating species = ', model.getNumFloatingSpecies())
    print ('Num floating species = ', model.getNumBoundarySpecies())
    print ('Num reactions = ', model.getNumReactions())
    print (model.getListOfCompartments())
    print (model.getListOfAllSpecies())
    print ('list of floating species = ', model.getListOfFloatingSpecies())
    print ('list of boundary species = ', model.getListOfBoundarySpecies())
    print ('List of reactions = ', model.getListOfReactionIds())
    print ('List of rules = ', model.getListOfRuleIds())

Here is an example script that uses simplesbml to create a stoichiometry matrix for a model::

    import tellurium as te, simplesbml, numpy as np

    r = te.loada("""
    S0 + S3 -> S2; k0*S0*S3;
    S3 + S2 -> S0; k1*S3*S2;
    S5 -> S2 + S4; k2*S5;
    S0 + S1 -> S3; k3*S0*S1;
    S5 -> S0 + S4; k4*S5;
    S0 -> S5; k5*S0;
    S1 + S1 -> S5; k6*S1*S1;
    S3 + S5 -> S1; k7*S3*S5;
    S1 -> $S4 + S4; k8*S1;

    S0 = 0; S1 = 0; S2 = 0; S3 = 0; S4 = 0; S5 = 0;
    k0 = 0; k1 = 0; k2 = 0; k3 = 0; k4 = 0
    k5 = 0; k6 = 0; k7 = 0; k8 = 0
    """)

    model = simplesbml.loadSBMLStr(r.getSBML())

    # Allocate space for the stoichiometry matrix
    stoich = np.zeros((model.getNumFloatingSpecies(), model.getNumReactions()))
    for i in range (model.getNumFloatingSpecies()):
        floatingSpeciesId = model.getNthFloatingSpeciesId (i)
        
        for j in range (model.getNumReactions()):
            productStoichiometry = 0; reactantStoichiometry = 0

            numProducts = model.getNumProducts (j)
            for k1 in range (numProducts):
                productId = model.getProduct (j, k1)

                if (floatingSpeciesId == productId):
                   productStoichiometry += model.getProductStoichiometry (j, k1)

            numReactants = model.getNumReactants(j)
            for k1 in range (numReactants):
                reactantId = model.getReactant (j, k1)
                if (floatingSpeciesId == reactantId):
                   reactantStoichiometry += model.getReactantStoichiometry (j, k1)

            st = int(productStoichiometry - reactantStoichiometry)
            stoich[i,j] = st
        
    print (stoich)

-------------------
Tests and Examples
-------------------

Two test files can be found in the tests folder. The runTest.py is the more formal testing file. It was decided not to use the Python unittest due to its limitations 
and pyTest simply made the code unmanagable. A simple test system was therefore created. To run the tests just execute runTests.py or more simply::

    simplesbml.tests.run()

Make sure you have libsbml or Tellurium installed (it can provide libsbml).

-------------------
Classes and Methods
-------------------

.. automodule:: simplesbml
   :members:
   :member-order: bysource

