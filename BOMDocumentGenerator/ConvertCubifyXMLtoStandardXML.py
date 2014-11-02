# -*- coding: utf-8; -*-
#
# This file is part of BOM Document Generator Tool.
#
# This tool is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MMC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
#The MIT License (MIT)

#Copyright (c) 2014 firepick

# (c) 2014 firepick-delta, http://delta.firepick.org/
# Author: David Shanklin, http://www.sagesmithing.org

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# These utilities are used to support GitHub Flavored Markdown (GFM for short)

import re
import os
import sys

# convert Cubify drawing to readiable XML file format
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

DEFAULT_TOP_LEVEL = {'ident':'','description':'','config':''}

DEFAULT_ITEM_LEVEL = {'ident':'','type':'','description':'','config':'','qty':''}

DEFAULT_SUBCOMPONENT_LEVEL = {'identifier':'XE-200','type':'Part','qty':'5'}

DEFAULT_SUBCOMPONENT_OF_LEVEL = {'identifier':'AADSS','type':'Assembly','qty':'5'}

TOP_LEVEL_PART_NUMBER = "AFPD0001"
TOP_LEVEL_PART_NUMBER_RE = "(TOP_LEVEL_PART_NUMBER)"
TOP_LEVEL_FORMAT_RE = "(.*) - (.*)_Config&lt;([0-9]*?)&gt;_([0-9]*)"
DEFAULT_ITEM = {'item': '', 'type' : '', 'description': '', 'config': '', 'number' : ''}

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def ItemExist(components, name):
    returnValue = False
    for ident in components.findall('./item/ident'):
        if (ident.text == name):
            returnValue = True
            break
    return returnValue

def CreateTopLevel(root, parsedtop):
    toplevel = SubElement(root, 'toplevel')
    for x in parsedtop:
        temp = SubElement(toplevel, x)
        temp.text = parsedtop[x]
    components = SubElement(toplevel,'components')
    return components

def CreateItem(components, parseditem):
    item = SubElement(components, 'item')
    for x in parseditem:
        temp = SubElement(item, x)
        temp.text = parseditem[x]
    return item

def CreateSubComponent(item, parsedsubcomponent):
    subcomponent = SubElement(item,'item')
    for x in parsedsubcomponent:
        temp = SubElement(subcomponent,x)
        temp.text = parsedsubcomponent[x]

def CreateSubComponentOf(item, parsedsubcomponentof):
    subcomponentof = SubElement(item,'item')
    for x in parsedsubcomponentof:
        temp = SubElement(subcomponentof,x)
        temp.text = parsedsubcomponent[x]

    #itemidentifier.text = "APFD0001"
    #description = SubElement(toplevel, 'description')
    #description.text = "Extrusion, nuts (pre-insertion)"
    #manufacturer = SubElement(toplevel, "manufacturer")
    #manufacturer.text = "firepick-delta"
    #url = SubElement(toplevel,"url")
    #url.text = "http://delta.firepick.org/"

# follows the form of XML generated by PDF from Cubify Design
def findTopLevel(tree):
    topNode = tree.find('Node')
    # TBD probably should check if topNode is file TPD (for file integrity check)
    topLevel = topNode .find('Node')
    return topLevel

def ParseTopLevel(tree):
    returnItem = DEFAULT_TOP_LEVEL
    nameInputTopLevel = tree.attrib[ 'Name' ]
    line = str(nameInputTopLevel)
    searchObj = re.search(  r'(.*) - (.*)_Config<([0-9]*?)>_([0-9]*)', line, re.M|re.I)
    if searchObj:
        returnItem['ident'] = searchObj.group(1)
        returnItem['description'] = searchObj.group(2)
        returnItem['config'] = searchObj.group(3)
    return returnItem

