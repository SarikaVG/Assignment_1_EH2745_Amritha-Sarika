# -*- coding: utf-8 -*-
"""
#Assignment 1 combines Python programming, CIM-XML modelling and parsing and
finally model building using Pandapower and using these create an embryo of Energy Management
System.

@author: Amritha Jayan and Sarika Vaiyapuri Gunassekaran

"""
import xml.etree.ElementTree as ET

from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import filedialog

# GUI of the application
root = Tk()
root.title("EH2745 - Assignment 1")
content = ttk.Frame(root)
frame = ttk.Frame(content, borderwidth=5, relief="solid", width=600, height=300)
img = PhotoImage(file='KTH.png')
panel = ttk.Label(content, image=img)
content.grid(column=1, row=0)
frame.grid(column=1, row=0, columnspan=3, rowspan=2)
panel.grid(column=1, row=0, columnspan=3, rowspan=2)

# Insert File
def EQ_file():
    EQ_file = filedialog.askopenfilename()
    global EQ_file_XML, Message_EQ
    EQ_file_XML = EQ_file
    Message_EQ = "Added EQ File"

def SSH_file():
    SSH_file = filedialog.askopenfilename()
    global SSH_file_XML, Message_SSQ
    SSH_file_XML = SSH_file
    Message_SSH = "Added SSH File"

# GUI Layout
Button_EQ = Button(root, text="Select EQ File", command=EQ_file)
Button_EQ.grid(column=1, row=3, sticky='nesw')
Button_SSH = Button(root, text="Select SSH File", command=SSH_file)
Button_SSH.grid(column=1, row=4, sticky='nesw')
Button_Run = Button(root, text="Run", command=root.destroy)
Button_Run.grid(column=1, row=5,sticky='nesw')

root.mainloop()

# Parse the XML files
tree_EQ = ET.parse(EQ_file_XML)
tree_SSH = ET.parse(SSH_file_XML)

# Get the root of the parsed trees
root_EQ = tree_EQ.getroot()
root_SSH = tree_SSH.getroot()

