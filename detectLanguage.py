"""
This script uses the model files(ROOTDIR/lang.model) to detect
the language of input text.
"""

from __future__ import division
from config import *
import base64
import bz2
import cPickle
import numpy as np


def getLangID(sentence):
	"""
	Return the language corresponding to the highest probability.

	Arguments:
	sentence - The input sentence who language needs to be identified
	"""
	probs = []
	for vocab,counts in models:
		prob = 0
		for i in xrange(len(sentence)-3):
			threeGram = sentence[i:i+3]
			fourGram  = sentence[i:i+4]

			if threeGram in vocab:
				threeGramIdx   = vocab.index(threeGram)
				threeGramCount = counts[0,threeGramIdx]
				
				if fourGram in vocab:
					fourGramIdx   = vocab.index(fourGram)
					fourGramCount = counts[0,fourGramIdx]
					
					prob += np.log(fourGramCount/threeGramCount)
		print prob
		probs.append(prob)
	return LANGUAGE_NAMES[probs.index(max(probs))]


models = []
for lang in LANG:
	with open(MODELDIR+lang+'.model') as filename:
		string = filename.read()
		model = cPickle.loads(bz2.decompress(base64.b64decode(string)))
		models.append(model)
