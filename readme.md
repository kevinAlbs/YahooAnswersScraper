Ideas:
- Yahoo Answers does provide API for answers given a question ID, but since we're only allowed 5000 API requests per day, this would be insufficient. Maybe request more from Yahoo.
- Probably throw this into MySQL database, dump and send

Issues:
- There doesn't seem to be a way to query for questions with more than 5 answers. This means we will probably have to go through many questions to find 1000 with 5 or more answers.
- Yahoo only shows downvotes when you sign in