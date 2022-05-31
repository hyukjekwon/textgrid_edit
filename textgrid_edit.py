# General tool for tier editing for Praat TextGrids
# Hyuk-Je Kwon: hyukjekwon@umass.edu
# Developed in conjunction with Beat Detective: https://github.com/hyukjekwon/Beat_Detective/blob/patch-2/beat_detective.py
# Last Updated June 2022

# args: file name, flags (-r, -s, -d)
# -r tier_no interval_no
# -s tier_no_1 tier_no_2
# -d tier_no num_divisions

import sys
import math
import textgrid #http://github.com/kylebgorman/textgrid/

# edits file to remove selected interval from selected tier
# doesn't use python textgrid library
# use to remove duplicate intervals that cause textgrids to be unusable
def remove_interval(f_name, tier, interval):
    contents = []
    reading = False
    indices = []
    with open(f_name, 'r') as file:
        for i, row in enumerate(file):
            if row ==  '    item [{}]:\n'.format(tier):
                reading = True
                indices.append(i)
            elif row == '    item [{}]:\n'.format(tier + 1):
                indices.append(i)
                break
            if reading:
                contents.append(row)
    index = contents.index('        intervals [{}]:\n'.format(interval))

    for i in range(0, 4):
        del contents[index]
    
    size = int(contents[5].split('=')[1]) - 1
    contents[5] = '        intervals: size = {}\n'.format(size)

    for i in range(index, len(contents), 4):
        contents[i] = contents[i][:19] + str(int(interval + (i - index)/4)) + ']:\n'

    with open('new_' + f_name, 'w') as file:
        with open(f_name, 'r') as file2:
            for i, row in enumerate(file2):
                if i in list(range(indices[0], indices[1]-4)):
                    file.write(contents[i-indices[0]])
                elif i not in list(range(indices[0], indices[1])):
                    file.write(row)

# swap two tiers in textgrid
def swap_tier(tg, num1, num2):
    tg_lst = []
    while tg:
        t = tg.pop()
        tg_lst = [t] + tg_lst
    temp = tg_lst[num1]
    tg_lst[num1] = tg_lst[num2]
    tg_lst[num2] = temp
    for t in tg_lst:
        tg.append(t)

# add new tier of divided tier
def div_tier(tg, tier, num_div):
    # calculate what kind of intervals are being divided
    # i.e. 8 if tier 4 is selected, 16 if tier 5 is selected
    itvl_type = int(math.pow(2, tier))

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
    new_tier = textgrid.IntervalTier(name=tier_name)

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
    temp = []
    while tg:
        t = tg.pop()
        temp = [t] + temp
    for i, t in enumerate(temp):
        tg.append(t)
        if i == tier:
            tg.append(new_tier)
    print('The ' + tier_name + ' tier has been added.')

if __name__ == '__main__':
    tg_name = sys.argv[1]
    flag = sys.argv[2]
    if flag == '-r':
        tier = int(sys.argv[3]) # get tier number
        interval = int(sys.argv[4]) # get interval number
        remove_interval(tg_name, tier, interval)
    else:
        tg = textgrid.TextGrid.fromFile(tg_name)

        if flag == '-d': # division
            tier = int(sys.argv[3]) - 1 # get tier number
            num_div = int(sys.argv[4]) # get number of divisions
            div_tier(tg, tier, num_div) # run division and add new tier
        elif flag == '-s': # swap
            num1 = int(sys.argv[3])
            num2 = int(sys.argv[4])
            swap_tier(tg, num1, num2)

        # # write state to a new TextGrid file
        tg.write('new_' + tg_name)