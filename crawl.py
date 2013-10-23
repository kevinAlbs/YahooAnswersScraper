#!/usr/bin/python

import json
import httplib, urllib
from bs4 import BeautifulSoup
import re
import _mysql
import sys
from time import gmtime, strftime


#script for retreiving 1000 questions from y/a data

#config globals
numQuestions = 12000 #number of questions desired from each category
numAllowed = 50 #number of results allowed by a single request

# I found the category ids from just going to the category on the Yahoo answers website, the category id is in the url under the sid parameter
# E.g. Going to the health category takes you here: http://answers.yahoo.com/dir/index?sid=396545018
# Also useful to double check is using the online YQL console they provide: http://developer.yahoo.com/yql/console
catIDs = {"Business & Finance": 396545013, "Health" : 396545018}
HOST = "localhost"
USER = "root"
PW = "102533"
DB = "ya"

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
	global jObj, soup, HOST, USER, PW, DB, numQuestions
	print "Parsing %s" % cat
	num_parsed = 0
	fname = "%s.json" % cat
	f = open(fname, 'r')
	err = open("errors.txt", "a");
	err.write("Time of Crawl: %s\n" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	fData = f.read()
	jObj = json.loads(fData)
	min_nums = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
	num_blank = 0
	conn = httplib.HTTPConnection("answers.yahoo.com:80")
	sqlCon = None
	count = 1
	try:
		sqlCon = _mysql.connect(HOST, USER, PW, DB)
		for result in jObj:
			if result['query']['results'] is None:
				print "Blank question set"
				num_blank += 1
			else:
				for q in result['query']['results']['Question']:
					try:
						#check if question has 5 or more answers
						for key in min_nums.keys():
							if(int(q['NumAnswers']) >= key):
								min_nums[key] += 1
						if(int(q['NumAnswers']) >= 5):
							print "Processing question %d" % (count)
							count += 1
							print "Storing question: %s" % q['id']
							#Store question into database
							#Please excuse the following code, I am relatively new to Python and did not know of a nice way to prepare MySQL statments... will hopefully clean
							d = {}
							d['id'] = _mysql.escape_string(q['id'])
							d['type'] = _mysql.escape_string(q['type'])
							d['subject'] = _mysql.escape_string(q['Subject'].encode('utf-8'))
							d['content'] = _mysql.escape_string(q['Content'].encode('utf-8'))
							d['date'] = _mysql.escape_string(q['Date'])
							d['specific_category'] = _mysql.escape_string(q['Category']['content'].encode('utf-8'))
							d['category_id'] = _mysql.escape_string(q['Category']['id'])
							d['user_id'] = _mysql.escape_string(q['UserId'])
							d['user_nickname'] = "Not Specified"
							if q['UserNick'] is not None:
								d['user_nickname'] =_mysql.escape_string(q['UserNick'].encode('utf-8'))
							d['num_answers'] = int(q['NumAnswers'])
							d['num_comments'] = int(q['NumComments'])
							d['chosen_answerer_id'] = ""
							d['chosen_answer_timestamp'] = "NULL" 
							d['chosen_answer_award_timestamp'] = "NULL"
							if q['ChosenAnswererId'] is not None:
								d['chosen_answerer_id'] = _mysql.escape_string(q['ChosenAnswererId'])
								d['chosen_answer_timestamp'] = "FROM_UNIXTIME(%d)" % int(q['ChosenAnswerTimestamp'])
								d['chosen_answer_award_timestamp'] = "FROM_UNIXTIME(%d)" % int(q['ChosenAnswerAwardTimestamp'])
							d['category'] = cat
							sqlCon.query("INSERT INTO question (`id`, `type`, `subject`, `content`, `datetime`, `specific_category`, `category_id`, `user_id`, `user_nickname`, `num_answers`, `num_comments`, `chosen_answer_id`, `chosen_answer_timestamp`, `chosen_answer_award_timestamp`, `category`) VALUES(\"%s\", \"%s\", \"%s\",\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", %d, %d, \"%s\", \"%s\", \"%s\", \"%s\")" % (d['id'],d['type'],d['subject'],d['content'],d['date'],d['specific_category'],d['category_id'],d['user_id'],d['user_nickname'],d['num_answers'],d['num_comments'],d['chosen_answerer_id'],d['chosen_answer_timestamp'],d['chosen_answer_award_timestamp'], d['category']))
							#fetch page and scrape
							#20100425114216AA802rx
							conn.request("GET", "/question/index?qid=%s" % q['id'])
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
								isBest = 0
								if hasBest and ans == best[0]:
									isBest = 1

								content = ans.find_all("div", class_="content")[0].get_text()
								upvotes = ans.find_all("li", class_="rate-up")
								time_posted = ans.find_all("abbr")[0]['title']

								
								if len(upvotes) == 1:
									#use regex to read the number of votes
									s = upvotes[0].span.get_text()
									m = re.compile("^[0-9]+").match(s)
									upvotes = int(m.group(0))
								else:
									upvotes = 0

								sqlCon.query("INSERT INTO answer (`qid`, `is_best`, `time_posted`, `upvotes`, `content`) VALUES(\"%s\", %d, \"%s\", %d, \"%s\")" % (_mysql.escape_string(q['id']), isBest, time_posted, upvotes, _mysql.escape_string(content.encode('utf-8'))))
								#Yahoo only shows downvotes when signed in... maybe I will consider trying
								#print isBest, upvotes, time_posted, content[0:10]
							num_parsed += 1
							#return
					except _mysql.Error, e:
						err.write("Error %d: %s" % (e.args[0], e.args[1]))
						err.write("\n")
						print "MySQL error occured"
	except _mysql.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		if sqlCon:
			sqlCon.close()
	conn.close()
	err.close()
	f.close()
	print "Finished"
	print "%d blank sets" % num_blank
	for key in min_nums.keys():
		print "%d or more : %d" % (key, min_nums[key])

#fetchData("Business & Finance")
#parseData("Business & Finance")
fetchData("Health")