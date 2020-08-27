import warnings

# try to import tesbml or libsbml
# if both of these fail, libsbml cannot be imported - cannot continue
try:

    import tesbml as libsbml   
except ImportError:
    import libsbml

from math import isnan
from re import sub
import os

# Version info is in __init__.py

def _isSBMLModel(obj):
  """
  Tests if object is a libsbml model
  """
  cls_stg = str(type(obj))
  if ('Model' in cls_stg) and ('lib' in cls_stg):
    return True
  else:
    return False

def _checkSBMLDocument(document): 
  if (document.getNumErrors() > 0):
    raise ValueError("Errors in SBML document")

class sbmlModel(object):

    """   
    sbmlModel is used to construct simple models using libSBML methods and
    print out the model in SBML format.  A user can add species, parameters,
    reactions, events, assignment rules, rate rules, and initial assignments
    to a model.  Then, the user can view the model in SBML format by printing
    the string representation of the class.

    sbmlModel contains two attributes: *document*, an
    `SBMLDocument <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_s_b_m_l_document.html>`_
    object, an
    *model*, the
    `Model <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_model.html>`_
    attribute of *document*.
    
    You can also pass a SBML string and use simlesbml to obtain information about the model
    using the get methods, e.g
       
    model = simplesbml.sbmlModel (sbmlStr=mySBMLString)
    """

    def __init__(self, time_units='second', extent_units='mole', \
                 sub_units='mole', level=3, version=1, sbmlStr=None, sbmlFile=None):
        if level == 1:
            raise SystemExit('Error: SimpleSBML does not support SBML level 1')
        try:
            self.document = libsbml.SBMLDocument(level,version)
        except ValueError:
            raise SystemExit('Could not create SBMLDocument object')
        
        if (sbmlFile != None) and (sbmlStr != None):
           raise Exception.Create ('Only select a string or file as the source of the SBML, not both')

        if (sbmlFile == None) and (sbmlStr == None): # They want to create a new model
            self.model = self.document.createModel()
            self._check(self.model, 'create model')
            if self.document.getLevel() == 3:
                self._check(self.model.setTimeUnits(time_units), 'set model-wide time units')
                self._check(self.model.setExtentUnits(extent_units), 'set model units of extent')
                self._check(self.model.setSubstanceUnits(sub_units),'set model substance units')

            per_second = self.model.createUnitDefinition()
            self._check(per_second,                         'create unit definition')
            self._check(per_second.setId('per_second'),     'set unit definition id')
            unit = per_second.createUnit()
            self._check(unit,                               'create unit on per_second')
            self._check(unit.setKind(libsbml.UNIT_KIND_SECOND),     'set unit kind')
            self._check(unit.setExponent(-1),               'set unit exponent')
            self._check(unit.setScale(0),                   'set unit scale')
            self._check(unit.setMultiplier(1),              'set unit multiplier')

            self.addCompartment()
        else:
            if sbmlStr != None:
                reader = libsbml.SBMLReader()  
                self.document = reader.readSBMLFromString(sbmlStr)

            if sbmlFile != None:
                if os.path.isfile(sbmlFile):
                   with open(sbmlFile, 'r') as fd:
                        xml = fd.read()
                   reader = libsbml.SBMLReader()  
                   self.document = reader.readSBMLFromString(xml)
                else:
                   raise Exception ('Specified file name does not appear to be a file?')    

            _checkSBMLDocument(self.document)
            self.model = self.document.getModel()
             
    def _check(self, value, message):
        if value == None:
            raise SystemExit('LibSBML returned a null value trying to ' + \
                    message + '.')
        elif type(value) is int:
            if value == libsbml.LIBSBML_OPERATION_SUCCESS:
                return
            else:
                err_msg = 'Error trying to ' + message + '.' \
                + 'LibSBML returned error code ' + str(value) + ': "'\
                + libsbml.OperationReturnValue_toString(value).strip() + '"'
            raise RuntimeError(err_msg)
        else:
            return

    def addCompartment(self, vol=1, comp_id=''):
        """Adds a `Compartment <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_compartment.html>`_
        of volume *vol* litres to the model.  The default volume is 1 litre. If the user does
        not specify *comp_id*, the id is set to 'c<n>' where the new compartment
        is the nth compartment added to the model. All sbmlModel objects are
        initialized with a default compartment 'c1'."""

        c1 = self.model.createCompartment()
        self._check(c1,                                 'create compartment')
        if len(comp_id) == 0:
            comp_id = 'c' + str(self.model.getNumCompartments())
        self._check(c1.setId(comp_id),                     'set compartment id')
        self._check(c1.setConstant(True),               'set compartment "constant"')
        self._check(c1.setSpatialDimensions(3),         'set compartment dimensions')

        self._check(c1.setSize(vol),                      'set compartment "size"')
        self._check(c1.setUnits('litre'),               'set compartment size units')
        return c1

    def addSpecies(self, species_id, amt, comp='c1'):
        
        """Adds a `Species <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_species.html>`_
        to the model.  If *species_id* starts
        with the '$' symbol, the species is set as a boundary condition.  If
        *species_id* is enclosed in brackets, the *amt* is the initial
        concentration of species within the specified compartment in mol/L.
        Otherwise, *amt* is the initial amount of species in moles."""

        s1 = self.model.createSpecies()
        self._check(s1,                           'create species s1')
        self._check(s1.setCompartment(comp),      'set species s1 compartment')
        if species_id[0] == '[' and species_id[len(species_id)-1] == ']':
            self._check(s1.setInitialConcentration(amt),    'set initial concentration for s1')
            species_id = species_id[1:(len(species_id)-1)]
        else:
            self._check(s1.setInitialAmount(amt),     'set initial amount for s1')
        self._check(s1.setSubstanceUnits(self.model.getSubstanceUnits()), 'set substance units for s1')
        if species_id[0] == '$':
            self._check(s1.setBoundaryCondition(True), \
                    'set "boundaryCondition" on s1')
            self._check(s1.setConstant(False), 'set "constant" attribute on s1')
            self._check(s1.setId(species_id[1:len(species_id)]), 'set species s1 id')
        else:
            self._check(s1.setBoundaryCondition(False), \
                    'set "boundaryCondition" on s1')
            self._check(s1.setConstant(False), 'set "constant" attribute on s1')
            self._check(s1.setId(species_id),  'set species s1 id')
        self._check(s1.setHasOnlySubstanceUnits(False), \
                'set "hasOnlySubstanceUnits" on s1')
        return s1

    def addParameter(self, param_id, val, units='per_second'):      
        """Adds a `Parameter <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_parameter.html>`_
        to the model.  *val* is the value of the parameter, and
        *param_id* is the parameter id.  If units are not specified by the user,
        the default units are 1/sec."""

        k = self.model.createParameter()
        self._check(k,                        'create parameter k')
        self._check(k.setId(param_id),        'set parameter k id')
        self._check(k.setConstant(False),      'set parameter k "not constant"')
        self._check(k.setValue(val),          'set parameter k value')
        self._check(k.setUnits(units), 'set parameter k units')
        return k

    def addReaction(self, reactants, products, expression, local_params={}, rxn_id=''):      
        """Adds a `Reaction <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_reaction.html>`_
        to the model.

        *reactants* and *products* are lists of species
        ids that the user wishes to define as reactants and products, respectively.
        If one of these lists contains a string with a number followed by a species
        id (i.e. '2 G6P') then the number is interpreted as the stoichiometry of
        the species.  Otherwise it is assumed to be 1.

        *expression* is a string that represents the reaction rate expression.

        *local_params* is a dictionary where the keys are local parameter ids and
        the values are the desired values of the respective parameters.

        If the
        user does not define a reaction id, it is set as 'v<n>' where the new
        reaction is the nth reaction added."""

        r1 = self.model.createReaction()
        self._check(r1,                         'create reaction')
        if len(rxn_id) == 0:
            rxn_id = 'v' + str(self.model.getNumReactions())
        self._check(r1.setId(rxn_id),           'set reaction id')
        self._check(r1.setReversible(False),    'set reaction reversibility flag')
        self._check(r1.setFast(False),          'set reaction "fast" attribute')

        for re in reactants:
            if re is not None and '$' in re:
                re.translate(None, '$')
            re_split = re.split()
            if len(re_split) == 1:
                sto = 1.0
                re_id = re
            elif len(re_split) == 2 and re_split[0].isdigit():
                sto = float(re_split[0])
                re_id = re_split[1]
            else:
                err_msg = 'Error: reactants must be listed in format \'S\' or \'(float)\' S\''
                raise SystemExit(err_msg)
            s1 = self.model.getSpecies(re_id)
            species_ref1 = r1.createReactant()
            self._check(species_ref1,                       'create reactant')
            self._check(species_ref1.setSpecies(s1.getId()), \
                    'assign reactant species')
            self._check(species_ref1.setStoichiometry(sto), \
                    'assign reactant stoichiometry')
            if self.document.getLevel() == 3:
                self._check(species_ref1.setConstant(True), \
                    'set "constant" on species ref 1')

        for pro in products:
            if pro is not None and '$' in pro:
                pro.translate(None, '$')
            pro_split = pro.split()
            if len(pro_split) == 1:
                sto = 1.0
                pro_id = pro
            elif len(pro_split) == 2:
                sto = float(pro_split[0])
                pro_id = pro_split[1]
            else:
                err_msg = 'Error: products must be listed in format \'S\' or \'(float)\' S\''
                raise SystemExit(err_msg)
            s2 = self.model.getSpecies(pro_id)
            species_ref2 = r1.createProduct()
            self._check(species_ref2, 'create product')
            self._check(species_ref2.setSpecies(s2.getId()), \
                    'assign product species')
            self._check(species_ref2.setStoichiometry(sto), \
                    'set product stoichiometry')
            if self.document.getLevel() == 3:
                self._check(species_ref2.setConstant(True), \
                    'set "constant" on species ref 2')

        math_ast = libsbml.parseL3Formula(expression)
        self._check(math_ast,    'create AST for rate expression')

        kinetic_law = r1.createKineticLaw()
        self._check(kinetic_law,                   'create kinetic law')
        self._check(kinetic_law.setMath(math_ast), 'set math on kinetic law')
        for param in local_params.keys():
            val = local_params.get(param)
            if self.document.getLevel() == 3:
                p = kinetic_law.createLocalParameter()
            else:
                p = kinetic_law.createParameter()
            self._check(p, 'create local parameter')
            self._check(p.setId(param), 'set id of local parameter')
            self._check(p.setValue(val),   'set value of local parameter')
        return r1

    def addEvent(self, trigger, assignments, persistent=True, \
                 initial_value=False, priority=0, delay=0, event_id=''):           
        """Adds an `Event <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_event.html>`_
        to the model.

        *trigger* is the string representation of a
        logical expression that defines when an event is 'triggered', meaning
        when the event is ready to be executed.

        *delay* is a numerical value that defines the amount of time between when
        the event is triggered and when the event assignment is implemented, in
        previously defined model-wide time units.

        *assignments* is a dictionary
        where the keys are variables to be changed and the values are the
        variables' new values.

        *persistent* is a boolean that defines whether the
        event will still be executed if the trigger switches from ``True`` to ``False``
        between the event's trigger and its execution.

        *initial_value* is the value of *trigger* when t < 0.

        *priority* is a numerical value that determines
        which event is executed if two events are executed at the same time.  The
        event with the larger ``priority`` is executed.

        .. note:: An event is only triggered when the trigger switches from ``False`` to
            ``True``.  If the trigger's initial value is ``True``, the event will not be
            triggered until the value switches to ``False`` and then back to ``True``."""

        e1 = self.model.createEvent()
        self._check(e1,     'create event')
        if len(event_id) == 0:
            event_id = 'e' + str(self.model.getNumEvents())
        self._check(e1.setId(event_id),    'add id to event')
        if self.document.getLevel()==3 or (self.document.getLevel()==2 \
                    and self.document.getVersion()==4):
            self._check(e1.setUseValuesFromTriggerTime(True), 'set use values from trigger time')

        tri = e1.createTrigger()
        self._check(tri,  'add trigger to event')
        tri_ast = libsbml.parseL3Formula(trigger)
        self._check(tri.setMath(tri_ast),     'add formula to trigger')
        if self.document.getLevel() == 3:
            self._check(tri.setPersistent(persistent),   'set persistence of trigger')
            self._check(tri.setInitialValue(initial_value), 'set initial value of trigger')

        de = e1.createDelay()
        if self.document.getLevel() == 3:
            k = self.addParameter(event_id+'Delay', delay, self.model.getTimeUnits())
        else:
            k = self.addParameter(event_id+'Delay', delay, 'time')
        self._check(de,               'add delay to event')
        delay_ast = libsbml.parseL3Formula(k.getId())
        self._check(de.setMath(delay_ast),     'set formula for delay')

        for a in assignments.keys():
            assign = e1.createEventAssignment()
            self._check(assign,   'add event assignment to event')
            self._check(assign.setVariable(a),  'add variable to event assignment')
            val_ast = libsbml.parseL3Formula(assignments.get(a))
            self._check(assign.setMath(val_ast),    'add value to event assignment')

        if self.document.getLevel() == 3:
            pri = e1.createPriority()
            pri_ast = libsbml.parseL3Formula(str(priority))
            self._check(pri.setMath(pri_ast), 'add priority to event')
        return e1

    def addAssignmentRule(self, var, math):
        
        """Adds an `AssignmentRule <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_assignment_rule.html>`_
        to the model.  An assignment rule is an equation
        where one side is equal to the value of a state variable and the other side
        is equal to some expression.  *var* is the id of the state variable and *math*
        is the string representation of the expression."""

        r = self.model.createAssignmentRule()
        self._check(r,                        'create assignment rule r')
        self._check(r.setVariable(var),          'set assignment rule variable')
        math_ast = libsbml.parseL3Formula(math)
        self._check(r.setMath(math_ast), 'set assignment rule equation')
        return r

    def addRateRule(self, var, math):
 
        """Adds a `RateRule <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_rate_rule.html>`_
        to the model.  A rate rule is similar to an assignment
        rule, but instead of describing a state variable's value as an
        expression, it describes the derivative of the state variable's value
        with respect to time as an expression.  *var* is the id of the state variable
        and *math* is the string representation of the expression."""

        r = self.model.createRateRule()
        self._check(r,                        'create rate rule r')
        self._check(r.setVariable(var),          'set rate rule variable')
        math_ast = libsbml.parseL3Formula(math)
        self._check(r.setMath(math_ast), 'set rate rule equation')
        return r

    def addInitialAssignment(self, symbol, math):
        
        """Adds an `InitialAssignment <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_initial_assignment.html>`_
        to the model.  If the
        initial value of a variable depends on other variables or parameters, this
        method can be used to define an expression that describes the initial value
        of the variable in terms of other variables or parameters.  *symbol* is the
        id of the variable and *math* is the string representation of the expression."""

        if self.document.getLevel() == 2 and self.document.getVersion() == 1:
            raise SystemExit('Error: InitialAssignment does not exist for \
                    this level and version.')
        a = self.model.createInitialAssignment()
        self._check(a,   'create initial assignment a')
        self._check(a.setSymbol(symbol),    'set initial assignment a symbol')
        math_ast = libsbml.parseL3Formula(math)
        self._check(a.setMath(math_ast),    'set initial assignment a math')
        return a

    def setLevelAndVersion(self, level, version):
        if level == 2 and version == 1:
            self._check(self.document.checkL2v1Compatibility(), 'convert to level 2 version 1')
        elif level == 2 and version == 2:
            self._check(self.document.checkL2v2Compatibility(), 'convert to level 2 version 2')
        elif level == 2 and version == 3:
            self._check(self.document.checkL2v3Compatibility(), 'convert to level 2 version 3')
        elif level == 2 and version == 4:
            self._check(self.document.checkL2v4Compatibility(), 'convert to level 2 version 4')
        elif level == 3 and version == 1:
            self._check(self.document.checkL3v1Compatibility(), 'convert to level 3 version 1')
        else:
            raise SystemExit('Invalid level/version combination')

        isSet = self.document.setLevelAndVersion(level, version)
        self._check(isSet, 'convert to level ' + str(level) + ' version ' + str(version))

    def getDocument(self):
        
        """Returns the
        `SBMLDocument <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_s_b_m_l_document.html>`_
        object of the sbmlModel. 

        This is not something you need to care about unless you need direct access to libsbml"""
        return self.document

    def getModel(self):
        """Returns the
        `Model <http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_model.html>`_
        object of the sbmlModel.

        This is not something you need to care about unless you need direct access to libsbml"""
        return self.model

    def getNumCompartments (self):
        """
        Returns the number of compartments in the current model.
        """
        return self.model.getNumCompartments()   
       
    def getNumSpecies (self):
        """
        Returns the number of all species in the current model.
        """
        return self.model.getNumSpecies()

    def getNumParameters (self):
        """
        Returns the number of global parameters in the current model.
        """        
        return self.model.getNumParameters()
    
    def getNumReactions (self):
        """
        Returns the number of reactions in the current model.
        """        
        return self.model.getNumReactions()

    def getNumEvents (self):
        """
        Returns the number of events in the current model.
        """        
        return self.model.getNumEvents()    

    def getNumRules (self):
        """
        Returns the number of rules in the current model.
        """        
        return self.model.getNumRules()  

    def getNumFunctionDefinitions (self):
        """
        Returns the number of function definitions in the current model.
        """        
        return self.model.getNumFunctionDefinitions()
    
    def getNumInitialAssignments (self):
        """
        Returns the number of initial assignments in the current model.
        """        
        return self.model.getNumInitialAssignments() 
    
    #def getSpecies(self, species_id):      
    #    return self.model.getSpecies(species_id)

    def getListOfCompartments(self):
        """
        Returns a list of compartment Ids
        """
        alist = []
        nCompartments = self.model.getNumCompartments()
        for i in range (nCompartments):
           comp = self.model.getCompartment(i)
           alist.append (comp.getId())
        return alist
    
    def getCompartmentVolume (self, Id):
        """
        **Parameters**
        
           Id: The Id of the compartment in question
           
        **Returns**
        
           The volume of the specified compartment
        """
        p = self.model.getCompartment(Id)
        if p != None:
           return p.getVolume()
        raise Exception ('Compartment does not exist')       
     
        
    def getListOfAllSpecies(self):
        """
        Returns a list of **ALL** species Ids in the model
        """
        alist = []
        nSpecies = self.model.getNumSpecies()
        for i in range (nSpecies):
           sp = self.model.getSpecies(i)
           alist.append (sp.getId())         
        return alist
    
    def isSpeciesValueSet (self, Id):
        """
        Returns true if the species has been set a value (concentration or amount).

        Example: if model.isSpeciesValueSet ('ATP'):
        """
        p = self.model.getSpecies(Id)
        if p == None:
           raise Exception ('Species does not exist')  
        if p.isSetInitialConcentration() or p.isSetInitialAmount():
            return True
        else:
            return False

    def getSpeciesInitialConcentration (self, Id):
        """
        Returns the initial values for the concentration of a species with given Id

        The species can be an index to the indexth species or the Id of the species. You can get the Ids by calling getListOfSpecies()

        Example: value = model.getSpeciesInitialConcentration ('Glucose')
        """
        p = self.model.getSpecies(Id)
        if p == None:
           raise Exception ('Species does not exist')             
        if p.isSetInitialConcentration() == True:
           return p.getInitialConcentration()
        else:
           raise Exception ('Species has not been initialized with a concentration')
        

    def getSpeciesInitialAmount (self, Id):
        """
        Returns the initial values for the amount of a species with given Id

        The species can be an index to the indexth species or the Id of the species. You can get the Ids by calling getListOfSpecies()

        Example: value = model.getSpeciesInitialAmount ('Glucose')
        """
        p = self.model.getSpecies(Id)
        if p == None:
           raise Exception ('Species does not exist')   
        if p.isSetInitialAmount():
           return p.getInitialAmount()
        else:
           raise Exception ('Species has not been initialized with an amount') 
         
    def getListOfFloatingSpecies(self):
        """
        Returns a list of all floating species Ids.
        """
        alist = []
        nSpecies = self.model.getNumSpecies()
        for i in range (nSpecies):
            sp = self.model.getSpecies(i)
            if not sp.getBoundaryCondition():
               alist.append (sp.getId())         
        return alist    

    def getListOfBoundarySpecies(self):
        """
        Returns a list of all boundary species Ids.
        """
        alist = []
        nSpecies = self.model.getNumSpecies()
        for i in range (nSpecies):
            sp = self.model.getSpecies(i)            
            if sp.getBoundaryCondition():
               alist.append (sp.getId())         
        return alist  
    
    def getNumFloatingSpecies (self):
        """
        Returns the number of floating species.
        """
        return len (self.getListOfFloatingSpecies())

    def getNumBoundarySpecies (self):
        """
        Returns the number of boundary species.
        """
        return len (self.getListOfBoundarySpecies())
    
    #def getParameter(self, param_id):
    #    return self.model.getParameter(param_id)

    def getListOfParameters(self):
        """
        Returns a list of all global parameter Ids in the model.
        """
        alist = []
        nParameters = self.model.getNumParameters() 
        for i in range (nParameters):
            p = self.model.getParameter(i)
            alist.append (p.getId())             
        return alist

    
    def isParameterValueSet (self, Id):
        """
        Returns true if the parameter has been assigned a value

        Example: if model.isParameterValueSet ('k1'):

        """
        p = self.model.getParameter(Id)
        if p == None:
           raise Exception ('Parameter does not exist')  
        if p.isSetValue():
            return True
        else:
            return False

    def getParameterValue (self, Id):
        """
        Returns the value for a given model parameter.

        **Parameters**
        
           Id: the Id of the parameter in question

        Example: value = model.getParameterValue ('k1')       
        """      
        p = self.model.getParameter(Id)
        if p.isSetValue():
           return p.getValue()
        raise Exception ('Parameter does not exist')      
        
    def getListOfReactions(self):
        """
        Returns a list of all reaction Ids.
        """       
        alist = []
        nReactions = self.model.getNumReactions() 
        for i in range (nReactions):
            p = self.model.getReaction(i)
            alist.append (p.getId())             
        return alist
    
    def getNumReactants (self, Id):
        """
         Returns the number of reactants in the reaction given by the Id argument.

        **Parameters**
        
           Id (string): The Id of the reaction in question.

        Example: numProducts = model.getNumReactants ('J1')
        """ 
        p = self.model.getReaction(Id)
        if p != None:
           return p.getNumReactants()
        raise Exception ('Reaction does not exist')  
        
    def getNumProducts (self, Id):
        """
        Returns the number of products in the reaction given by the Id argument.

        **Parameters**
        
           Id (string): The Id of the reaction in question.
           
        Example: numProducts = model.getNumProducts ('J1')
        """ 
        p = self.model.getReaction(Id)
        if p != None:
           return p.getNumProducts()
        raise Exception ('Reaction does not exist') 
        
    def getRateLaw (self, Id):
        """
        Returns the expression for the rate laws of the reaction given by the specified Id

        **Parameters**
        
           Id (string): The Id of the reaction in question.
  
        Example: formulaStr = model.getRateLaw ('J1')
        """ 
        p = self.model.getReaction(Id)
        if p != None:
           return p.getKineticLaw().getFormula()
        raise Exception ('Reaction does not exist')      
              
    def getReactant (self, reactionId, reactantIndex):
        """
        Returns the Id of the reactantIndexth reactant in the reaction given by the reactionId

        **Parameters**
        
           Id (string): The Id of the reaction in question
           
           reactantIndex (int): The ith reactant in the reaction

        Example: astr = model.getReactant ('J1', 0)
        """ 
        ra = self.model.getReaction(reactionId)
        sr = ra.getReactant(reactantIndex)
        return sr.getSpecies()
    
    def getProduct (self, reactionId, productIndex):
        """
        Returns the Id of the productIndexth product in the reaction given by the reactionId

        **Parameters**
        
           Id (string): The Id of the reaction in question
           
           productIndex (int): The ith product in the reaction

        Example: astr = model.getProduct ('J1', 0)
        """ 
        ra = self.model.getReaction(reactionId)
        sr = ra.getProduct(productIndex)
        return sr.getSpecies()
    
    def getReactantStoichiometry (self, reactionId, reactantIndex):
        """
        Returns the stoichiometry for a reactant in a reaction.

        **Parameters**
        
           reactionId (string): The Id of the reaction in question
           
           reactantIndex (int): The ith reactant in the reaction
           
        **Returns**
        
           The value of the reactant stoichiometry

        Example: stInt = model.getReactantStoichiometry ('J1', 0)
        """         
        ra = self.model.getReaction(reactionId)
        sr = ra.getReactant(reactantIndex)
        return sr.getStoichiometry ()

    def getProductStoichiometry (self, reactionId, productIndex):
        """
        Returns the stoichiometry for a product in a reaction.

        **Parameters**
        
           reactionId (string): The Id of the reaction in question
           
           productIndex (int): The ith product in the reaction
           
        **Returns**
        
           The value of the product stoichiometry

        Example: stInt = model.getProductStoichiometry ('J1', 0)
        """
        ra = self.model.getReaction(reactionId)
        sr = ra.getProduct(productIndex)
        return sr.getStoichiometry ()
        
    def getListOfRules(self):
        """
        Returns a list of Ids for the rules
        """ 
        alist = []
        nRules = self.model.getNumRules() 
        for i in range (nRules):
            p = self.model.getRule(i)
            alist.append (p.getId())             
        return alist
    
    def getRuleId (self, index):
        """
        Returns the rule Id of the indexth rule

        Example: rule = model.getRuleId (2)
        """         
        return self.model.getRule (index).getId()

    def getRuleRightSide (self, rule):
        """
        Returns the formula on the right-hand side of the rule in question.

        The rule can be an index to the indexth rule or the Id of the rule. You can get the Ids by calling getListOfRules()

        Example: formula = model.getRuleRightSide (0)
        """
        return self.model.getRule (rule).getFormula()

    def getRuleType (self, rule):
        """
        Returns a string indicating the type of rule in question.

        The rule can be an index to the indexth rule or the Id of the rule. You can get the Ids by calling getListOfRules()

        Example: ruleStr = model.getRuleType (0)
        """
        myRule = self.model.getRule (rule)
        t1 = myRule.getTypeCode()
        if t1 == libsbml.SBML_RATE_RULE:
           return 'ODE (or rate) rule' 
        if t1 == libsbml.SBML_ASSIGNMENT_RULE:
           return 'Assignment rule' 
        if t1 == libsbml.SBML_ALGEBRAIC_RULE:
           return 'Algebraic rule' 
        raise Exception ('Unknown rule in SBML model')

    def getEventId (self, index):
        """
        Returns the Id for the indexth event

        Example: astr = model.getEventId (0)
        """
        return self.model.getEvent (index).getId()

    def getEventString (self, event):
        """
        Returns the indexth event as a compelte string.

        The event argument can be an index to the indexth event or the Id of the event  

        Example: print (model.getEventString (0))
        """
        myEvent = self.model.getEvent (event)
        astr = 'at ' + self.getEventTrigger (event) + ' then { '
        num = myEvent.getNumEventAssignments()
        astr = astr + self.getEventVariable (event, 0) + ' = ' + self.getEventAssignment (event, 0)
        for i in range (1, num):
            astr = astr + '; ' + self.getEventVariable (event, i) + ' = ' + self.getEventAssignment (event, i)
        astr = astr + ' }'
        return astr
        
    def getEventTrigger (self, event):
        """
        Returns the formula as a string for the event trigger of the event event.

        The event argument can be an index to the indexth event or the Id of the event

        Example : astr = model.getEventTrigger (0)
        """
        myEvent = self.model.getEvent(event)
        trig = myEvent.getTrigger()        
        return libsbml.formulaToL3String (trig.getMath())

    def getNumEventAssignments (self, index):
        """
        Returns the number of assignments in the indexth rule.
        """
        event = self.model.getEvent(index)
        return event.getNumEventAssignments()

    def getEventVariable (self, event, assignmentIndex):
        """
        Returns the event variables (i.e the left-hand side) for the assignmentIndexth assignment
        in the event, given by event,

        The event argument can be an index to the indexth event or the Id of the event

        Example: astr = model.getEventVariable (0, 0)
        """
        myEvent = self.model.getEvent(event)
        eventAss = myEvent.getEventAssignment(assignmentIndex)  
        return eventAss.getVariable()

    def getEventAssignment (self, event, assignmentIndex):
        """
        Retuns the assignmentIndexth assignment in the event event.

        The event argument can be an index to the indexth event or the Id of the event   

        Example: mathStr = model.getEventAssignment (1, 0)     
        """
        myEvent = self.model.getEvent(event)
        eventAss = myEvent.getEventAssignment(assignmentIndex)                
        m = eventAss.getMath()
        return libsbml.formulaToL3String(m)

    def getFunctionId (self, index):
        """
        Retuns the Id of the indexth user function definition

        Example: mathStr = model.getFunctionId (0)     
        """
        return self.model.getFunctionDefinition (index).getId()

    def getFunctionBody (self, func):
        """
        """ 
        myFunc = self.model.getFunctionDefinition (func) 
        return libsbml.formulaToL3String(myFunc.getBody())

    def getNumArgumentsInUserFunction (self, func):
        """
        Returns the number of arguments in the given function. The func argument can either be the name
        of a user function or its index.

        Example: 

          nargs = model.getNumArgumentsInUserFunction ('Hill')

          nargs = model.getNumArgumentsInUserFunction (0)
        """
        myFunc = self.model.getFunctionDefinition (func) 
        return myFunc.getNumArguments()                

    def getListOfArgumentsInUserFunction (self, func):
        """
        Returns a list of arguments in the specified user function. The func argument can either be the name
        of a user function or its index in the list of user fucntions.

        Example: 

          alist = model.getListOfArgumentsInUserFunction ('Hill')

          alist = model.getListOfArgumentsInUserFunction (0)
        """
        myFunc = self.model.getFunctionDefinition (func) 
        alist = []
        for i in range (myFunc.getNumArguments()):
            alist.append (libsbml.formulaToL3String(myFunc.getArgument(i)))
        return alist

    # def getReaction(self, rxn_id):
    #     return self.model.getReaction(rxn_id)

    # def getCompartment(self, comp_id):
    #     return self.model.getCompartment(comp_id)

    # def getListOfEvents(self):
    #     return self.model.getListOfEvents()

    # def getEvent(self, event_id):
    #     return self.model.getEvent(event_id)

    # def getRule(self, var):
    #     return self.model.getRule(var)

    # def getInitialAssignment(self, var):
    #     return self.model.getInitialAssignment(var)

    # def getListOfInitialAssignments(self):
    #     return self.model.getListOfInitialAssignments()

    def toSBML(self):
        """Returns the model in SBML format as a string.  Also checks model consistency
       and prints all errors and warnings.

       Example: print (model.toSBML())
       """

        errors = self.document.checkConsistency()
        if (errors > 0):
            for i in range(errors):
                print(self.document.getError(i).getSeverityAsString(), ": ", self.document.getError(i).getMessage())

        return libsbml.writeSBMLToString(self.document)

    def __repr__(self):
        return self.toSBML()