# Define the namespaces used in the XML files
ns = {'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
              'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
              'md': 'http://iec.ch/TC57/61970-552/ModelDescription/1#',
              'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

# Import the required classes from their respective modules
from GeneratingUnit import GeneratingUnit
from ACLineSegment import ACLineSegment
from BusbarSection import BusbarSection
from Breaker import Breaker
from PowerTransformer import PowerTransformer
from RatioTapChanger import RatioTapChanger
from EnergyConsumer import EnergyConsumer
from LinearShuntCompensator import LinearShuntCompensator
from SynchronousMachine import SynchronousMachine
from BaseVoltage import BaseVoltage
from VoltageLevel import VoltageLevel
from RegulatingControl import RegulatingControl
from ConductingEquipment import ConductingEquipment
from ConnectivityNode import ConnectivityNode
from Terminal import Terminal

# Initialize empty lists to store the extracted information from the EQ XML files
ACLine_Segment_length = []
ACLine_Segment_list = []
ACLine_Segment_name = []
BaseVoltage_list = []
Breaker_list = []
BusbarSection_list = []
ConductingEquipment_list = []
ConnectivityNode_list = []
ConnectivityNode_list_id = []
EnergyConsumer_list = []
GeneratingUnit_list = []
LinearShuntCompensator_list = []
Object_name_list = []
PowerTransformer_list = []
RatioTapChanger_list = []
RegulatingControl_list = []
SynchronousMachine_list = []
Terminal_list = []
Terminal_list_ConductingEquipment = []
Terminal_list_ConnectivityNode = []
VoltageLevel_list = []
node_list = []

# Initialize empty lists to store the extracted information from the SSH XML files
Breaker_list_ssh = []
EnergyConsumer_list_ssh = []
Object_name_list_2 = []
RatioTapChanger_list_ssh = []
Terminal_list_ssh = []

# Loop through the root_EQ list of equipment to mapping the attributes to the corresponding attributes
# of the class and extract relevant data from the EQ XML file.
for equipment in root_EQ:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}", "")
        Object_name_list.append(name)
        # Check the type of equipment and create an instance of the corresponding class
        if name == 'BusbarSection':
            Busbar_Section = BusbarSection(equipment)
            Busbar_Section.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Busbar_Section.id = equipment.attrib.get(ns['rdf']+'ID')
            Busbar_Section.Node_Type = 'CE'
            Busbar_Section.EquipmentContainer = equipment.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            BusbarSection_list.append(Busbar_Section)
            ConductingEquipment_list.append(Busbar_Section)
            Busbar_Section.CE_type = 'BusbarSection'

        elif name == 'ACLineSegment':
            ACLine_Segment = ACLineSegment(equipment)
            ACLine_Segment.name = equipment.find('cim:IdentifiedObject.name', ns).text
            ACLine_Segment.Node_Type = 'CE'
            ACLine_Segment.id = equipment.attrib.get(ns['rdf']+'ID')
            ACLine_Segment.name = equipment.find('cim:IdentifiedObject.name', ns).text
            ACLine_Segment.r = equipment.find('cim:ACLineSegment.r', ns).text
            ACLine_Segment.x = equipment.find('cim:ACLineSegment.x', ns).text
            ACLine_Segment.bch = equipment.find('cim:ACLineSegment.bch', ns).text
            ACLine_Segment.length = equipment.find('cim:Conductor.length', ns).text
            ACLine_Segment_list.append(ACLine_Segment)
            ACLine_Segment_name.append(ACLine_Segment.name)
            ACLine_Segment_length.append(ACLine_Segment.length)
            ConductingEquipment_list.append(ACLine_Segment)

        elif name == 'Breaker':
            Brea_ker = Breaker(equipment)
            Brea_ker.id = equipment.attrib.get(ns['rdf']+'ID')
            Brea_ker.Node_Type = 'CE'
            Brea_ker.container_id = equipment.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Breaker_list.append(Brea_ker)
            ConductingEquipment_list.append(Brea_ker)

        elif name == 'EnergyConsumer':
            Energy_Consumer = EnergyConsumer(equipment)
            Energy_Consumer.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Energy_Consumer.id = equipment.attrib.get(ns['rdf']+'ID')
            Energy_Consumer.aggregate = equipment.find('cim:Equipment.aggregate', ns).text
            Energy_Consumer.container_id = equipment.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Energy_Consumer.Node_Type = 'CE '
            EnergyConsumer_list.append(Energy_Consumer)
            ConductingEquipment_list.append(Energy_Consumer)

        elif name == 'GeneratingUnit':
            Generating_Unit = GeneratingUnit(equipment)
            Generating_Unit.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Generating_Unit.id = equipment.attrib.get(ns['rdf']+'ID')
            Generating_Unit.initialP = equipment.find('cim:GeneratingUnit.initialP', ns).text
            Generating_Unit.nominalP = equipment.find('cim:GeneratingUnit.nominalP', ns).text
            Generating_Unit.maxOperatingP = equipment.find('cim:GeneratingUnit.maxOperatingP', ns).text
            Generating_Unit.minOperatingP = equipment.find('cim:GeneratingUnit.minOperatingP', ns).text
            Generating_Unit.container_id = equipment.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Generating_Unit.Node_Type = 'CE '
            GeneratingUnit_list.append(Generating_Unit)

        elif name == 'LinearShuntCompensator':
            LinearShunt_Compensator = LinearShuntCompensator(equipment)
            LinearShunt_Compensator.name = equipment.find('cim:IdentifiedObject.name', ns).text
            LinearShunt_Compensator.id = equipment.attrib.get(ns['rdf']+'ID')
            LinearShunt_Compensator.container_id = equipment.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            LinearShunt_Compensator.RegulatingControl = equipment.find('cim:RegulatingCondEq.RegulatingControl', ns).attrib.get(ns['rdf']+'resource')
            LinearShunt_Compensator.nomU = float(equipment.find('cim:ShuntCompensator.nomU', ns).text)
            LinearShunt_Compensator.b = float(equipment.find('cim:LinearShuntCompensator.bPerSection', ns).text)
            LinearShunt_Compensator.q = float(LinearShunt_Compensator.b*LinearShunt_Compensator.nomU*LinearShunt_Compensator.nomU)
            LinearShunt_Compensator.Node_Type = 'CE '
            LinearShuntCompensator_list.append(LinearShunt_Compensator)
            ConductingEquipment_list.append(LinearShunt_Compensator)

        elif name == 'VoltageLevel':
            Voltage_Level = VoltageLevel(equipment)
            Voltage_Level.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Voltage_Level.id = equipment.attrib.get(ns['rdf']+'ID')
            Voltage_Level.lowVoltageLimit = equipment.find('cim:VoltageLevel.lowVoltageLimit', ns).text
            Voltage_Level.highVoltageLimit = equipment.find('cim:VoltageLevel.highVoltageLimit', ns).text
            Voltage_Level.Substation = equipment.find('cim:VoltageLevel.Substation', ns).attrib.get(ns['rdf']+'resource')
            Voltage_Level.BaseVoltage = equipment.find('cim:VoltageLevel.BaseVoltage', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            VoltageLevel_list.append(Voltage_Level)

        elif name == 'PowerTransformer':
            Power_Transformer = PowerTransformer(equipment)
            Power_Transformer.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Power_Transformer.id = equipment.attrib.get(ns['rdf']+'ID')
            Power_Transformer.Node_Type = 'CE'
            Power_Transformer.EquipmentContainer = equipment.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            PowerTransformer_list.append(Power_Transformer)
            ConductingEquipment_list.append(Power_Transformer)

        elif name == 'RatioTapChanger':
            Ratio_TapChanger = RatioTapChanger(equipment)
            Ratio_TapChanger.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Ratio_TapChanger.id = equipment.attrib.get(ns['rdf']+'ID')
            Ratio_TapChanger.Node_Type = 'CE'
            Ratio_TapChanger.TapChangerControl = equipment.find('cim:TapChanger.TapChangerControl', ns).attrib.get(ns['rdf']+'resource')
            Ratio_TapChanger.neutralU = equipment.find('cim:TapChanger.neutralU', ns).text
            Ratio_TapChanger.lowStep = equipment.find('cim:TapChanger.lowStep', ns).text
            Ratio_TapChanger.highStep = equipment.find('cim:TapChanger.highStep', ns).text
            Ratio_TapChanger.neutralStep = equipment.find('cim:TapChanger.neutralStep', ns).text
            Ratio_TapChanger.normalStep = equipment.find('cim:TapChanger.normalStep', ns).text
            Ratio_TapChanger.stepVoltageIncrement = equipment.find('cim:RatioTapChanger.stepVoltageIncrement', ns).text
            RatioTapChanger_list.append(Ratio_TapChanger)

        elif name == 'SynchronousMachine':
            Synchronous_Machine = SynchronousMachine(equipment)
            Synchronous_Machine.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Synchronous_Machine.id = equipment.attrib.get(ns['rdf']+'ID')
            SynchronousMachine_list.append(Synchronous_Machine)
            Synchronous_Machine.EquipmentContainer = equipment.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Synchronous_Machine.GeneratingUnit = equipment.find('cim:RotatingMachine.GeneratingUnit', ns).attrib.get(ns['rdf']+'resource')
            Synchronous_Machine.ratedU = equipment.find('cim:RotatingMachine.ratedU', ns).text
            Synchronous_Machine.Node_Type = 'CE'
            ConductingEquipment_list.append(Synchronous_Machine)

        elif name == 'BaseVoltage':
            Base_Voltage = BaseVoltage(equipment)
            Base_Voltage.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Base_Voltage.id = equipment.attrib.get(ns['rdf']+'ID')
            Base_Voltage.Node_Type = 'CE'
            BaseVoltage_list.append(Base_Voltage)
            Base_Voltage.nominalVoltage = equipment.find('cim:BaseVoltage.nominalVoltage', ns).text

        elif name == 'ConnectivityNode':
            Connectivity_Node = ConnectivityNode(equipment)
            Connectivity_Node.name = equipment.find('cim:IdentifiedObject.name', ns).text
            Connectivity_Node.id = equipment.attrib.get(ns['rdf']+'ID')
            Connectivity_Node.container_id = equipment.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Connectivity_Node.Node_Type = 'CN'
            ConnectivityNode_list.append(Connectivity_Node)
            ConnectivityNode_list_id.append(Connectivity_Node.id)

        elif name == 'Terminal':
            T_erminal = Terminal(equipment)
            T_erminal.name = equipment.find('cim:IdentifiedObject.name', ns).text
            T_erminal.id = equipment.attrib.get(ns['rdf']+'ID')
            T_erminal.ConductingEquipment = equipment.find('cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            T_erminal.ConnectivityNode = equipment.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            T_erminal.Node_Type = 'TE'
            T_erminal.traversal_flag = 0
            Terminal_list.append(T_erminal)
            Terminal_list_ConductingEquipment.append(
                T_erminal.ConductingEquipment.replace('#', ''))
            Terminal_list_ConnectivityNode.append(
                T_erminal.ConnectivityNode.replace('#', ''))

# Loop through the root_EQ list of equipment to mapping the attributes to the corresponding attributes
# of your class and extract relevant data from the SSH XML file.
for equipment in root_SSH:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}", "")
        Object_name_list_2.append(name)
        if name == 'Terminal':
            T_erminal = Terminal(equipment)
            T_erminal.id = equipment.attrib.get(ns['rdf']+'ID')
            Terminal_list_ssh.append(T_erminal)

        elif name == 'EnergyConsumer':
            Energy_Consumer = EnergyConsumer(equipment)
            Energy_Consumer.id = equipment.attrib.get(ns['rdf']+'ID')
            Energy_Consumer.p = equipment.find('cim:EnergyConsumer.p', ns).text
            Energy_Consumer.q = equipment.find('cim:EnergyConsumer.q', ns).text
            EnergyConsumer_list_ssh.append(Energy_Consumer.p)

        elif name == 'RatioTapChanger':
            Ratio_TapChanger = RatioTapChanger(equipment)
            Ratio_TapChanger.id = equipment.attrib.get(ns['rdf']+'ID')
            Ratio_TapChanger.step = equipment.find('cim:TapChanger.step', ns).text
            Ratio_TapChanger.controlEnabled = equipment.find('cim:TapChanger.controlEnabled', ns).text
            RatioTapChanger_list_ssh.append(Ratio_TapChanger)

        elif name == 'Breaker':
            B_reaker = Breaker(equipment)
            B_reaker.id = equipment.attrib.get(ns['rdf']+'ID')
            B_reaker.Switch = equipment.find('cim:Switch.open', ns).text
            Breaker_list_ssh.append(Breaker)

# Mapping Base Voltage and Nominal voltage of Busbar.
for equipment in root_EQ:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}", "")
        if name == 'BusbarSection':
            for Busbar_Section in BusbarSection_list:
                for Voltage_Level in VoltageLevel_list:
                    if Busbar_Section.EquipmentContainer == Voltage_Level.id:
                        for Base_Voltage in BaseVoltage_list:
                            if Voltage_Level.BaseVoltage == Base_Voltage.id:
                                Busbar_Section.voltage = float(
                                    Base_Voltage.nominalVoltage)

