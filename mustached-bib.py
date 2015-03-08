import bibtexparser
import latex 
latex.register()
import string 
import sys
import os
import json

script_path=os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,script_path)

#def jsonsavecfg():
  #cfgout=json.dumps({'excludewords':['a','and','as','if','as','of','for','with','where','when','how','why','over','that','at','the','by','in'],
   #'excludefield':['url','file','abstract','copyright','note','month','keyword','urldate','language','issn','link']})
  #with open('cleanbib.json','w') as fout:
   #fout.write(cfgout)
  
  #exit()

#jsonsavecfg()

def loadconfig(fin):
  data=json.loads(fin.read())
  return data

cfgfd='cleanbib.json'
with open(cfgfd,'r') as fin:
  config=loadconfig(fin)

def norm_title(txt):
  """
  Title format:
  capitalize only names and verbs and 1st word
  """
  exclude=config['excludewords']
  txt=txt.strip().split(' ')
  txt=[i.strip() for i in txt]
  #txt[0]=txt[0].capitalize()
  for i,j in enumerate(txt):
    if j.lower() not in exclude and ( i==0 or j.upper()!=j) and (j[0]!='{' and j[-1]!='}'):
      txt[i]=j.capitalize()
    else:
      txt[i]=j.lower()
      
  txt=' '.join(txt)
  return txt

def cleanbib(fin,fout):
  # ========================
  #  load bibliography 
  # ========================
  with open(fin) as bibin:
      bstr=bibin.read()
  bd=bibtexparser.loads(bstr)

  # ========================
  #  TODO expand this section for clarity
  #  config loaded via JSON
  #  filter unwanted entries of type misc and those w/o title
  # ========================
  n=[i for i in bd.entries if i['type']!='misc' and 'title' in i.keys()]
  # ========================
  #  filter unwanted fields
  #  remove empty filels
  #  remove url, file,...
  # ========================
  n=[dict([(k,v)  for k,v in i.iteritems() if k not in config['excludefield'] and len(k) and v.strip()!='']) for i in n]

  # ========================
  #  clean missing field in id
  #  and make duplicates list
  # ========================
  duplicated=[]
  changed_ids=[]
  for i in n:
    #try:
      #authors=i['author'].split("and")
      #authors=[[word.strip() for word in j.split(',')] for j in authors]
      #for j,v in enumerate(authors):
	#surname,name =v
	#names=name.split(" ")
	
	#names=name.split("-")
	
	#names=[n[0].upper() for n in names]
	
      #print authors
    #except:
      #pass
    oldid=i['id']
    i['id']=i['id'].replace('_????','')
    low=map(chr, range(97, 123))
    upp=map(chr, range(97, 123))
    letters=low+upp+['_','-',]+list('0123456789')
    i['id']=''.join([j for j in i['id'] if j in letters])
    newid=i['id']
    if oldid!=newid:
      changed_ids.append((oldid,newid))
    try:
      string.atoi(i['id'].split('-')[-1])
      duplicated.append(i['id'])
    except (IndexError,ValueError):
      pass

  # ========================
  #  remove duplicates
  # ========================
  new=[]
  for i in n: 
    if i['id'] not in duplicated:
      new.append(i)
  n=new[:]
  
  # ========================
  #  normalize title format
  # ========================
  for i in n:
    i['title']=norm_title(i['title'])

  # ========================
  #  short or long journal names
  #  based on output of abbreviateJournal.py (in the same folder)
  # ========================
  import cPickle
  with open(script_path+"/abbrev.pkl","rb") as finabb:
    short2full,full2short = cPickle.load(finabb)
  for i in n:
    try:
      journal=i['journal'].strip().lower()
    except KeyError:
      continue
    if 'the' == journal[:3]:
      #the list has not The ..
      journal=journal[3:].strip()
    if ':' in journal:
      journal=journal.split(':')[0].strip()
    try:
      i['journal']=full2short[journal]
      #print '*'
    except KeyError:
      print journal ,"not in abbrv list"
      #pass
      
  # ========================
  #  saving
  # ========================
  bd2=bd
  bd2.entries=n
  # encode to latex format to escape non ascii chars to latex format
  bstr_out=bibtexparser.dumps(bd2).encode('latex')
  
  print >> open(fout,"w"),bstr_out
  
  # ========================
  #  reporting
  # ========================
  print len(n),"valied entries"
  print len(duplicated),"duplicated entries were removed"
  print '\n'.join(sorted(duplicated))
  print '--'*80
  print "capitalization style"
  print '--'*80
  txt="Look At The Fuzzy fox that jumps over The bench"
  print 'OLD',txt
  print 'NEW',norm_title(txt)
  if len(changed_ids):
    print '--'*80
    print "BEWARE, some ids where changed"
    print '--'*80
    for o,n in changed_ids:
      print o,'->',n


if __name__=='__main__':
  import argparse
  parser = argparse.ArgumentParser(description="""
A nifty program to clean zotero\' bibtex files.
This program takes an input bibtex file (ideally produced by zotero)
and outputs a stripped/corrected version. """)
  parser.add_argument('--fin', metavar='InputFileName', type=str, nargs=1,action="store",
                   help='The input bibtex file',required=1)
  parser.add_argument('--fout', metavar='outputFileName', type=str, nargs=1,action="store",
                   help='The output bibtex file',required=1)
  
  
  args = parser.parse_args()
  fin=args.fin[0]
  fout=args.fout[0]
  print "input file:",fin
  print "output file:", fout
  
  
  
  cleanbib(fin,fout)
