# emailanalyser
An email analyser script that will use online API's to determine if an email contains phishing or viruses

## How to use
You need python 3.8+ in order to run this program
Run the command `python -m pip install -r requirements.txt` located in the src file

Then simply run `python main.py` located in the src folder.

This program only takes in .eml files and analyses them.
In order to use the program, you'll need a VirusTotal API key. This key needs to be added to a constants.py file which is obviously an ignored file in this project.

Add `VT_API_KEY = 'api-key-here'` and save it as constants.py in your src folder.

## Recommended use
It is adviced that you run this script within a save environment, such as a VM.
This is due to the fact that it automatically downloads attachments and saves it to the `attachments` folder. 
Upon closing the program (by selecting option 2) it will delete all downloaded attachments.

### To do:
- Collect the list of attachments and analyse/scan these with the API
...* Currently it just downloads the attachments
- Filter the header contents and retrieve the "received-spf" and "authentication-results" items
- Clean up the menu/main.py
