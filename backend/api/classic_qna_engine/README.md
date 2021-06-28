#Classic

First install all dependencies
* For UNIX/macOS
    1. run `pip3 install -r requirements.txt`
    2. additionally run `pip3 install -U textblob` and `python3 -m textblob.download_corpora`

* For Windows
    1. run `py -m pip3 install -r requirements.txt`
    2. additionally run `pip3 install -U textblob` and `python3 -m textblob.download_corpora`
    
Next make sure to start backend
* in tutorai/backend/crawling/ run `npm start`

Next make sure to start flask api
* in jetbrains run api.py

Finally classic engine api can be accessed by:
* localhost:5000/tutorai/classic/<user_question>/<moses_module_number>
* Make sure to enter user_question with spaces between words and without a question mark
* Example calls:
    * localhost:5000/tutorai/classic/Wie viele Leistungspunkte/40017
    * localhost:5000/tutorai/classic/any requirements needed/20145
    