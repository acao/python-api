# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 10:50:27 2015

@author: egassama
"""
import numpy  

# the input data for the 3 pt rainflow must be periodic
def LoadingRanges(Index,Loading):
    #
    CurrentLoadingRange  = abs(Loading[Index]   - Loading[Index-1]) # range X
    PreviousLoadingRange = abs(Loading[Index-1] - Loading[Index-2]) # range Y
    #
    return PreviousLoadingRange,CurrentLoadingRange

def Rainflow(Loading,Time):
    #
    #   Input:
    #     Loading[] - Input stress or strain array. Loading data must already be filtered so 
    #                 that only the peak and valley points are retained (intermediate points
    #                 are discarded), and the data must also be shifted such that the maximum
    #                 loading magnitude corresponds to the first position in the array. 
    #   Output:
    #     Cycles[]  - Array of cycles (closed stress-strain hysteresis loops) that were found
    #                 from the input loading history data. Each cycle contains the starting and
    #                 ending indices of the cycle, the loading range and the mean loading.
    #       
    NumberPoints  = len(Loading) 
    Cycles        = [] # Initialize list of cycles to empty array
    t0            = []
    t1            = []
    Ranges        = []
    Index         = 2 
#    print '\n t0  t1    Load0     Load1     Range      Mean'
    while NumberPoints > 2:
        CycleIndices = []  # Initialize cycle indices to an empty array
        PreviousLoadingRange,CurrentLoadingRange = LoadingRanges(Index,Loading)
        if CurrentLoadingRange < PreviousLoadingRange:
            Index = Index + 1
        else: 
#            Plot(Time,Loading)
            Mean  = (Loading[Index-1] + Loading[Index-2])/2.0
            Cycles.append([Time[Index-2],Time[Index-1],Loading[Index-2], Loading[Index-1], \
                           PreviousLoadingRange, Mean])
#            print '{:3d} {:3d} {:9.5f} {:9.5f} {:9.5f} {:9.5f}'.format(Time[Index-2], \
#                   Time[Index-1],Loading[Index-2],Loading[Index-1],PreviousLoadingRange,Mean)
            t0.append(Time[Index-2])
            t1.append(Time[Index-1])
            Ranges.append(round(PreviousLoadingRange,8))
            CycleIndices.append(Index-2)
            CycleIndices.append(Index-1)
            #   Remove any closed loop cycles that were found from the loading 
            #   array and start over with reduced array.  
            Loading       = numpy.delete(Loading,CycleIndices,None)
            Time          = numpy.delete(Time,CycleIndices,None)
            NumberPoints  = len(Loading)
            Index = 2
    t0 = numpy.array(t0)
    t1 = numpy.array(t1)
    Ranges = numpy.array(Ranges)
    #
    return Cycles,t0,t1,Ranges
    
def IsPeakOrValley(Loading):
#
#   Determine whether the middle point in the input array of three successive loading 
#   points corresponds to a peak or valley (a reversal). Returns True if a peak or valley, 
#   otherwise, returns False.
#   
    ForwardDifference=Loading[2]-Loading[1] 
    PreviousDifference=Loading[1]-Loading[0]
    if ForwardDifference*PreviousDifference <0 or \
       ForwardDifference == 0.0 and PreviousDifference != 0.0 or \
       ForwardDifference != 0.0 and PreviousDifference == 0.0:
          return True
    else:
        return False
#
#   Determines if the stress array is already ordered properly or not
#
def NotOrdered(Stress):
    #
    MaxStressIndex = numpy.argmax(abs(Stress)) 
    #
    return MaxStressIndex > 0
