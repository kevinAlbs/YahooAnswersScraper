Ideas:
- Yahoo Answers does provide API for answers given a question ID, but since we're only allowed 5000 API requests per day, this would be insufficient. Maybe request more from Yahoo.
- Probably throw this into MySQL database, dump and send

Issues:
- There doesn't seem to be a way to query for questions with more than 5 answers. This means we will probably have to go through many questions to find 1000 with 5 or more answers.
- Yahoo only shows downvotes when you sign in
- When fetching answers, I found a few duplicates in the question ids... so for now I modified mysql errors to write to a file instead of exiting as to not interrupt the program. Question id's are: 20131020103951AAJqaTE, 20131016175727AAa1l43, 20131015174409AAImTMz
- chosen_answer_timestamp and chosen_answer_award_timestamp did not get filled