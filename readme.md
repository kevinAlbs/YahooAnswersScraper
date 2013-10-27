#Yahoo Answers Scraper

This python script is for fetching data about questions and answers from [Yahoo Answers](http://answers.yahoo.com). It uses the [Yahoo Answers API](http://developer.yahoo.com/answers/) to fetch questions from a single category at a time. 

##Prerequisites
You need Python installed (I had version 2.7.3) and the Python libraries [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) as well as [MySQLDB](http://sourceforge.net/projects/mysql-python/)

You need MySQL installed.

##Setup
First, set up your MySQL database which will be used to store the final data. A creation for the two tables (questions and answers) can be found in the file:

```
mysql-db-setup.sql
```

Import these to create the necessary tables, and then edit the lines in the scrape.py file to match your database:

```
HOST = <Your MySQL host>
USER = <Your MySQL username>
PW = <Your MySQL password>
DB = <The database containing the questions/answers tables>

```

Also, make any necessary changes to the numQuestions variable to specify how many questions you would like fetched.

##Usage
###Summary

```
python scrape.py -get=[questions|answers] -category=["Business & Finance"|"Health"|"Travel"|"Sports"|"Home & Garden"|"Entertainment & Music"|<custom category>]  [-num_questions=<number>] [-min_num_answers=<number>]
```

- get: tells whether you want to get questions or answers. To get answers, you first have to fetch the questions.
- category: the category from which you wish to fetch. This needs to be one of the six included, or you can find the category id yourself and add it to the catIDs dictionary.
- num_questions: the number of total questions you want to fetch when using -get=questions.
- min_num_answers: setting this to a number <b>n</b> will only parse questions having at least <b>n</b> answers. This can be useful in filtering unanswerered questions.

###Fetching Questions
Example for fetching questions from "Sports" category

```
python scrape.py -get=questions -category="Sports"
```

This will write all of the questions to the file: data/Sports.json

###Fetching Answers
Example for fetching answers from "Sports" category (assuming you have already fetched the questions)

```
python scrape.py -get=answers -category="Sports"
```

This will read all of the questions from data/Sports.json and write to your MySQL database both the questions and answers.

##Errors
Sometimes Yahoo Answers returns duplicate question ids causing MySQL errors on insertion. These errors are written in the errors.txt file, but should not effect the running of the program since the duplicates are ignored.

##Data Structure
TODO

##Implementation
It seems that the YQL table for the Yahoo Answers data only allows 50 questions to be returned at a single time. Therefore, this script loops to fetch 50 questions at a time until your desired amount is reached. This is fetched all into the data directory. When fetching questions, the data will go into:

'''
data/<category name>.json
'''

The reason that the questions are stored locally is to reduce the API calls to Yahoo since they are limited. This way, once you fetch the question data, you do not have to call the API again.

Once questions are stored the next thing to do is fetch the answers.

<hr/>
##Ideas:
- Yahoo Answers does provide API for answers given a question ID, but since we're only allowed 5000 API requests per day, this would be insufficient. Maybe request more from Yahoo.

##Issues:
- There doesn't seem to be a way to query for questions with more than 5 answers. This means we will probably have to go through many questions to find 1000 with 5 or more answers.
- Yahoo only shows downvotes when you sign in
- When fetching answers, I found a few duplicates in the question ids... so for now I modified mysql errors to write to a file instead of exiting as to not interrupt the program. Question id's are: 20131020103951AAJqaTE, 20131016175727AAa1l43, 20131015174409AAImTMz
- chosen_answer_timestamp and chosen_answer_award_timestamp did not get filled
- It seems like after so many questions are fetched, you get blank results back