# Mapping Base Voltage and Nominal voltage of Connectivity Node.
for equipment in root_EQ:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}", "")
        if name == 'ConnectivityNode':
            for CN in ConnectivityNode_list:
                for Voltage_Level in VoltageLevel_list:
                    if CN.container_id == Voltage_Level.id:
                        for Base_Voltage in BaseVoltage_list:
                            if Voltage_Level.BaseVoltage == Base_Voltage.id:
                                CN.voltage = float(
                                    Base_Voltage.nominalVoltage)


# Network Travsersing

# Finding the terminal connected to respective CN

Terminal_attached_to_CN_list = []
def find_Terminal_attached_to_CN(CN):
    for TE in Terminal_list:
        if CN.id == TE.ConnectivityNode:
            return(TE)

def find_Terminal_attached_to_CN_list(CN):
    Terminal_attached_to_CN_list1 = []
    for TE in Terminal_list:
        if TE.ConnectivityNode == CN.id:
            Terminal_attached_to_CN_list1.append(TE)
    return(Terminal_attached_to_CN_list1)

for CN in ConnectivityNode_list:
    Terminal_attached_to_CN_list.append(find_Terminal_attached_to_CN(CN))

# Finding the terminal connected to respective CE
def find_Terminal_attached_to_CE(CE):
    for TE in Terminal_list:
        if CE.id == TE.ConductingEquipment:
            return(TE)

