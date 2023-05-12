EH2745: Computer Applications in Power Systems- Assignment 1. By Amritha Jayan and Sarika Vaiyapuri Gunassekaran

Objective: This code is part of Assignment 1, which aims to create an embryo of an Energy Management System (EMS). It combines Python programming, CIM-XML modeling and parsing, and model building using Pandapower.

Overview: The code reads and parses two XML files: MicroGridTestConfiguration_T1_BE_EQ_V2.xml and MicroGridTestConfiguration_T1_BE_SSH_V2.xml. It extracts relevant data from these files and uses the data to create an EMS prototype.

Prerequisites: The code requires the following dependencies:
Python 3. x (Spyder Version 5)
Pandapower

Usage:
The XML files (MicroGridTestConfiguration_T1_BE_EQ_V2.xml and MicroGridTestConfiguration_T1_BE_SSH_V2.xml) are present in the same directory as this code file and run the code.

Functionality:
1. Parsing XML Files: The code parses the XML files using the xml.etree.ElementTree module.
Tree_EQ and tree_SSH variables hold the parsed trees.
The root_EQ and root_SSH variables contain the parsed trees' roots.
2. Data Extraction: 
The code builds instances of classes corresponding to various types of equipment after extracting data from the EQ XML file.
The retrieved information is kept in several lists that correspond to various types of equipment.
Additionally, data is extracted from the SSH XML file and put into different lists by the code.
3. Class Definitions:
The code imports classes from their respective modules.
4. Data Storage: 
To store the data collected from the EQ and SSH XML files, the code initializes empty lists.
For the purpose of storing the unique characteristics of each piece of equipment, separate lists are made.
5. Graph Traversal has been done.
6. The network is plotted with the help of Pandapower.

Reference: We have referred to some codes from the GitHub Repository.



