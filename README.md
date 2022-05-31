# textgrid_edit.py
A script designed for easier musicological annotation in TextGrid files.

## necessary packages:
Use the command prompt to install the textgrid package for Python.
```
pip install textgrid
```

## purpose:
The script takes a given interval tier in a TextGrid file, and divides it up evenly and creates a new tier for it. Designed as a tool for musicological annotation in Praat software. Developed in conjunction with beat_detective.py.

https://github.com/hyukjekwon/Beat_Detective/blob/patch-2/beat_detective.py

## parameters/usage:
First, put the script and the desired TextGrid in the same file directory. Then run the following command with these parameters:
- file_name: must be the name of a TextGrid file
- tier: the number of the tier you want to divide up
- num_div: the number of divisions you want to do
```
python3 tier_div.py file_name tier num_div
```
After the script runs, it should print out a message telling you that the program worked successfully, and that a new tier was added.

## example:
Let's say I'm already annotating Ms. Jackson by Outkast, and I want to add a tier for 16th triplets because the lyrics don't fit with standard 16ths. The tier with 16th notes in it is tier 5, and I want to divide them by 3, so the appropriate command would be:
```
python3 tier_div.py ms-jackson.TextGrid 5 3
```
Assuming the tiers are organized in the same way as pre-set by beat_detective.py, a message should print out:

*"The 16th triplets tier has been added."*

And the new file will be created, named "new_ms-jackson.TextGrid"

## contact:
Email me for any questions: hyukjekwon@umass.edu