def find_Terminal_attached_to_ConductingEquipment_list(CE):
    Terminal_attached_to_ConductingEquipment_list1 = []
    for TE in Terminal_list:
        if CE.id == TE.ConductingEquipment:
            Terminal_attached_to_ConductingEquipment_list1.append(TE)
    return(Terminal_attached_to_ConductingEquipment_list1)

Terminal_attached_to_ConductingEquipment_list = []
for Node in ConductingEquipment_list:
    Terminal_attached_to_ConductingEquipment_list.append(find_Terminal_attached_to_CE(Node))

# Find and return the next node based on the previous node and current node types
def find_next_node(previous_node, current_node):
    # If the current node is a ConnectivityNode ('CN'), return a randomly sampled terminal from Terminal_attached_to_CN_list
    if current_node.Node_Type == 'CN':
        return(random.sample(Terminal_attached_to_CN_list, 1))
    # If the current node is a ConductingEquipment ('CE'), return a randomly sampled terminal from Terminal_attached_to_ConductingEquipment_list
    elif current_node.Node_Type == 'CE':
        return(random.sample(Terminal_attached_to_ConductingEquipment_list, 1))
    # If the current node is a Terminal ('TE') and the previous node is a ConnectivityNode ('CN'), find the corresponding ConductingEquipment and return it
    elif current_node.Node_Type == 'TE' and previous_node.Node_Type == 'CN':
        for Node in ConductingEquipment_list:  
            if current_node.ConductingEquipment == Node.id:
                return(Node)
    # If the current node is a Terminal ('TE') and the previous node is a ConductingEquipment ('CE'), find the corresponding ConnectivityNode and return it
    elif current_node.Node_Type == 'TE' and previous_node.Node_Type == 'CE':
        for Node in ConnectivityNode_list:
            if current_node.ConnectivityNode == Node.id:
                return(Node)


