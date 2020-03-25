# Word Counter
This assigment was written using Python 3.7.3 and Flask 1.1.1

## Description
#### The app supports 2 endpoints:
1. POST request to process input:
   http://127.0.0.1:5000/count/<input_type> 
   
   input type can be one of:
   - 'url' - request body to include the desired url
   - 'local' - request body to include the absolute path to a ".txt" file
   - 'text' - request body is the text to process

2. GET request to retrieve word occurences:
   http://127.0.0.1:5000/statistics/<query_word>
   
The text processed by the app is being tokenized based on spaces.
each token is stripped from all non alpha characters
e.g.: 
   - me2, m2e, 2me -> me

   
## How to run   
### Install

In project folder run:

```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```
### Run
Start the app by running:

```$ python app.py```


## Project Assumptions
 - processed text - space delimmeted text (new lines and tabs are optional)
 - The main challange of the app is to deal with very large input
 - url input - valid url format
 - local file - absolute path to a local txt file
 - after clarification - requests are being processed **synchronously**

