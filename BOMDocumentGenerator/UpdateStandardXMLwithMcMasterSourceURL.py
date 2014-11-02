
import csv
import BOMUtilities

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

DefaultRow = {'ItemType':'','ID':'', 'Description1':'', 'Description2':'',	'Description3':'', 'Description4':'', 'Directory':'', 'Filename':'', 'Description':'', 'Distrib':'', 'PN':'', 'USD':'', 'QTY':'', 'Price':'', 'Manufacturer':'', 'Notes':'', 'URL':''}

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem,'utf-8')
    print rough_string
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def AddBomInformationtoStandardXML(filename):

    root = ElementTree.parse(filename)

    with open('AFPD0001-McMaster-10-4.csv','rb') as csvfile:
            reader = csv.reader(csvfile,delimiter=',',quotechar='|')
            for row in reader: 
              DefaultRow['ID'] = row[0]
              DefaultRow['Description4'] = row[6]
              if not (''==row[6]):
                  name = row[0]
                  for item in root.findall('./toplevel/components/item'):
                        ident = item.findall('ident')
                        url = item.findall('url')
                        if not (url):
                            test = ident[0].text
                            if (test == name):
                                 temp = SubElement(item,'url')
                                 temp.text = "http://www.mcmaster.com/#" + row[6]
    return root.getroot()

def WriteBOMtoStandardXML(filename):

    root = AddBomInformationtoStandardXML(filename)
    output = prettify(root)
    f = open(filename,'w+')
    f.write(output)
    f.close()

WriteBOMtoStandardXML('AFPD0001_Standard.xml')