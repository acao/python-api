# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12th

@author: acao

"""
from Uniaxial import GetUniaxialCycles
import json
import sys
import string

ParsedData = json.loads(sys.argv[1]);

StartTimes,EndTimes,ReorderedStartTimes,ReorderedEndTimes,Ranges,MaxStresses,MeanStresses,ReorderedTime,ReorderedStress,ReorderedStrain = GetUniaxialCycles(ParsedData[0],ParsedData[1],ParsedData[2])

result = []
for i in range(len(StartTimes)):
    result.append([str(StartTimes[i]) + " to " + str(EndTimes[i]), Ranges[i], MaxStresses[i], MeanStresses[i]])

print(json.dumps(result));
