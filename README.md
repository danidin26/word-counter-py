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
   
## How to run

 
