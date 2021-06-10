# emailanalyser
An email analyser script that will use online API's to determine if an email contains phishing or viruses

## How to use
You need python 3.8+ in order to run this program
Run the command `python -m pip install -r requirements.txt` located in the src file

Then simply run `python main.py` located in the src folder.

This program only takes in .eml files and analyses them.
In order to use the program, you'll need a VirusTotal API key. This key needs to be added to a constants.py file which is obviously an ignored file in this project.

Add `VT_API_KEY = 'api-key-here'` and save it as constants.py in your src folder.
