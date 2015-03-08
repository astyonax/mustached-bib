import xml.etree.cElementTree as ET
import os
scriptpath= os.path.dirname(os.path.realpath(__file__))
def getconversion():
  try:
    tree=ET.parse(scriptpath+"/unicode.xml")
  except IOError:
    print "you should download the xml file, first"
  root=tree.getroot()
  chars=root.findall("character")
  ascii=[chr(i) for i in xrange(128)]
  out=[]
  for char in chars:
    try:
        id=int(char.attrib['dec'])
        if id<=127:
            raise ValueError
        if id in [0x2028,0x2029]:
           raise ValueError
        latex=char.find("latex").text
        if latex in ascii:
            raise ValueError
        if 'fontencoding' in latex or 'char' in latex or '\\' not in latex:
            raise ValueError
        out.append((id,latex))
    except (AttributeError,ValueError):
        pass
  
  return dict(out)
    
if __name__=='__main__':
   out=getconversion()
   print '\n'.join(['%s %s' %(i,j) for i,j in out.iteritems()])
   
