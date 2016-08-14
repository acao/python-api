# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 08:09:25 2015

@author: astenta
"""
from Algorithms import RainFlow_3pt_New
from LoadingHistory import GetLoadingHistory2
import numpy

#
# This is the main file in which we choose which model to run and which input
#

def GetUniaxialCycles(OriginalTime,OriginalStress,OriginalStrain):
    #
    ReorderIdentifier                               = 'Both'
    ReorderedTime,ReorderedStress,ReorderedStrain   = GetLoadingHistory2.WhichInputFile2(OriginalTime,OriginalStress,OriginalStrain,ReorderIdentifier)
    #
    # This cycle count uses the reordered time indices for the original loading
    #
    Cycles,StartTimes,EndTimes,Ranges               = RainFlow_3pt_New.Rainflow(ReorderedStrain,ReorderedTime)
    Cycles                          		        = numpy.array(Cycles)
    #
    # This cycle count uses a new set of time indices that are reinitialized at 0
    #
    TimeIndices                                 = numpy.arange(0.0,float(len(ReorderedStrain)))
    Cycles2,ReorderedStartTimes,ReorderedEndTimes,Ranges2   = RainFlow_3pt_New.Rainflow(ReorderedStrain,TimeIndices)
    Cycles2                                     = numpy.array(Cycles2)
    #
    # Calculate the max and mean stress for the cycles 
    # 
    Length = len(Cycles)
    Cycles2 = numpy.array(Cycles2)
    RangeIndex = 0
    MaxStresses = []
    MeanStresses = []
    while RangeIndex <= Length-1:
        StartIndex = Cycles2[RangeIndex,0]
        EndIndex = Cycles2[RangeIndex,1]
        MaxStress = max(ReorderedStress[StartIndex:EndIndex+1])
        MinStress = min(ReorderedStress[StartIndex:EndIndex+1])
        MeanStress = (MaxStress+MinStress)/2
        MaxStresses.append(MaxStress)
        MeanStresses.append(MeanStress)
        RangeIndex = RangeIndex + 1
    #
    return StartTimes,EndTimes,ReorderedStartTimes,ReorderedEndTimes,Ranges,MaxStresses,MeanStresses,TimeIndices,ReorderedStress,ReorderedStrain

if __name__ == "__main__": 
    #
    # Available = ('Lee', 'Downing', 'Draper', 'Sandia', 'ActualStrain', 'Plasticity')
    #
    Data                            = 'LeeSAE_1005_LoadingHistory'
    Time,Stress,Strain              = GetLoadingHistory2.WhichInputFile(Data,'None')
    #
    # Call the uniaxial cycle counting and damage algorithm
    #
    StartTimes,EndTimes,ReorderedStartTimes,ReorderedEndTimes,Ranges,MaxStresses,MeanStresses,ReorderedTime,ReorderedStress,ReorderedStrain = GetUniaxialCycles(Time,Stress,Strain)
    #
    # Print the results that are appended to a file.
    #
    for i in range(len(StartTimes)):
        print 'Cycle',i,'from original t =',StartTimes[i],'to t =',EndTimes[i],'or reordered t =',ReorderedStartTimes[i],'to t =',ReorderedEndTimes[i],'with Strain Range =',Ranges[i],'Max Stress =',MaxStresses[i],'and Mean Stress =',MeanStresses[i]