def ParseItem(tree):
    returnItem = DEFAULT_ITEM_LEVEL
    nameInputTopLevel = tree.attrib[ 'Name' ]
    line = str(nameInputTopLevel)
    searchObj = re.search(  r'(.[0-9|A-Z|a-z|a-]*) - (.*)<([0-9]*?)>_Config<([0-9]*?)>_([0-9]*)', line, re.M|re.I)
    if not searchObj:
        searchObj = re.search(  r'(.*)<([0-9]*?)>_Config<([0-9]*?)>_([0-9]*)', line, re.M|re.I)
        if searchObj :
            returnItem['ident'] = searchObj.group(1)
            returnItem['description'] = ' '
            returnItem['config'] = searchObj.group(3)
            if len(tree):
                returnItem['type'] = 'Assembly'
            else:
                returnItem['type'] = 'Part'
    else:
        returnItem['ident'] = searchObj.group(1)
        returnItem['description'] = searchObj.group(2)
        returnItem['config'] = searchObj.group(4)
        if len(tree):
            returnItem['type'] = 'Assembly'
        else:
            returnItem['type'] = 'Part'
    return returnItem

def Quantity(tree, name, component):
    returnValue = 0
    if (component == True):
       returnValue = 0

    for child in tree.iter('Node'):
        line = child.attrib
        line = line['Name']
        # print line
        searchObj = re.search(  r'(\w*) - (.*)_Config<([0-9]*?)>_([0-9]*)', line, re.M|re.I)
        if (searchObj):
            if searchObj.group(1) == name:
                returnValue = returnValue + 1
        else:
            searchObj = re.search(  r'(.*)<([0-9]*?)>_Config<([0-9]*?)>_([0-9]*)', line, re.M|re.I)
            if searchObj:
                if searchObj.group(1) == name:
                    returnValue = returnValue + 1
    return returnValue
    #    searchObj = re.search(  r'(.*) - (.*)_Config<([0-9]*?)>_([0-9]*)', line['Name'], re.M|re.I)
    #    if searchObj(1) == name:
    #        returnValue = returnValue + 1
    #print returnValue
    #returnValue = str(returnValue) 

def ParseCubifyXMLToStandardXML(filename):
    # high level XML name
    product = Element('product')
    if (os.path.isfile(filename)):
        # parse cubify drawing xml toplevel to standard xml
        root = ElementTree.parse(filename)
        inputTopLevel = findTopLevel(root)
        parsedtoplevel = ParseTopLevel(inputTopLevel)
        components = CreateTopLevel(product, parsedtoplevel)
        for item in inputTopLevel.findall('.//Node'):
            parseditem = ParseItem(item)
            #print parseditem
            #print str(parseditem['ident'])
            # if we haven't added the item to standard XML
            if (not ItemExist(components, parseditem['ident'])):
                quantity = Quantity(inputTopLevel, parseditem['ident'],True)
                parseditem['qty'] = str(quantity)
                createditem = CreateItem(components, parseditem)
                if(parseditem['type'] == 'Part'):
                    pass

                else:
                    subcomponent = SubElement(createditem,'subcomponent')
                    for child in item:
                        subcomponentparseditem = ParseItem(child)
                        if (not ItemExist(subcomponent, subcomponentparseditem['ident'])):
                            quantity = Quantity(item, subcomponentparseditem['ident'],False)
                            subcomponentparseditem['qty'] = str(quantity)
                            CreateSubComponent(subcomponent,subcomponentparseditem)
                          
    return product
 
def WriteStandardXML(inputfilename,outputfilename):
    product = ParseCubifyXMLToStandardXML(inputfilename)
    output = prettify(product)
    f = open(outputfilename,'w+')
    f.write(output)
    f.close()

def PrintStandardXML(filename):
    product = ParseCubifyXMLToStandardXML(filename)
    print prettify(product)

def testForFileName(argv): 
    length = len(sys.argv)
    if length < 2:
        return -1
    else: 
        infile = sys.argv[1]
        if not os.path.exists(infile):
            return -1
        else:
            return infile
# PrintStandardXML('AFPD0001_Cubify.XML')
WriteStandardXML('AFPD0001_Cubify.XML','AFPD0001_Standard.XML')
#input = testForFileName(sys.argv)
#if input != -1:
#    WriteStandardXML(input,'AFPD0001_Standard.XML')
#else:
#    print "File Not Found!"