# -*- coding: utf-8 -*-
class Breaker:
    def __init__(self, name):
        self.name = name
        self.Terminal_List = []
        self.Num_attachTerms = 0 
        self.Node_Type = 'CE'
        self.id = 'id'
        self.state = 'false'
        self.CE_type='Breaker'
