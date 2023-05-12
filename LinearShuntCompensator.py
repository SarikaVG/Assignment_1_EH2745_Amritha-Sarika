# -*- coding: utf-8 -*-
class LinearShuntCompensator:
    def __init__(self,name):
        self.name = name
        self.id = 'id'
        self.nomU= 0
        self.Terminal_List = []
        self.Node_Type='CE'
        self.CE_type='Compensator'
        self.Num_attachTerms=0
        self.b=0
        self.q=0
  