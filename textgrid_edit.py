# General tool for tier editing for Praat TextGrids
# Hyuk-Je Kwon: hyukjekwon@umass.edu
# Developed in conjunction with Beat Detective: https://github.com/hyukjekwon/Beat_Detective/blob/patch-2/beat_detective.py
# Last Updated June 2022

# args: file name, flags (-r, -s, -m, -mm, -d)
# -r tier_no interval_no
# -rt tier_no
# -s tier_no_1 tier_no_2
# -m tier_no destination
# -mm front_of_selection back_of_selection destination
# -mi tier_no destination first_interval last_interval
# -d tier_no num_divisions

# check README for usage examples

import sys
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

# for debugging
def print_tiers(tg):
    for t in tg:
        print(t)

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

# move one tier to a specific height
def mov_tier(tg, idx, dest):
    tg_lst = []
    while tg:
        t = tg.pop()
        tg_lst = [t] + tg_lst
    temp = tg_lst[idx]
    tg_lst.remove(temp)
    tg_lst.insert(dest, temp)
    for t in tg_lst:
        tg.append(t)

# move multiple tiers to a specific height
def mov_mult(tg, front, back, dest):
    tg_lst = []
    while tg:
        t = tg.pop()
        tg_lst = [t] + tg_lst
    L = tg_lst[:front]
    M = tg_lst[front:back + 1]
    R = tg_lst[back + 1:]
    tg_lst = L + R
    new_lst = []
    for i, t in enumerate(tg_lst):
        if i == dest:
            for m in M:
                new_lst += [m]
        new_lst += [t]
    for t in new_lst:
        tg.append(t)

# move intervals to specified tier
def mov_intervals(tg, source, target, rg):
    srctier = tg[source]
    tartier = tg[target]
    buf = []
    for i in range(rg[1] - rg[0]):
        buf += [srctier[i + rg[0]]]
    for b in buf:
        collision = tartier.intervalContaining((b.minTime + b.maxTime)/2)
        if collision:
            tartier.removeInterval(collision)
        tartier.addInterval(b)
        srctier.removeInterval(b)

# helper for div_tier
def insert_tier(tg, tier, idx):
    buf = []
    while tg:
        buf.append(tg.pop())
    buf = buf[::-1]
    buf.insert(idx, tier)
    for b in buf:
        tg.append(b)

# removes a given tier
def remove_tier(tg, tier_no):
    buf = []
    while tg:
        buf.append(tg.pop())
    buf = buf[::-1]
    del buf[tier_no]
    for b in buf:
        tg.append(b)

# add new tier of divided tier
def div_tier(tg, tier_no, num_div):
    def mega(num):
        return int(num * 100000)
    tier = tg[tier_no][1:]
    newtier = textgrid.IntervalTier(str(tier_no + 1))
    buf = []
    for itvl in tier:
        minTime = int(mega(itvl.minTime))
        maxTime = int(mega(itvl.maxTime))
        itvl_len = int((maxTime - minTime) / num_div)
        for i in range(num_div):
            buf.append(minTime + (i * itvl_len))
    for i, b in list(enumerate(buf))[:-1]:
        minTime = b / 100000
        maxTime = buf[i + 1] / 100000
        new_itvl = textgrid.Interval(minTime, maxTime, "")
        newtier.addInterval(new_itvl)
    insert_tier(tg, newtier, tier_no + 1)

if __name__ == '__main__':
    tg_name = sys.argv[1]
    if tg_name == '-help':
        s = 'python3 textgrid_edit.py filename'
        print(s + ' -r tier_# interval_#:\n        remove a single interval from a tier\n')
        print(s + ' -rt tier_#:\n        remove an entire tier from the textgrid\n')
        print(s + ' -d tier_# divisor:\n        divide each interval in a tier by the divisor\n')
        print(s + ' -s tier_1 tier_2:\n        swap the position of two tiers\n')
        print(s + ' -m tier_# destination:\n        move the position of a given tier\n')
        print(s + ' -mm top_tier bottom_tier destination:\n        move multiple tiers\n')
        print(s + ' -mi src_tier des_tier itvl1 itvl2:\n        move intervals from one tier to another\n')
    if len(sys.argv) > 2:
        flag = sys.argv[2]
        if flag == '-r':
            tier = int(sys.argv[3]) # get tier number
            interval = int(sys.argv[4]) # get interval number
            remove_interval(tg_name, tier, interval)
        else:
            tg = textgrid.TextGrid.fromFile(tg_name)
            if flag == '-rt': # remove a given tier
                tier = int(sys.argv[3]) - 1 # get tier number
                remove_tier(tg, tier)
            elif flag == '-d': # division
                tier = int(sys.argv[3]) - 1 # get tier number
                num_div = int(sys.argv[4]) # get number of divisions
                div_tier(tg, tier, num_div) # run division and add new tier
            elif flag == '-s': # swap
                num1 = int(sys.argv[3]) - 1
                num2 = int(sys.argv[4]) - 1
                swap_tier(tg, num1, num2)
            elif flag == '-m': # move single tier
                idx = int(sys.argv[3]) - 1
                dest = int(sys.argv[4]) - 1
                mov_tier(tg, idx, dest)
            elif flag == '-mm': # move multiple tiers
                front = int(sys.argv[3]) - 1
                back = int(sys.argv[4]) - 1
                dest = int(sys.argv[5]) - 1
                mov_mult(tg, front, back, dest)
            elif flag == '-mi': # move intervals
                srctier = int(sys.argv[3]) - 1
                destier = int(sys.argv[4]) - 1
                itvl1 = int(sys.argv[5]) - 1
                itvl2 = int(sys.argv[5]) - 1
                mov_intervals(tg, srctier, destier, (itvl1, itvl2))
            
            # write state to a new TextGrid file
            tg.write('new_' + tg_name)