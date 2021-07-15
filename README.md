# emailanalyser
An email analyser script that uses online API's to determine if an email contains phishing or viruses. All rights are reserved by Ordina.

## Install
A few steps are necessary to install all requirements for this program.

1. Clone the `requirements.sh` and `emailanalyser.sh` file
2. Create a VirusTotal account and collect your API key
3. Edit the requirements.sh file and change `<PASTE VT API KEY BETWEEN QUOTES>` to your API key
4. Make the shell scripts executable with `chmod a+x *.sh`
5. Execute `./requirements.sh`. This will install python3 on your machine and the necessary modules/libraries in order to run the program
6. Execute `./emailanalyser.sh` in order to start the program.

If you want to manually run the program, go to the `/src` folder and run `python3 main.py`

This program has mainly been tested with `.eml` files.

## Recommended use
It is adviced that you run this script within a save environment, such as a VM.
This is due to the fact that it automatically downloads attachments and saves it to the `attachments` folder. 
Upon closing the program (by selecting option 2) it will delete all downloaded attachments.

## Input/Output
It takes `.eml` files and creates an `.xlsx` file in the /src/scanresults folder. The `.xlsx` file consists of the found and scanned URLs in the body of the email. Besides that, authentication results/signatures are saved in this excel file beneath the table. The table is ordered by the 'malicious' and 'suspicious' column. 

