# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 23:13:42 2015

@author: carolc24
"""

import sys
from libsbml import *

class sbmlModel(object):
            
    def check(self, value, message):
        if value == None:
            raise SystemExit('LibSBML returned a null value trying to ' + \
                    message + '.')
        elif type(value) is int:
            if value == LIBSBML_OPERATION_SUCCESS:
                return
            else:
                err_msg = 'Error trying to ' + message + '.' \
                + 'LibSBML returned error code ' + str(value) + ': "'\
                + OperationReturnValue_toString(value).strip() + '"'
            raise SystemExit(err_msg)
        else:
            return
    
    def __init__(self, time_units='second', extent_units='mole', \
                 sub_units='mole'):
        try:
            self.document = SBMLDocument(3,1)
        except ValueError:
            raise SystemExit('Could not create SBMLDocument object')
        self.model = self.document.createModel()
        self.check(self.model, 'create model')
        self.check(self.model.setTimeUnits('second'), 'set model-wide time units')
        self.check(self.model.setExtentUnits('mole'), 'set model units of extent')
        self.check(self.model.setSubstanceUnits('mole'),'set model substance units')
        
        per_second = self.model.createUnitDefinition()
        self.check(per_second,                         'create unit definition')
        self.check(per_second.setId('per_second'),     'set unit definition id')
        unit = per_second.createUnit()
        self.check(unit,                               'create unit on per_second')
        self.check(unit.setKind(UNIT_KIND_SECOND),     'set unit kind')
        self.check(unit.setExponent(-1),               'set unit exponent')
        self.check(unit.setScale(0),                   'set unit scale')
        self.check(unit.setMultiplier(1),              'set unit multiplier')
        self.addCompartment();
            
    def addCompartment(self, comp_id=''):
        c1 = self.model.createCompartment()
        self.check(c1,                                 'create compartment')
        if len(comp_id) == 0:
            comp_id = 'c' + str(self.model.getNumCompartments());
        self.check(c1.setId(comp_id),                     'set compartment id')
        self.check(c1.setConstant(True),               'set compartment "constant"')
        self.check(c1.setSize(1),                      'set compartment "size"')
        self.check(c1.setSpatialDimensions(3),         'set compartment dimensions')
        self.check(c1.setUnits('litre'),               'set compartment size units')
        return c1
        
    def addSpecies(self, species_id, amt, comp='c1'):
        s1 = self.model.createSpecies()
        self.check(s1,                           'create species s1')
        self.check(s1.setCompartment(comp),      'set species s1 compartment')
        self.check(s1.setInitialAmount(amt),     'set initial amount for s1')
        self.check(s1.setSubstanceUnits('mole'), 'set substance units for s1')
        if species_id[0] == '$':
            self.check(s1.setBoundaryCondition(True), \
                    'set "boundaryCondition" on s1')
            self.check(s1.setConstant(False), 'set "constant" attribute on s1')
            self.check(s1.setId(species_id[1:len(species_id)]), 'set species s1 id')
        else:
            self.check(s1.setBoundaryCondition(False), \
                    'set "boundaryCondition" on s1')
            self.check(s1.setConstant(False), 'set "constant" attribute on s1')
            self.check(s1.setId(species_id),  'set species s1 id')
        self.check(s1.setHasOnlySubstanceUnits(False), \
                'set "hasOnlySubstanceUnits" on s1')
        return s1
        
    def addParameter(self, param_id, val, units='per_second'):
        k = self.model.createParameter()
        self.check(k,                        'create parameter k')
        self.check(k.setId(param_id),        'set parameter k id')
        self.check(k.setConstant(True),      'set parameter k "constant"')
        self.check(k.setValue(val),          'set parameter k value')
        self.check(k.setUnits(units), 'set parameter k units')
        return k
        
    def addReaction(self, reactants, products, expression, rxn_id=''):
        r1 = self.model.createReaction()
        self.check(r1,                         'create reaction')
        if len(rxn_id) == 0:
            rxn_id = 'v' + str(self.model.getNumReactions());
        self.check(r1.setId(rxn_id),           'set reaction id')
        self.check(r1.setReversible(False),    'set reaction reversibility flag')
        self.check(r1.setFast(False),          'set reaction "fast" attribute')
        
        for re in reactants:
            s1 = self.model.getSpecies(re);
            species_ref1 = r1.createReactant()
            self.check(species_ref1,                       'create reactant')
            self.check(species_ref1.setSpecies(str(s1)[9:len(str(s1))-1]), \
                    'assign reactant species')
            self.check(species_ref1.setConstant(True), \
                    'set "constant" on species ref 1')
            
        for pro in products:
            s2 = self.model.getSpecies(pro);
            species_ref2 = r1.createProduct()
            self.check(species_ref2, 'create product')
            self.check(species_ref2.setSpecies(str(s2)[9:len(str(s2))-1]), \
                    'assign product species')
            self.check(species_ref2.setConstant(True), \
                    'set "constant" on species ref 2')
         
        math_ast = parseL3Formula(expression);
        self.check(math_ast,    'create AST for rate expression')
     
        kinetic_law = r1.createKineticLaw()
        self.check(kinetic_law,                   'create kinetic law')
        self.check(kinetic_law.setMath(math_ast), 'set math on kinetic law')
        return r1
    
    def addEvent(self, trigger, delay, var, value, persistent=True, \
                 initial_value=False, priority=0, event_id=''):
        e1 = self.model.createEvent();
        self.check(e1,     'create event');
        if len(event_id) == 0:
            event_id = 'e' + str(self.model.getNumEvents());
        self.check(e1.setId(event_id),    'add id to event');
        
        tri = e1.createTrigger();
        self.check(tri,  'add trigger to event');
        self.check(tri.setPersistent(persistent),   'set persistence of trigger');
        self.check(tri.setInitialValue(initial_value), 'set initial value of trigger');
        tri_ast = parseL3Formula(trigger);
        self.check(tri.setMath(tri_ast),     'add formula to trigger');
        
        de = e1.createDelay();
        k = self.addParameter(event_id+'Delay', delay, self.model.getTimeUnits());
        self.check(de,               'add delay to event');
        delay_ast = parseL3Formula(k.getId());
        self.check(de.setMath(delay_ast),     'set formula for delay');
        
        for v in var:          
            assign = e1.createEventAssignment();
            self.check(assign,   'add event assignment to event');
            self.check(assign.setVariable(v),  'add variable to event assignment');
            val_ast = parseL3Formula(str(value[var.index(v)]));
            self.check(assign.setMath(val_ast),    'add value to event assignment');
        
        pri = e1.createPriority();
        pri_ast = parseL3Formula(str(priority));
        self.check(pri.setMath(pri_ast), 'add priority to event');
        return e1
        
    def getSpecies(self, species_id):
        return self.model.getSpecies(species_id);

    def getParameter(self, param_id):
        return self.model.getParameter(param_id);
    
    def getReaction(self, rxn_id):
        return self.model.getReaction(rxn_id);
        
    def getCompartment(self, comp_id):
        return self.model.getCompartment(comp_id);
                  
    def __repr__(self):
        return writeSBMLToString(self.document)
        
def writeCodeFromFile(filename):
    comp_template = 'model.addCompartment(\'%s\');';
    species_template = 'model.addSpecies(\'%s\', %s);';
    param_template = 'model.addParameter(\'%s\', %s);';
    rxn_template = 'model.addReaction(%s, %s, \'%s\', \'%s\');';
    event_template = 'model.addEvent(\'%s\', %s, %s, %s, %s, %s, %s, \'%s\');';
    init_template = 'import simplesbml\nmodel = simplesbml.sbmlModel(\'%s\', \'%s\', \'%s\');';
    command_list = [];
    
    reader = SBMLReader();
    doc = reader.readSBMLFromFile(filename);
    mod = doc.getModel();
    comps = mod.getListOfCompartments();
    species = mod.getListOfSpecies();
    params = mod.getListOfParameters();
    rxns = mod.getListOfReactions();
    events = mod.getListOfEvents();
    
    timeUnits = mod.getTimeUnits();
    extentUnits = mod.getExtentUnits();
    substanceUnits = mod.getSubstanceUnits();
    command_list.append(init_template % (timeUnits, extentUnits, substanceUnits));
    
    for comp in comps:
        if comp.getId() != 'c1':
            command_list.append(comp_template % (comp.getId()));
            
    for s in species:
        amt = s.getInitialAmount();
        sid = s.getId();
        bc = s.getBoundaryCondition();
        if bc:
            sid = "$" + sid;
        command_list.append(species_template % (sid, str(amt)));
        
    for p in params:
        val = p.getValue();
        pid = p.getId();
        isDelay = pid.find('Delay');
        if isDelay == -1:
            command_list.append(param_template % (pid, str(val)));
        
    for v in rxns:
        vid = v.getId();
        reactants = [];
        for r in v.getListOfReactants():
            reactants.append(r.getSpecies());
        products = [];
        for p in v.getListOfProducts():
            products.append(p.getSpecies());
        expr = formulaToString(v.getKineticLaw().getMath());
        command_list.append(rxn_template % (str(reactants), str(products), expr, vid));
        
    for e in events:
        persistent = e.getTrigger().getPersistent();
        initialValue = e.getTrigger().getInitialValue();
        eid = e.getId();
        priority = formulaToL3String(e.getPriority().getMath());
        tri = formulaToL3String(e.getTrigger().getMath());
        did = formulaToL3String(e.getDelay().getMath());
        delay = mod.getParameter(did).getValue();
        assigns = e.getListOfEventAssignments();
        var = [];
        values = [];
        for assign in assigns:
            var.append(assign.getVariable());
            values.append(formulaToL3String(assign.getMath()));
        command_list.append(event_template % (tri, str(delay), str(var), str(values), \
                str(persistent), str(initialValue), str(priority), eid));
    
    commands = '\n'.join(command_list);
    return commands;