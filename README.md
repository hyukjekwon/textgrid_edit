# textgrid_edit.py
A script designed for easier musicological annotation in TextGrid files.

## necessary packages:
Use the command prompt to install the textgrid package for Python.
```
pip install textgrid
```

## purpose:
Depending on the flags argument, you can either swap the position of two tiers, remove any given interval, or subdivide any tier into any number. Designed as a tool for musicological annotation in Praat software. Developed in conjunction with beat_detective.py.

https://github.com/hyukjekwon/Beat_Detective/blob/patch-2/beat_detective.py

## parameters/usage:
file_name: name of a given TextGrid file

For interval removal:
  - tier: the number of the tier you want to remove from
  - interval: the number of the interval you want to remove
```
python3 textgrid_edit.py file_name -r tier interval
```
For tier swapping:
  - tier_no_1: the number of the 1st tier you want to swap
  - tier_no_2: the number of the 2nd tier you want to swap
```
python3 textgrid_edit.py file_name -s tier_no_1 tier_no_2
```
For moving a single tier:
  - tier_no: the number of the tier you want to move
  - destination: the number of the position you want to move the tier to
```
python3 textgrid_edit.py file_name -m tier_no destination
```
For moving multiple tiers:
  - front: the highest of the tiers you want to move
  - back: the lowest of the tiers you want to move
  - destination: the number of the position you want to move the tier to
```
python3 textgrid_edit.py file_name -mm front back destination
```
For subdivision:
  First, put the script and the desired TextGrid in the same file directory. Then run the following command with these parameters:
  - tier: the number of the tier you want to divide up
  - num_div: the number of divisions you want to do
```
python3 textgrid_edit.py file_name -d tier num_div
```
After the script runs, it should print out a message telling you that the program worked successfully, and that a new tier was added.

## example:
Let's say I'm already annotating Ms. Jackson by Outkast, and I want to add a tier for 16th triplets because the lyrics don't fit with standard 16ths. The tier with 16th notes in it is tier 5, and I want to divide them by 3, so the appropriate command would be:
```
python3 textgrid_edit.py ms-jackson.TextGrid -d 5 3
```
Assuming the tiers are organized in the same way as pre-set by beat_detective.py, a message should print out:

*"The 16th triplets tier has been added."*

And the new file will be created, named "new_ms-jackson.TextGrid"

## contact:
Email me for any questions: hyukjekwon@umass.edu
