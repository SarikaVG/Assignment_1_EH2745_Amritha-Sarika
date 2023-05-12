# -*- coding: utf-8 -*-
class GeneratingUnit:
    def __init__(self, name):
        self.name = name
        self.id = 'id'
        self.initialP = 'initialP'
        self.nominalP = 'nominalP'
        self.maxOperatingP = 'maxOperatingP'
        self.minOperatingP = 'minOperatingP'        
        self.Terminal_List = []
        self.Node_Type = 'CE'
        self.CE_type='Generator'
        self.Num_attachTerms=0
       
