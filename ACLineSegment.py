# -*- coding: utf-8 -*-

class ACLineSegment:
    def __init__(self, name):
        self.name = name
        self.Terminal_List = []
        self.Num_attachTerms = 0 
        self.Node_Type = 'CE'
        self.id = 'id'
        self.r = 'r'
        self.x = 'x'
        self.bch = 'bch'
        self.length = 'length'
        self.CE_type='ACLineSegment'