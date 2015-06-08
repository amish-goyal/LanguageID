"""
This script creates text files from chunks of XML documents.
The text files are stored in a directory hierarchy as follows:

TARGETDIR
	-language1
		-textfile1
		-textfile2
		- ...
	-language2
		-textfile1
		-textfile2
		- ...

The script assumes the XML documents to be in the following hierarchy:

ROOTDIR
	-language1
		-file1
		-file2
		- ...
	-language2
		-file1
		-file2
		- ...
"""


from config import *
import os
import xml.etree.ElementTree as ET


CHUNKSIZE = 50
TOTALDOCS = 10


def generateXML_Filepaths(rootdir):
	"""Generate filepaths of all XML files present in the root folder.

	Arguments:
	rootdir - name of the root directory (string)
	"""
	for subdir, dirs, files in os.walk(rootdir):
		for filename in files:
			if filename.endswith('.xml'): 
				filepath = subdir + '/' + filename
				yield filepath


def parseXML(filepath):
	"""Return concatenated string of all the text in the XML document.

	Arguments:
	filepath - the complete filepath of the XML file (string)
	"""
	try:
		tree = ET.parse(filepath)
		root = tree.getroot()

		text = ''
		for paragraph in root.iter(tag = 'p'):
			text += ' ' + paragraph.text

		return text
	except:
		return ""


def generateDocs(lang, chunkSize, totalDocs):
	"""Generate text files from the XML documents

	Arguments:
	lang 	  - The language of the text content
	chunkSize - Total XML files used for one document
	totalDocs - Total number of documents to be generated
	"""
	docCount = 0
	chunkCount = 0
	text = ''

	print "Language: ", lang

	for filepath in generateXML_Filepaths(ROOTDIR+lang):
		text += ' ' + parseXML(filepath)
		chunkCount += 1
		
		if chunkCount == chunkSize:
			print "Creating document ",docCount
			docCount += 1

			with open(TARGETDIR+lang+'/'+lang+'-'+str(docCount)+'.txt','w') as filename:
				filename.write(text.encode('utf-8'))
				text = ''
				chunkCount = 0
		
		if docCount == totalDocs:
			break


if __name__ == "__main__":
	for lang in LANG:
		generateDocs(lang,CHUNKSIZE,TOTALDOCS)