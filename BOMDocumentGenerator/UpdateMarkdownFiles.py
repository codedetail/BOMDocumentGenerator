
import csv
import BOMUtilities

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom


DefaultRow = {'ItemType':'','ID':'', 'Description1':'', 'Description2':'',	'Description3':'', 'Description4':'', 'Directory':'', 'Filename':'', 'Description':'', 'Distrib':'', 'PN':'', 'USD':'', 'QTY':'', 'Price':'', 'Manufacturer':'', 'Notes':'', 'URL':''}


#with open('AFPD0001.csv','rb') as csvfile:
#    reader = csv.reader(csvfile,delimiter=',',quotechar='|')
#    for row in reader: 
#      DefaultRow['ItemType'] = row[0]
#      DefaultRow['ID'] = row[1]
#      DefaultRow['Description1'] = row[2]
#      DefaultRow['Description2'] = row[3]
#      DefaultRow['Description3'] = row[4]
#      DefaultRow['Description4'] = row[5]
#      fileName = DefaultRow['ID'] + '.md'
#      descriptions = DefaultRow['Description1'] + DefaultRow['Description2'] + DefaultRow['Description3'] + DefaultRow['Description4']
#      print DefaultRow['ID']
#      print descriptions
#      BOMUtilities.AddNewMarkdownAutoGeneratedSection(fileName, DefaultRow['ID'], descriptions, DefaultRow['ItemType'])

root = ElementTree.parse('AFPD0001_Standard.XML')
components = root.find('./toplevel/components')
BOMUtilities.AddNewMarkdownAutoGeneratedSection(components)