def writeCode(doc):
    """Returns a string containing calls to SimpleSBML functions that reproduce
    the model contained in the SBMLDocument *doc* in an sbmlModel object."""

    comp_template = 'model.addCompartment(vol=%s, comp_id=\'%s\');'
    species_template = 'model.addSpecies(species_id=\'%s\', amt=%s, comp=\'%s\');'
    param_template = 'model.addParameter(param_id=\'%s\', val=%s, units=\'%s\');'
    rxn_template = 'model.addReaction(reactants=%s, products=%s, expression=\'%s\', local_params=%s, rxn_id=\'%s\');'
    event_template = 'model.addEvent(trigger=\'%s\', assignments=%s, persistent=%s, initial_value=%s, priority=%s, delay=%s, event_id=\'%s\');'
    event_defaults = [True, False, '0', 0]
    assignrule_template = 'model.addAssignmentRule(var=\'%s\', math=\'%s\');'
    raterule_template = 'model.addRateRule(var=\'%s\', math=\'%s\');'
    initassign_template = 'model.addInitialAssignment(symbol=\'%s\', math=\'%s\')'
    init_template = 'import simplesbml\nmodel = simplesbml.sbmlModel(time_units=\'%s\', extent_units=\'%s\', sub_units=\'%s\', level=%s, version=%s);'
    init_defaults = ['second', 'mole', 'mole', 3, 1]
    command_list = []

    if doc.getLevel() == 1:
        warnings.warn('Warning: SimpleSBML does not support SBML Level 1.')

    props = libsbml.ConversionProperties()
    props.addOption('flatten comp', True)
    result = doc.convert(props)
    if(result != libsbml.LIBSBML_OPERATION_SUCCESS):
        raise SystemExit('Conversion failed: (' + str(result) + ')')

    mod = doc.getModel()
    comps = mod.getListOfCompartments()
    species = mod.getListOfSpecies()
    params = mod.getListOfParameters()
    rxns = mod.getListOfReactions()
    events = mod.getListOfEvents()
    rules = mod.getListOfRules()
    inits = []
    if doc.getLevel() == 3 or (doc.getLevel() == 2 and doc.getVersion() > 1):
        inits = mod.getListOfInitialAssignments()

    timeUnits = 'second'
    substanceUnits = 'mole'
    extentUnits = 'mole'
    if doc.getLevel() == 3:
        timeUnits = mod.getTimeUnits()
        extentUnits = mod.getExtentUnits()
        substanceUnits = mod.getSubstanceUnits()
    level = mod.getLevel()
    version = mod.getVersion()
    init_list = [timeUnits, extentUnits, substanceUnits, level, version]
    for i in range(0,5):
        if init_list[i] == init_defaults[i]:
            init_list[i] = 'del'

    command_list.append(init_template % \
            (init_list[0], init_list[1], init_list[2], init_list[3], init_list[4]))

    for comp in comps:
        if comp.getId() != 'c1':
            if comp.getId()[0] == 'c' and comp.getId()[1:len(comp.getId())].isdigit():
                if comp.getSize() == 1e-15:
                    command_list.append(comp_template % ('del', 'del'))
                else:
                    command_list.append(comp_template % (comp.getSize(), 'del'))
            else:
                if comp.getSize() == 1e-15:
                    command_list.append(comp_template % ('del', comp.getId()))
                else:
                    command_list.append(comp_template % (comp.getSize(), comp.getId()))

    for s in species:
        conc = s.getInitialConcentration()
        amt = s.getInitialAmount()
        sid = s.getId()
        if s.getCompartment() == 'c1':
            comp = 'del'
        else:
            comp = s.getCompartment()
        bc = s.getBoundaryCondition()
        if bc:
            sid = "$" + sid
        if isnan(conc) or amt > conc:
            command_list.append(species_template % (sid, str(amt), comp))
        else:
            command_list.append(species_template % ("[" + sid + "]", str(conc), comp))

    for p in params:
        val = p.getValue()
        pid = p.getId()
        if p.getUnits() == 'per_second':
            units = 'del'
        else:
            units = p.getUnits()
        isDelay = pid.find('Delay')
        if isDelay == -1:
            command_list.append(param_template % (pid, str(val), str(units)))

    for v in rxns:
        vid = v.getId()
        if vid[0] == 'v' and vid[1:len(vid)].isdigit():
            vid = 'del'
        reactants = []
        for r in v.getListOfReactants():
            reactants.append((str(r.getStoichiometry()) + ' ' + r.getSpecies()).replace('1.0 ', ''))
        products = []
        for p in v.getListOfProducts():
            products.append((str(p.getStoichiometry()) + ' ' + p.getSpecies()).replace('1.0 ', ''))
        expr = libsbml.formulaToString(v.getKineticLaw().getMath())
        local_params = {}
        local_ids = []
        local_values = []
        for k in v.getKineticLaw().getListOfParameters():
            local_ids.append(k.getId())
            local_values.append(k.getValue())
        local_params = dict(zip(local_ids, local_values))
        if len(local_params) == 0:
            local_params = 'del'
        command_list.append(rxn_template % (str(reactants), str(products), \
                    expr, str(local_params), vid))

    for e in events:
        persistent = True
        initialValue = False
        priority = '0'
        eid = e.getId()
        if len(eid) == 0 or (eid[0] == 'e' and eid[1:len(eid)].isdigit()):
            eid = 'del'
        if doc.getLevel() == 3:
            persistent = e.getTrigger().getPersistent()
            initialValue = e.getTrigger().getInitialValue()
            priority = e.getPriority()
            if type(priority) == libsbml.Priority:
                priority = libsbml.formulaToL3String(priority.getMath())
            else:
                priority = '0'
        tri = libsbml.formulaToL3String(e.getTrigger().getMath())
        did = e.getDelay()
        if type(did) == libsbml.Delay:
            delay = libsbml.formulaToL3String(did.getMath())
        else:
            delay = '0'
        assigns = e.getListOfEventAssignments()
        var = []
        values = []
        for assign in assigns:
            var.append(assign.getVariable())
            values.append(libsbml.formulaToL3String(assign.getMath()))
        assigns = dict(zip(var, values))

        event_list = [persistent, initialValue, priority, delay]
        for i in range(0,4):
            if event_list[i] == event_defaults[i]:
                event_list[i] = 'del'

        command_list.append(event_template % (tri, str(assigns), \
                event_list[0], event_list[1], event_list[2], event_list[3], eid))

    for r in rules:
        sym = r.getVariable()
        math = libsbml.formulaToL3String(r.getMath())
        if r.getTypeCode() == libsbml.SBML_ASSIGNMENT_RULE:
            command_list.append(assignrule_template % (sym, math))
        elif r.getTypeCode() == libsbml.SBML_RATE_RULE:
            command_list.append(raterule_template % (sym, math))
        else:
            next

    for i in inits:
        sym = i.getSymbol()
        math = libsbml.formulaToL3String(i.getMath())
        command_list.append(initassign_template % (sym, math))

    commands = '\n'.join(command_list)
    commands = sub('\w+=\'?del\'?(?=[,)])', '', commands)
    commands = sub('\((, )+', '(', commands)
    commands = sub('(, )+\)', ')', commands)
    commands = sub('(, )+', ', ', commands)
    return commands

def writeCodeFromFile(filename):
    """Reads the file saved under *filename* as an SBML format model and
    returns a string containing calls to SimpleSBML functions that reproduce
    the model in an sbmlModel object."""

    reader = libsbml.SBMLReader()
    doc = reader.readSBMLFromFile(filename)
    if doc.getNumErrors() > 0:
        raise SystemExit(doc.getError(0))
    return writeCode(doc)

def writeCodeFromString(sbmlstring):
    """Reads *sbmlstring* as an SBML format model and
    returns a string containing calls to SimpleSBML functions that reproduce
    the model in an sbmlModel object."""

    reader = libsbml.SBMLReader()
    doc = reader.readSBMLFromString(sbmlstring)
    return writeCode(doc)
