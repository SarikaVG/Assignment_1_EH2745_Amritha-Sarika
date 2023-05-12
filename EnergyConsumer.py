# -*- coding: utf-8 -*-
class EnergyConsumer:
    def __init__(self, name):
        self.name = name
        self.Terminal_List = []
        self.num_attachTerms = 0 
        self.Node_Type = 'CE'
        self.id = 'id'
        self.aggregate = 'aggregate'
        self.CE_type='load'
        self.p=0
        self.q=0
