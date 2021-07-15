#!/bin/bash
{
	cd -- "$(find / -name main.py -path '*emailanalyser*/*src*/*' -type f -printf '%h' -quit)"
	git pull
} &> /dev/null
python3 main.py
