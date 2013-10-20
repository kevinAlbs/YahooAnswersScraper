import json
import httplib, urllib
from bs4 import BeautifulSoup
import re
#script for retreiving 1000 questions from y/a data
numQuestions = 5 #number of questions desired from each category
numAllowed = 5 #number of results allowed by a single request
catIDs = {"Business & Finance": 396545013}
#fetches data from each category
def fetchData(cat):
	global numQuestions, numAllowed, catIDs
	print "Fetching from %s" % cat
	fname = "%s.json" % cat
	f = open(fname, 'w')
	f.write("[")
	first = True
	numSteps = int(numQuestions / numAllowed) #max of 50 can be retrieved from public API (or so I think)
	conn = httplib.HTTPConnection("query.yahooapis.com:80")
	for i in range(numSteps):
		s = "select * from answers.getbycategory(%d, %d) where category_id=%s" % (i * numAllowed, numAllowed, catIDs[cat])
		s = urllib.quote(s)
		conn.request("GET", "/v1/public/yql?q=%s&format=json&sort=ans_count_desc" % s)
		r = conn.getresponse()
		data = r.read()
		if not first:
			f.write(",")
		first = False
		f.write(data)
		print "%d of %d completed" % (i+1, numSteps)
	f.write("]")
	f.close()
	conn.close()
	print "File %s is complete" % fname 

jObj = [] #tmp
soup = []
def parseData(cat):
	global jObj, soup
	print "Parsing %s" % cat
	num_parsed = 0
	fname = "%s.json" % cat
	f = open(fname, 'r')
	fData = f.read()
	jObj = json.loads(fData)
	conn = httplib.HTTPConnection("answers.yahoo.com:80")
	for result in jObj:
		for q in result['query']['results']['Question']:
			#check if question has 5 or more answers
			if(int(q['NumAnswers']) > 0): #CHANGE
				print "Storing question: %s" % q['id']
				#Store question into database TODO

				#fetch page and scrape
				print q['id']
				conn.request("GET", "/question/index?qid=20100425114216AA802rx")
				r = conn.getresponse()
				data = r.read()
				soup = BeautifulSoup(data)
				#get all answers on this page

				#best answer has class 'answer best'
				#other answers just have class 'answer'
				answers = soup.select(".answer")
				best = soup.select(".answer.best")
				hasBest = False
				if len(best) == 1:
					hasBest = True

				for ans in answers:
					#get each attribute
					isBest = False
					if hasBest and ans == best[0]:
						isBest = True
					content = ans.find_all("div", class_="content")[0].get_text()
					upvotes = ans.find_all("li", class_="rate-up")
					print ans
					if len(upvotes) == 1:
						#use regex to read the number of votes
						s = upvotes[0].span.get_text()
						m = re.compile("^[0-9]+").match(s)
						upvotes = int(m.group(0))
					else:
						upvotes = 0
					#Yahoo only shows downvotes when signed in... maybe I will consider trying
					print isBest, upvotes

				
				print "Fetched"
				num_parsed += 1
				return
	conn.close()

	print "Loaded"

#fetchData("Business & Finance")
parseData("Business & Finance")
