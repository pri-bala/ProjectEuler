# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np



def calcNextCut(start, angle):
    '''
    This calculates the position of the next cut, which is fundamentally the modulo function with differnet behaviour at the limit
    '''
    nextcut = (start + angle) % 360
    if nextcut == 0:
        return 360
    else:
        return nextcut

def sliceFlip(cake, start, end):
    '''
    This function flips the a slice
    
    start is strictly less than min (s)
    
    '''
    if start== 360:
        start=0
    
    
    #Order the cake slices\
    allkeys = sorted(cake)
    allvalues = [cake[x] for x in allkeys]
    # if start < end, justsort
        #e.g. start = 300, end = 50
        # 40, 50, 60, 70,.... 300, 320, 360,  we want to take 40 and 50 ... and put them at the back
    before_start_keys = [k for k in allkeys if k < start]
    count_before_start = len(before_start_keys)
    before_start_values = allvalues[:count_before_start]

    orderedkeys = allkeys[count_before_start:] + before_start_keys
    orderedvals = allvalues[count_before_start:] + before_start_values
    
    orderedcake = dict(zip(orderedkeys, orderedvals))


    # Extract the slice from the cake
    if start < end:
        cake_slice = {c:orderedcake[c] for c in list(orderedcake.keys()) if (c <= end and c > start)}
        cake_remaining = {c:orderedcake[c] for c in list(orderedcake.keys()) if (c > end or c <= start)}
    else:
        cake_slice = {c:orderedcake[c] for c in list(orderedcake.keys()) if (c <= end or c > start)}
        cake_remaining = {c:orderedcake[c] for c in list(orderedcake.keys()) if (c > end and c <= start)}     
        
    
    # Calculate distances of existing cuts, from start of this slice
    cuts = [start] + list(cake_slice.keys())
    
   
    dists = list(np.diff(cuts))
    its = list(cake_slice.values())
    
    
    
        # Invert order of dists, as the slice is flipped
    dists.reverse()

    # Update cuts values 
    cuts = list(np.cumsum([start] + dists))[1:] #cumsum first returned value is 'start', so omit it
    cuts = [c + 360 if c <= 0 else c for c in cuts]
    # Invert order of icing top list, as the slice is flipped
    its.reverse()
    
    
    # Invert values of icing, as top is now bottom
    its = [not it for it in its]
    
    cake_slice = dict(zip(cuts, its))
    
    cake = cake_remaining
    cake.update(cake_slice)
    return cake #newcake

#t = {10:True, 40:False, 60:True, 180:True, 360:True}
#print(sliceFlip(t, 0, 60))



#print(sliceFlip({310:False,330:False,350:False,360:False,20:False,30:False,80:False}, 310, 20))
#print(sliceFlip({20:False,30:False,80:False,310:False,330:False,350:False,360:False}, 310, 20))

    


def cutCake(cake, last_cut, angle, cakelog):
    
    # Where to cut the cake
    cut = calcNextCut(last_cut, angle)
    
    
    # A cut is on an existing slice. e.g. a cut at 50 degrees, between existing cuts (i.e. a slice of cake) between 45 and 90 degrees.
    # if a cut has already been made here, then we just take that 'iced top' value and invert
    # WE CUT AT POINT C, ON SLICE BETWEEN s0 and s1
    s1 = min([x for x in list(cake.keys()) if x >= cut])
    
    new_slice_it = cake[s1]
    
    #s0 = max([x for x in list(cake.keys()) + [0] if x < cut])
    
    cake[cut] = new_slice_it



    # Print the existing cake, exploding where the cut is
    cakelog.append([cake, last_cut, last_cut])
    cakelog.append([cake, last_cut, cut])
   # Flip    
    cake = sliceFlip(cake, last_cut, cut)
    
    cakelog.append([cake, last_cut, cut])

    return cake, cut, cakelog


cake = {360:True}
a = 10
b = 14
c = 16
angles = [360/a,360/b,360/(np.sqrt(c))]

last_cut = 0

i = 0
cakelog=[]

while (all(cake.values()) == False) or (i < 2) :
    angle = angles[i % 3]
    i += 1

    cake, cut, cakelog = cutCake(cake,last_cut, angle, cakelog)
    last_cut = cut

    if i > 1000:
        print("fucked")
        break
    orderedcuts = sorted(cake)
    orderedit = [cake[x] for x in orderedcuts]
print(i)


print(dict(zip(orderedcuts,orderedit)),angle, cut)
