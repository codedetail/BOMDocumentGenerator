
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
    print rough_string
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def AddImagestoStandardXML(filename):
    # high level XML name
    
    root = ElementTree.parse(filename)

    print
    if os.path.exists(IMAGE_DIRECTORY):
        print 'A'
        dirs = os.listdir(IMAGE_DIRECTORY)
        for image in dirs:
           print image
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