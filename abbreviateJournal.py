import urllib
urls=['http://jabref.sourceforge.net/journals/journal_abbreviations_geology_physics.txt',
      "http://jabref.sourceforge.net/journals/journal_abbreviations_general.txt"]

urls=['http://people.su.se/~alau4517/jabref.wos.txt',] #this guy did a cool thing.. 
abbrevs=[]
for url in urls:
  z=urllib.urlopen(url)
  z.readline()
  z=[i.split("=") for i in z if (i[0]!='#' and '=' in i)]
  
  z=[(i.strip(),j.strip()) for i,j in z]
  abbrevs.extend(z)
  print "*",url
  
z=abbrevs
z2=z[:]
for i,j in z:
  
  if ':' in i:
    i=i.split(':')[0].strip()
  z2.append((i,j))
z=z2[:]
    
short2full=dict([(j.lower(),i) for i,j in z])
full2short=dict([(i.lower(),j) for i,j in z])

import cPickle as cp
with open("abbrev.pkl",'wb') as fout:
  cp.dump((short2full,full2short),fout)


print len(short2full)