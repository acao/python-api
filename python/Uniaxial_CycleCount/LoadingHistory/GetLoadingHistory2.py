# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 10:50:27 2015

@author: egassama
"""
import numpy  

def Reorder(Time,Stress,Strain):
#
#   Assuming the loading (stress or strain) data is periodic in time, find the point 
#   of maximum loading magnitude and then shift (rotate) this periodic data so that 
#   this maximum value always occurs at the first position in the array (amounts to a 
#   shift in the phase angle of the period).
#
    MaxIndex  = numpy.argmax(abs(Strain)) 
    
    if MaxIndex > 0:
        #
        # Loading array needs to be shifted according to type and MaxIndex
        #
        if Stress[0]==0.0 and Time[0]==0.0:
            StressBeforeMax     = Stress[1:MaxIndex+1]
            StrainBeforeMax     = Strain[1:MaxIndex+1]
            TimeBeforeMax       = Time[1:MaxIndex+1]
            
        elif Stress[0]!=0.0 and Time[0] == 0.0:
            Time                = Time+1.
            StressBeforeMax     = Stress[:MaxIndex+1]
            StrainBeforeMax     = Strain[:MaxIndex+1]
            TimeBeforeMax       = Time[:MaxIndex+1]
            
        elif Stress[0]==0.0 and Time[0] != 0.0:
            Time                = numpy.delete(Time,0)
            Time                = numpy.insert(Time,0,0)
            StressBeforeMax     = Stress[1:MaxIndex+1]
            StrainBeforeMax     = Strain[1:MaxIndex+1]
            TimeBeforeMax       = Time[1:MaxIndex+1]
    
        else:
            StressBeforeMax     = Stress[:MaxIndex+1]
            StrainBeforeMax     = Strain[:MaxIndex+1]
            TimeBeforeMax       = Time[:MaxIndex+1]
            
        StressAfterMax      = Stress[MaxIndex:] 
        StrainAfterMax      = Strain[MaxIndex:] 
        TimeAfterMax        = Time[MaxIndex:]
        
        ReorderedStress     = numpy.concatenate([StressAfterMax,StressBeforeMax])
        ReorderedStrain     = numpy.concatenate([StrainAfterMax,StrainBeforeMax])
        ReorderedTime       = numpy.concatenate([TimeAfterMax,TimeBeforeMax])
        
    else:
#
#       Loading array is already ordered correctly
#    
        ReorderedStress     = Stress
        ReorderedStrain     = Strain
        ReorderedTime       = Time
    #
    return ReorderedTime,ReorderedStress,ReorderedStrain

def Filter(Time,Stress,Strain):
#
#   Filter the original loading (stress/strain) history to remove any intermediate 
#   points that do not correspond to peaks or valleys. The output loading array will
#   contain only peak and valley points. The first and last points are always retained.
#
    FilteredTime        =[Time[0]]
    FilteredStress      =[Stress[0]]
    FilteredStrain      =[Strain[0]]
    Index=1
    while Index < len(Stress)-1 and len(Stress) > 2:
        if IsPeakOrValley(Stress[Index-1:Index+2]):
            FilteredTime.append(Time[Index])
            FilteredStress.append(Stress[Index])
            FilteredStrain.append(Strain[Index])
        Index=Index+1
    FilteredTime.append(Time[-1])
    FilteredStress.append(Stress[-1])
    FilteredStrain.append(Strain[-1])
    FilteredTime = numpy.array(FilteredTime)
    FilteredStress = numpy.array(FilteredStress)
    FilteredStrain = numpy.array(FilteredStrain)

    return FilteredTime,FilteredStress,FilteredStrain 

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

def NotOrdered(Stress):
    #
    #   Determines if the stress array is already ordered properly or not
    #
    MaxStressIndex = numpy.argmax(abs(Stress)) 
    #
    return MaxStressIndex > 0
  
def WhichInputFile(DataIdentifier,ReorderIdentifier):
    #
    DataSet = DataIdentifier
    try:
        if DataSet == 'LeePart_14_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeePart_14_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeePart_14_Al_Ti_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeePart_14_Al_Ti_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeBannantine_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeeBannantine_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1137_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeeSAE_1137_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1045_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeeSAE_1045_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1010_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeeSAE_1010_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1005_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeeSAE_1005_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSS316_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\LeeSS316_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150Part_14_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150Part_14_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150Part_14_Al_Ti_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150Part_14_Al_Ti_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150Bannantine_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150Bannantine_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1137_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150SAE_1137_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1045_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150SAE_1045_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1005_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150SAE_1005_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1010_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150SAE_1010_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SS316_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('LoadingHistory\AbaqusNotch150SS316_LoadingHistory.txt',unpack=True)
    except:
        if DataSet == 'LeePart_14_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeePart_14_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeePart_14_Al_Ti_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeePart_14_Al_Ti_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeBannantine_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeeBannantine_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1137_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeeSAE_1137_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1045_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeeSAE_1045_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1010_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeeSAE_1010_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSAE_1005_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeeSAE_1005_LoadingHistory.txt',unpack=True)
        elif DataSet == 'LeeSS316_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\LeeSS316_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150Part_14_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150Part_14_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150Part_14_Al_Ti_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150Part_14_Al_Ti_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150Bannantine_Fe_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150Bannantine_Fe_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1137_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150SAE_1137_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1045_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150SAE_1045_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1005_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150SAE_1005_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SAE_1010_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150SAE_1010_LoadingHistory.txt',unpack=True)
        elif DataSet == 'AbaqusNotch150SS316_LoadingHistory':
            OriginalTime,OriginalStress,OriginalStrain  = numpy.loadtxt('Source_CycleCount\LoadingHistory\AbaqusNotch150SS316_LoadingHistory.txt',unpack=True)
    #        
    # Are we Reordering and Filtering the data or just filtering it or neither
    #    
    if ReorderIdentifier == 'Both':  
        FilteredTime,FilteredStress,FilteredStrain      = Filter(OriginalTime,OriginalStress,OriginalStrain)  # correct and general
        Time,Stress,Strain                              = Reorder(FilteredTime,FilteredStress,FilteredStrain)
    elif ReorderIdentifier == 'FilterOnly':
        Time,Stress,Strain                              = Filter(OriginalTime,OriginalStress,OriginalStrain) # Correct and general
    else:
        Time                                            = OriginalTime
        Stress                                          = OriginalStress
        Strain                                          = OriginalStrain
    #    
    return Time,Stress,Strain
    
def WhichInputFile2(OriginalTime,OriginalStress,OriginalStrain,ReorderIdentifier):
    #        
    # Are we Reordering and Filtering the data or just filtering it or neither
    #    
    if ReorderIdentifier == 'Both':  
        FilteredTime,FilteredStress,FilteredStrain      = Filter(OriginalTime,OriginalStress,OriginalStrain)  # correct and general
        Time,Stress,Strain                              = Reorder(FilteredTime,FilteredStress,FilteredStrain)
    elif ReorderIdentifier == 'FilterOnly':
        Time,Stress,Strain                              = Filter(OriginalTime,OriginalStress,OriginalStrain) # Correct and general
    else:
        Time                                            = OriginalTime
        Stress                                          = OriginalStress
        Strain                                          = OriginalStrain
    #    
    return Time,Stress,Strain