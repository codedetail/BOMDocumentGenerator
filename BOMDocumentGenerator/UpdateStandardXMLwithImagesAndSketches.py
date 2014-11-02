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

# convert Cubify drawing to readiable XML file format
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom


IMAGE_DIRECTORY = "./images"

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem,'utf-8')
    #print rough_string
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def AddImagestoStandardXML(filename):
    # high level XML name
    
    root = ElementTree.parse(filename)

    #print
    if os.path.exists(IMAGE_DIRECTORY):
        #print 'A'
        dirs = os.listdir(IMAGE_DIRECTORY)
        for image in dirs:
           #print image
           searchObj = re.search(  r'(.*)_SCH.png', image, re.M|re.I)
           if (searchObj):
               name = searchObj.group(1)
               for item in root.findall('./toplevel/components/item'):
                   ident = item.findall('ident')
                   test = ident[0].text
                   if (test == name):
                        imagefile = name + '_SCH.png'
                        temp = SubElement(item,'image')
                        temp.text = imagefile
    return root.getroot()

def WriteImagestoStandardXML(filename):

    root = AddImagestoStandardXML(filename)
    output = prettify(root)
    f = open(filename,'w+')
    f.write(output)
    f.close()

WriteImagestoStandardXML('AFPD0001_Standard.XML')