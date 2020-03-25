# Word Counter
This assigment was written using Python 3.7.3 and Flask 1.1.1

## Description
#### The app supports 2 endpoints:
1. POST request to process input:
   http://127.0.0.1:5000/count/<input_type> 
   
   input type can be one of:
   - 'url' - request body to include the desired url
   - 'local' - request body to include the absolute path to a ".txt" file
   - 'text' - request body is the text to process.
      e.g.:
       ```
      curl --location --request POST 'http://127.0.0.1:5000/count/text' \
      --header 'Content-Type: text/plain' \
      --data-raw 'Lorem ipsum dolor sit amet........
      ```

2. GET request to retrieve word occurences:
   http://127.0.0.1:5000/statistics/<query_word>
   
   e.g.:
   ```curl --location --request GET 'http://127.0.0.1:5000/statistics/corona'```
   
The text processed by the app is being tokenized based on spaces.
each token is stripped from all non alpha characters
e.g.: 
   - me2, m2e, 2me -> me

#### How it works
When a request for process is made, based on the input type, the relevant flow will trigger.

In order to deal with potentially big input the data from files and url is being read by chunks.

For a txt file:

```buf = file.read(_READ_CHUNK_SIZE) ```

To avoid loss of data, the file is being read until the first whitespace:

```
while not buf[-1].isspace():
ch = file.read(1)
```

For url:

```
response.iter_content(chunk_size=_READ_CHUNK_SIZE, decode_unicode=True)
```

To avoid loss of data, the buffer is being splitted by the index of the last whitespace and the rest is being concated to the next buffer.

The buffer then being tokenized, cleaned, summed in a `Collections.Counter` object and updated to the `statistics.json` file.

 
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
 - Processed text - space delimmeted text (new lines and tabs are optional)
 - The main challange of the app is to deal with very large input
 - URL input - valid url format
 - Local file - absolute path to a local txt file
 - After clarification - requests are being processed **synchronously** - no support for concurrent requests and file locking.