# number of terminals attached to connectivity node

number_list = []

def Num_attached_terminal_of_CN(CN):
    for TE in Terminal_attached_to_CN_list:
        if TE.ConnectivityNode == CN.id:
            number_list.append(TE)
            return(len(number_list))

# number of terminals attached to ConductingEquipment

def Num_attached_terminal_of_CE(CE):
    for TE in Terminal_attached_to_ConductingEquipment_list:
        try:
            if TE.ConductingEquipment == CE.id:
                number_list.append(TE)
                return(len(number_list))
        except:
            pass

# find CN attach to bus
CN_attached_to_busbar_list = []
CN_name = []
for CN in ConnectivityNode_list:
    for TE in find_Terminal_attached_to_CN_list(CN):
        next_node = find_next_node(CN, TE)
        try:
            if next_node.CE_type == 'BusbarSection':
                CN_attached_to_busbar_list.append(CN)
                CN_name.append(CN.name)
        except:
            pass
#print(CN_attached_to_busbar_list)
print(CN_name)

CN_not_attached_to_busbar = []
CN_not_name = []

for CN in ConnectivityNode_list:
    if CN not in CN_attached_to_busbar_list:
        CN_not_name.append(CN.name)
        CN_not_attached_to_busbar.append(CN)


#print(CN_not_attached_to_busbar)
print(CN_not_name)

# Initialize an empty stack
All_stack = []

# Traverse through the ConnectivityNode_list and its attached terminals to create stacks of connected elements
# Each stack represents a connected path in the network
# Store all the created stacks in the All_stack list

for CN in ConnectivityNode_list:
    if Num_attached_terminal_of_CN(CN) > 0:
        for TE in find_Terminal_attached_to_CN_list(CN):
            if TE.traversal_flag == 0:
                current_node = CN
                CN.Num_attachTerms -= 1 
                TE.traversal_flag = 1
                previous_node = current_node
                current_node = TE
                next_node = find_next_node(previous_node, current_node)  
                CN_CE_stack = [CN]
                CN_CE_stack.append(next_node)
                CE = next_node 
                try:
                    if Num_attached_terminal_of_CE(CE) > 1:
                        for TE in find_Terminal_attached_to_ConductingEquipment_list(CE):
                            if TE.traversal_flag == 0: 
                                TE.traversal_flag = 1
                                next_node = find_next_node(CE, TE)
                                CN_CE_stack.append(next_node)
                except:
                    pass
                
                if CN_CE_stack not in All_stack: 
                    All_stack.append(CN_CE_stack)
