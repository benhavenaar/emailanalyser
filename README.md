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

## Input/Output
It takes `.eml` files and creates an `.xlsx` file in the /src/scanresults folder. The `.xlsx` file consists of the found and scanned URLs in the body of the email. Besides that, authentication results/signatures are saved in this excel file beneath the table. The table is ordered by the 'malicious' column. 

### To do:
- Whitelist certain attachment files (.png/.gif... etc.) or not considering macro'd attachments.
- Make sure to check whether the scanresults folder exists (doesn't exist on github, only locally atm). If not, create it
- Add scan results to excel whenever a result is found instead of all together at the end. Might make filtering a bit harder, but the file read/filtered at the end again, or completely renewed when all data is found
