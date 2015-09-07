# mustached-bib

Note that this program may be not useful when zotero is used in combination with the "better bibtex" plugin.

---
A CLI program to clean Zotero's bibtex files.
This program takes an input bibtex file (ideally produced by zotero)
and outputs a stripped/corrected version.

At the moment, it removes every entry:
* of type 'misc'
* duplicated entry
* entries w/o a title

For every entry:
* it removes some not-so-useful field:

  'url','file','abstract','copyright','note','month' 
 
  this list can be configured in the __JSON__ file cleanbib.json:excludefield
* it clears the key names from the tedious _???? markers
* it tries to makes all titles with a uniform style



This is a pseudo-working version: it does what I expect, but it's not tested against 
difficult cases.

At the moment I'm using the code from varius projects:
* latex.py is from (D. Eppstein, October 2003.) http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252124
* unicode.xml is from TODO
* the folder bibtexparser  https://bibtexparser.readthedocs.org/en/latest/
* the journal abbreviations list is from http://people.su.se/~alau4517/jabref.wos.txt
(see also abbreviateJournal.py )