print(All_stack)

#Create network in Pandapower.

import pandapower.networks
from pandapower.plotting import simple_plot
from pandapower.plotting.plotly import vlevel_plotly, simple_plotly
from pandapower.networks import mv_oberrhein
import pandapower as pp

# create component for panda power
net = pp.create_empty_network()

# create busbar 'b' and node 'n'

for Busbar_Section in BusbarSection_list:
    pp.create_bus(net, name=Busbar_Section.name, vn_kv=Busbar_Section.voltage, type="b")

for CN in CN_not_attached_to_busbar:
    pp.create_bus(net, name=CN.name, vn_kv=CN.voltage, type="n")
    
print(net.bus)

# Define function to find the busbar for connectivit node attached to terminal

def find_busbar_for_connectivity_node(CN):
    lista = find_Terminal_attached_to_CN_list(CN)
    for TE in lista:
        bus = find_next_node(CN, TE)
        try:
            if bus.CE_type == 'BusbarSection':
                return(pp.get_element_index(net, "bus", bus.name))
            if bus.CE_type == 'Breaker':
                return(pp.get_element_index(net, "bus", CN.name))
        except:
            pass

# The ACLineSegment, breaker and transformer are Conducting equipments that come between two CNs,
# hence, we consider item[0] and item [1].

# create line
for item in All_stack:
    for lines in item:
        try:
            if lines.CE_type == 'ACLineSegment':
                pp.create_line(net, find_busbar_for_connectivity_node(item[0]), find_busbar_for_connectivity_node(
                    item[-1]), length_km=2, std_type="N2XS(FL)2Y 1x300 RM/35 64/110 kV",  name=lines.name)
        except:
            pass
print(net.line)



# create breaker
for item in All_stack:
    for breaker in item:
        try:
            if breaker.CE_type == 'Breaker':
                if breaker.state == 'false':
                    pp.create_switch(net, find_busbar_for_connectivity_node(item[0]), find_busbar_for_connectivity_node(item[-1]), et="b", type="CB", closed=True)
                if breaker.state == 'ture':
                    pp.create_switch(net, find_busbar_for_connectivity_node(item[0]), find_busbar_for_connectivity_node(item[-1]), et="b", type="CB", closed=False)
        except:
            pass
net.switch
print(net.switch)

# create transformer

# For transformers the high and low voltage busbars need to be determined

for item in All_stack:
    for transformer in item:
        try:
            if transformer.CE_type == 'Transformer':
                if item[0].voltage > item[2].voltage:
                    busbar_hv = find_busbar_for_connectivity_node(item[0])
                    busbar_lv = find_busbar_for_connectivity_node(item[2])
                else:
                    busbar_hv = find_busbar_for_connectivity_node(item[2])
                    busbar_lv = find_busbar_for_connectivity_node(item[0])
                pp.create_transformer(
                    net, busbar_hv, busbar_lv, name=transformer.name, std_type="25 MVA 110/20 kV")
        except:
            pass
        
print(net.trafo)

# The Load, Syncronous generator and shunt compensator are end devices and hence we use only item[0]

# create load
for item in All_stack:
    for load in item:
        try:
            if load.CE_type == 'load':
                pp.create_load(net, find_busbar_for_connectivity_node(item[0]), load.p, load.q, scaling=0.6, name=load.name)
        except:
            pass
print(net.load)

# create generators
check = []
for item in All_stack:
    for generator in item:
        try:
            if generator.CE_type == 'SynchronousMachine':
                check.append(generator)
                pp.create_sgen(net, find_busbar_for_connectivity_node(item[0]), p_mw=0.9, q_mvar=0.9, name=generator.name)
        except:
            pass
print(net.sgen)

# create Compensator
for item in All_stack:
    for Compensator in item:
        try:
            if Compensator.CE_type == 'Compensator':
                pp.create_shunt(net, find_busbar_for_connectivity_node(item[0]), q_mvar=0.01*Compensator.q, p_mw=0, name=Compensator.name)
        except:
            pass        

print(net.shunt)

print(net)

# plot the network
pp.plotting.simple_plot(net)