"""
This script stores character N gram models for various languages into compressed
files in the format: ROOTDIR/lang.model

The indexed documents that are processed to generate these models are stored in
a directory hierarchy as follows:

ROOTDIR
	-language1
		-textfile1
		-textfile2
		- ...
	-language2
		-textfile1
		-textfile2
		- ...
"""


INDEXRANGE = (1,11)
NGRAMRANGE = (3,4)


from config import *
from sklearn.feature_extraction.text import CountVectorizer
import base64
import bz2
import cPickle


def sentenceGenerator(lang, docRange):
	"""Generator that yields sentences from a range of indexed text documents.

	Arguments:
	lang     - The language of the text content
	docRange - The range of the indexed documents to be processed
	"""
	for i in xrange(docRange[0], docRange[1]):
		with open(ROOTDIR+lang+'/'+lang+'-'+str(i)+'.txt') as filename:
			text = filename.read()
			for sentence in text.split('.'):
				yield sentence


def createCharNgramModel(lang, docRange, ngramRange):
	"""Stores (vocabulary, character N gram counts) tuples in compressed format

	Arguments:
	lang 	   - The language of the text content
	docRange   - The range of the indexed documents to be processed
	ngramRange - The range of character N grams to be calculated
	"""
	print lang
	Counter = CountVectorizer(input='content', analyzer='char', ngram_range=ngramRange)
	Counts = Counter.fit_transform(sentenceGenerator(lang, docRange))
	Vocab = Counter.get_feature_names()
	totalCounts = Counts.sum(axis=0)

	model = Vocab, totalCounts
	string = base64.b64encode(bz2.compress(cPickle.dumps(model)))
	with open(MODELDIR+lang+'.model','w') as f:
		f.write(string)


if __name__ == "__main__":
	for lang in LANG:
		print "Creating Character N Gram Models for:\n"
		createCharNgramModel(lang, INDEXRANGE,NGRAMRANGE)