#!/bin/bash
echo "Preparing python3 install" 
sudo apt update &> /dev/null
sudo apt install software-properties-common -y &> /dev/null
echo "Adding deadsnakes repository for python" 
sudo apt-add-repository ppa:deadsnakes/ppa "" &> /dev/null
sudo apt update &> /dev/null
echo "Installing python3.9" 
sudo apt install python3.9 -y &> /dev/null
echo "Preparing pip install"
sudo apt-add-repository universe &> /dev/null
echo "Installing pip" 
sudo apt install python3-pip -y &> /dev/null
echo "Install python3 libraries..."
echo "Installing pandas"
python3 -m pip install pandas &> /dev/null
echo "Installing openpyxl"
python3 -m pip install openpyxl &> /dev/null
echo "Installing tkinter"
sudo apt install python3-tk -y &> /dev/null
echo "Installing git"
sudo apt install git -y &> /dev/null
echo "Cloning into repository"
git clone https://github.com/benhavenaar/emailanalyser &> /dev/null
echo "VT_API_KEY = '<PASTE VT API KEY BETWEEN QUOTES>'" > ./emailanalyser/src/constants.py
echo "Remove emoji font as git/linux doesn't like that"
sudo apt remove --purge fonts-noto-color-emoji -y &> /dev/null
