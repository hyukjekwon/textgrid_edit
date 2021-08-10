# Divides a given tier into a given amount of divisions
# Hyuk-Je Kwon: hyukjekwon@umass.edu
# Developed in conjunction with Beat Detective: https://github.com/hyukjekwon/Beat_Detective/blob/patch-2/beat_detective.py
# August 2021

# args: file name, tier selected for division, number of divisions

import sys
import math
import textgrid #http://github.com/kylebgorman/textgrid/

# get file name of textgrid
tg_name = sys.argv[1]

# create TextGrid state based on file name
tg = textgrid.TextGrid.fromFile(tg_name)

# get tier
tier = int(sys.argv[2]) - 1

# calculate what kind of intervals are being divided
# i.e. 8 if tier 4 is selected, 16 if tier 5 is selected
itvl_type = int(math.pow(2, tier))

# get number of divisions
num_div = int(sys.argv[3])

# TextGrid duration
tg_len = tg[tier][len(tg[tier]) - 1].maxTime

# create new tier name
if num_div % 2 == 0:
    tier_name = str(num_div * itvl_type) + 'ths'
elif num_div == 3:
    tier_name = str(itvl_type) + 'th triplets'
else:
    tier_name = 'new'

# create new tier for annotation
new_tier = textgrid.IntervalTier(name = tier_name)

# get first downbeat in megaseconds
first_downbeat = int(tg[tier][0].maxTime * 100000)

# get duration between primary intervals in given tier
itvl_dur = tg[tier][1].maxTime - tg[tier][0].maxTime

# get duration between secondary intervals in new tier
new_itvl_dur = itvl_dur / num_div

# get variables in megaseconds for the for loop
tg_len_Ms = int(tg_len * 100000)
itvl_dur_Ms = int(itvl_dur * 100000)

# iterate from the first downbeat to the end of the TextGrid, step: primary interval length
for i in range(first_downbeat, tg_len_Ms, itvl_dur_Ms):
    i_s = float(i / 100000) # get current onset of primary interval in seconds
    for j in range(num_div - 1): # iterate based on the given number of divisions
        new_tier.addInterval(textgrid.Interval(i_s + (new_itvl_dur * j), i_s + (new_itvl_dur * (j + 1)), ''))

# add new tier to TextGrid state
tg.append(new_tier)
print('The ' + tier_name + ' tier has been added.')

# write state to a new TextGrid file
tg.write('new_' + tg_name)
