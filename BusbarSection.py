# -*- coding: utf-8 -*-
class BusbarSection:
    def __init__(self,name):
        self.name = name
        self.id = 'id'
        self.Terminal_List = []
        self.Num_attachTerms = 0 
        self.Node_Type = 'CE '
        self.Busbar_Section_rdf_id = 'Busbar_Section_rdf_id'
        self.CE_type='BusbarSection'
        self.voltage=0
    
