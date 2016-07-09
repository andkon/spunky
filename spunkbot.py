"""
remaining problems:
[] how do i keep the pipeline full? I don't wanna have to push code for it to add songs
[] does it need a db? to store the lyrics? this is kinda related to the above.
[] twitter posting stuff. basically, it should cut off at the sentence that wouldn't go past 140 characters
[] maybe replace the \n -> ". " with a special character? maybe ".* " so that you can return to the \n for the tweet. see what spacy considers "significant punct"
and honestly, maybe try spunkify() without getting rid of newlines. see what it looks like

biebs = u"For all the times that you rained on my parade"/
u"And all the clubs you get in using my name" 
/You think you broke my heart, oh girl for goodness sake. You think I'm crying on my own, well I ain't"

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


import requests
MUSIXMATCH_BASE_URL = "http://api.musixmatch.com/ws/1.1/"
MUSIXMATCH_API_KEY = "d9ac0b26bcec0f138369f176fcb470c2"
chart = requests.get(MUSIXMATCH_BASE_URL + "chart.tracks.get", params={"f_lyrics_language": "en", "country": "us", "f_has_lyrics": True, "apikey": MUSIXMATCH_API_KEY})
ids = map(lambda x: x['track']['track_id'], chart.json()['message']['body']['track_list'])

cleaned_lyrics = []
for id in ids:
	r=requests.get(MUSIXMATCH_BASE_URL+"track.lyrics.get", params={"apikey":MUSIXMATCH_API_KEY, "track_id":id})
	lyrics_body = r.json()['message']['body']['lyrics']['lyrics_body']
	lyrics_body.replace("\n", ".* ")
	cleaned_lyrics.append(lyrics_body)

# now post to twitter

