"""
biebs = u"For all the times that you rained on my parade. And all the clubs you get in using my name. You think you broke my heart, oh girl for goodness sake. You think I'm crying on my own, well I ain't"

import spacy
en_nlp = spacy.load('en')
doc = en_nlp(biebs)
from spunkbot import spunkify
spunkify(doc)
"""

def spunkify(doc):
	p = ""
	for t in doc:
		if t.dep_ == "dobj":
			# this should only 
			if t.lemma_ != t.orth_:
				p += "spunk" + t.suffix_ + t.whitespace_
			else:
				p += "spunk" + t.whitespace_
		elif t.dep_ == "nsubj":

			if t.lower_ != "you" and t.lower_ != "i":
				# don't change "you" or "i" to spunk
				p += "spunk" + t.suffix_ + t.whitespace_
			else:
				p += t.text_with_ws
		elif t.dep_ == "ROOT" and t.pos_ == "VERB":
			"""not if the verb """
			# elif t.tag_ == "VBP":
			if t.tag_ == "VBD":
				sub = map(lambda x: x.lower_, filter(lambda x: x.lower_ == "you" and x.dep_ == "nsubj", t.subtree))
				if len(sub) > 0:
					# "you" is the noun subject
					sub2 = filter(lambda x: x.dep_ == "dobj", t.subtree)
					# only spunk if there isn't a dobj in the subtree
					if len(sub2) == 0:
						p += "spunked" + t.whitespace_
					else:
						p += t.text_with_ws
				else:
					p += "spunked" + t.whitespace_
			else:
				p += t.text_with_ws
		elif t.dep_ == "ccomp" and t.pos_ == "VERB" and t.tag_ == "VBG":
			# only spunk if there's not a dobj that has spunk in it in the subtree
			dobjs = filter(lambda x: x.dep_ == "dobj", t.subtree)
			if len(dobjs) == 0:
				p += "spunk" + t.suffix_ + t.whitespace_
			else:
				p += t.text_with_ws
		else:
			p += t.text_with_ws
	return p

def diagnose(doc):
	for t in doc:
		print t.dep_ + ", " + t.pos_ + "/" + t.tag_  + ": " + t.lower_

"""
# problem rn: 
rained => spunkned
think => spunkink

"Whenever there's a verb where "you" is the noun subject, you should first look for a dobj."
"For all the times that you spunkned on my parade. And all the clubs you get in using my spunk. You spunkink you broke my spunk, oh girl for goodness sake. You spunkink I'm crying on my own, well I ain't"

Now:
For all the times that you spunked on my parade. And all the clubs you get in using my spunk. You think you broke my spunk, oh girl for goodness sake. You spunked I'm crying on my own, well I ain't
so the problem is:
"think" (ROOT, VERB/VBP) => spunked
"""