# Assignment 3

# Table of Contents
# 1) Imported modules
# 2) Main

# 1) Imported modules
# -------------------

import sys
import math
import random
import statistics
import numpy as np
from matplotlib import pyplot as plt

# 1.2) Sides functions

def frange(start, stop, step):
         i = start
         while i < stop:
             yield i
             i += step

# 2) Main
# -------

seed = 92732
mu = 40
sigma = 2
lowerBound = 2
upperBound = 4
speed = 50.0
d1 = 300.0
d2 = 250.0
d3 = 180.0
numberOfRuns = 1000

# 3) Parts
# --------

class Part:
    def __init__(self,t0):
        self.t0=t0   #start of the process
        self.t1=0   #reach machine1
        self.t2=0   #end of process machine 1
        self.t3=0   #reach machine2
        self.t4=0   #end of process machine 2
        self.t5=0   #reach outline

    def drawSchedule(self):
        #introduction time
        # time to reach machine 1
        self.t1 = d1/speed+self.t0
        # machine 1
        z11 = random.normalvariate(mu, sigma)
        z12 = random.uniform(lowerBound, upperBound)
        z1 = z11 + z12
        self.t2 = self.t1 + z1
        # time to reach machine 2
        self.t3 = self.t2 + d2/speed
        # machine 2
        z21 = random.normalvariate(mu, sigma)
        z22 = random.uniform(lowerBound, upperBound)
        z2 = z21 + z22
        self.t4 = self.t3 + z2
        # time to get out the line
        self.t5 = self.t4 + d3/speed
        # for statistics
        #L.append(t5)
        #s += t5
        #s2 += t5*t5

    def printPart(self):
        print("t0="+str(self.t0)+" t1="+str(self.t1)+" t2="+str(self.t2)+" t3="+str(self.t3)+" t4="+str(self.t4)+" t5="+str(self.t5))

class Machine:
    def __init__(self,machineN):
        self.machineN=machineN  #machine number
        self.table=[]           #table of use of machine

    def addToTable(self,part):
        if self.machineN==1:
            self.table.append([part.t1,part.t2])
        if self.machineN==2:
            self.table.append([part.t3,part.t4])    

    def useTime(self):
        sum=0
        for t in self.table:
            t1=t[0]
            t2=t[1]
            use=t2-t1
            sum=sum+use
        return sum

class System:
    def __init__(self):
        self.machines=[]
        self.parts=[]
        self.tOP=0              #time of process


    def partInConflict(self):
        state=0
        for i in range(len(self.parts)):
            for j in range(len(self.parts)):
                if i!=j:
                    if (self.parts[j].t1<self.parts[i].t1<self.parts[j].t2 or self.parts[j].t3<self.parts[i].t3<self.parts[j].t4):
                        state=1
        return state

    def addMachine(self,machine):
        self.machines.append(machine)

    def addPart(self,part):
        self.parts.append(part)

    def generateParts(self,nbOfParts,dT):
        t=0
        for i in range(nbOfParts):
            self.addPart(Part(t))    
            t=t+dT

    def dispParts(self):
        for i in range(len(self.parts)):
            print("Part n°"+str(i)+":")
            print (self.parts[i].printPart())




    def drawAllSchedule(self):
        for i in range(len(self.parts)):
            self.parts[i].drawSchedule()
            self.machines[0].addToTable(self.parts[i])
            self.machines[1].addToTable(self.parts[i])

    def machineUseTimes(self):
        useTimes=[]
        for i in range(len(self.machines)):
            useTimes.append(self.machines[i].useTime()/self.parts[-1].t5)
        return useTimes





random.seed(seed)
timeOfRun=14400 #s
abscisse=[]
ordonnee1=[]
ordonnee2=[]
ordonnee3=[]
ordonnee4=[]

for dT in frange(50, 60,0.25):    
    numOfParts=int(round(timeOfRun/dT))

    s = 0
    s2 = 0
    L = []
    numberOfRuns=500

    #creating parts

    lesT5=[]
    conflicts=[]
    useTimes=[]
    for i in range(numberOfRuns):
        machineA=Machine(1)
        machineB=Machine(2)
        controller=System()
        controller.addMachine(machineA)
        controller.addMachine(machineB)
        controller.generateParts(numOfParts,dT)
        controller.drawAllSchedule()
        #print(len(controller.parts))
        #print("Etat du conflit : "+str(controller.partInConflict()))
        conflicts.append(controller.partInConflict())
        for part in controller.parts:
            lesT5.append(part.t5-part.t0)
        #print (lesT5)
        
        # for i in range(len(controller.machines)):
        #     print("La machine n°"+str(i)+" a un useTime de "+str(controller.machineUseTimes()[i]))

        useTimes.append(controller.machineUseTimes())

    for i in range(len(controller.machines)):
             print("La machine n°"+str(i)+" a un useTime moyen de "+str(np.mean(useTimes,axis=0)[i]))
    print("Le taux de conflit est de "+str(np.mean(conflicts)*100)+"%")

    print("Une part met en moyenne "+str(np.mean(lesT5))+"s à être produite, avec un écart type de "+str(np.std(lesT5)))

    abscisse.append(dT)
    ordonnee1.append(np.mean(conflicts)*100)
    ordonnee2.append(np.mean(lesT5))
    ordonnee3.append(np.mean(useTimes,axis=0)[0])
    ordonnee4.append(np.mean(useTimes,axis=0)[1])

plt.figure(1, figsize=(9, 15))

plt.title('A tale of 2 subplots')

plt.subplot(411)
plt.plot(abscisse, ordonnee1)
plt.ylabel('Conflict rate (%)')

plt.subplot(412)
plt.scatter(abscisse, ordonnee2)
plt.ylabel('Mean time for a part (s)')

plt.subplot(413)
plt.plot(abscisse, ordonnee3)
plt.ylabel('UseTime machine A')

plt.subplot(414)
plt.plot(abscisse, ordonnee4)
plt.ylabel('Use time Machine B')


plt.xlabel('Time space between every part')

plt.show()

# part1=Part(0)
# part2=Part(1)

# part1.printPart()
# part2.printPart()
# controller=System()
# controller.addPart(part1)


#process
# for run in range(0, numberOfRuns):
#     # time to reach machine 1

#     L.append(t5)
#     s += t5
#     s2 += t5*t5
# mean = s/numberOfRuns
# m2 = s2/numberOfRuns
# variance = m2 - mean*mean
# standardDeviation = math.sqrt(variance)
# print("mean\t" + str(mean))
# print("standardDeviation\t" + str(standardDeviation))

# print("With statistics module")
# print("mean\t" + str(statistics.mean(L)))
# print("standardDeviation\t" + str(statistics.stdev(L)))

# controller.dispParts()
# print(len(controller.parts))

# print("Etat du conflit : "+str(controller.partInConflict()))