from typing import List, Callable, Optional
import functools
import copy
import math 
import os

class Process:
    def __init__(self, id, arrival, burst, priority):
        self._id = id
        self._arrival = arrival
        self._burst = burst
        self._priority = priority
        self._waiting = 0
        self._turnaround = 0
        self._currBurst = burst
    
    def id(self):
        return self._id
    
    def arrival(self):
        return self._arrival
    
    def burst(self):
        return self._burst
    
    def priority(self):
        return self._priority
    
    def waiting(self):
        return self._waiting
    
    def turnaround(self):
        return self._turnaround
    
    def currBurst(self):
        return self._currBurst
    
    def addWaiting(self, time):
        self._waiting += time

    def subCurrBurst(self):
        self._currBurst -= 1
    
    def setWaiting(self, waiting):
        self._waiting = waiting
    
    def setTurnaround(self, turnaround):
        self._turnaround = turnaround

    #For table purposes
    def __str__(self):
        return f"{self._id}\t\t{self._arrival}\t\t{self._burst}\t\t{self._priority}\t\t{self._waiting}\t\t{self._turnaround}"

class SchedulingAlgorithms:
    def __init__(self):
        pass
    
    def calculate(self, processes: List[Process], key: Callable):
        newProcess = copy.deepcopy(processes)
        newProcess.sort(key = key)

        currWaiting = 0
        averageWaiting = 0
        averageTurnaround = 0

        for process in newProcess:
            process.addWaiting(currWaiting)

            turnaround = currWaiting + process.burst()
            process.setTurnaround(turnaround)

            averageWaiting += currWaiting
            averageTurnaround += turnaround
            currWaiting += process.burst()
        
        averageWaiting /= len(newProcess)
        averageTurnaround /= len(newProcess)

        finished = copy.deepcopy(newProcess)
        finished.sort(key = lambda x:x.id())

        return Gantt(newProcess, finished, averageWaiting, averageTurnaround)

    def fcfs(self, processes):
        return self.calculate(processes, lambda x:x.id())

    def sjf(self, processes):
        return self.calculate(processes, functools.cmp_to_key(self.sjfCompare))

    def sjfCompare(self, process1: Process, process2:Process):
        #Checks if process1 and process 2 burst time are equal => id
        if process1.currBurst() == process2.currBurst():
            return process1.id() - process2.id()
        
        return process1.currBurst() - process2.currBurst()

    def srpt(self, processes):
        newProcess = copy.deepcopy(processes)
        newProcess.sort(key = functools.cmp_to_key(self.srptCompare))

        sjf: List[Process] = []
        gantt: List[Process] = [copy.deepcopy(newProcess[0])]
        finished: List[Process] = []

        currTime = 0
        currProcess = 0

        while len(sjf) != 0 or len(newProcess) != 0:
            if len(sjf) > 0:
                currProcess = sjf[0]

                if sjf[0].currBurst() == 0:
                    sjf[0].setTurnaround(currTime)
                    finished.append(sjf[0])
                    sjf.pop(0)

            while len(newProcess) > 0 and newProcess[0].arrival() == currTime:
                sjf.append(newProcess.pop(0))
            
            if len(sjf) > 0:
                sjf.sort(key = functools.cmp_to_key(self.sjfCompare))
                #New Process
                if currProcess != None and sjf[0] != currProcess:
                    gantt[-1].setTurnaround(currTime)
                    gantt.append(copy.deepcopy(sjf[0]))
                
                sjf[0].subCurrBurst()
            currTime += 1
        gantt[-1].setTurnaround(currTime - 1)

        averageWaiting = 0
        averageTurnaround = 0

        for process in finished:
            waiting = process.turnaround() - process.burst() - process.arrival()
            process.setWaiting(waiting)
            averageWaiting += waiting
            averageTurnaround += process.turnaround()
        
        finished.sort(key = lambda x:x.id())
        averageWaiting /= len(finished)
        averageTurnaround /= len(finished)

        return Gantt(gantt, finished, averageWaiting, averageTurnaround)

    def srptCompare(self, process1: Process, process2:Process):
        #Checks if process1 and process 2 burst time are equal => arrival time
        if process1.arrival() == process2.arrival():
            return process1.currBurst() - process1.currBurst()
        
        return process1.arrival() - process2.arrival()

    def priority(self, process):
        return self.calculate(process, functools.cmp_to_key(self.prioCompare))

    def prioCompare(self, process1: Process, process2: Process):
        #Checks if process1 and process 2 prio are equal => id
        if process1.priority() == process2.priority():
            return process1.id() - process2.id()
        
        return process1.priority() - process2.priority()
            
    def roundRobin(self, processes):
        newProcess = copy.deepcopy(processes)
        newProcess.sort(key = lambda x:x.id())

        gantt: List[Process] = [copy.deepcopy(newProcess[0])]
        finished: List[Process] = [] 
        currTime = 4
        totalTime = 0

        while len(newProcess):
            if newProcess[0].currBurst() == 0:
                newProcess[0].setTurnaround(totalTime)
                finished.append(newProcess[0])
                newProcess.pop(0)
                currTime = 4

                gantt[-1].setTurnaround(totalTime)

                if len(newProcess) > 0:
                    gantt.append(copy.deepcopy(newProcess[0]))
            
            if currTime == 0:
                newProcess.append(newProcess.pop(0))
                gantt[-1].setTurnaround(totalTime)
                gantt.append(copy.deepcopy(newProcess[0]))
                currTime = 4
            
            if len(newProcess) > 0:
                newProcess[0].subCurrBurst()
            
            currTime -= 1
            totalTime += 1

        averageWaiting = 0
        averageTurnaround = 0

        for process in finished:
            waiting = process.turnaround() - process.burst()
            process.setWaiting(waiting)
            averageWaiting += waiting
            averageTurnaround += process.turnaround()
        
        finished.sort(key = lambda x:x.id())
        averageWaiting /= len(finished)
        averageTurnaround /= len(finished)

        return Gantt(gantt, finished, averageWaiting, averageTurnaround)

class Gantt:
    def __init__(self, ganttProcess: List[Process], processes: List[Process], averageWaiting, averageTurnaround):
        self._processes = processes
        self._ganttProcess = ganttProcess
        self._averageWaiting = averageWaiting
        self._averageTurnaround = averageTurnaround
    
    def printGantt(self):
        maxHeight = max(process.turnaround() - (0 if i == 0 else self._ganttProcess[i - 1].turnaround()) for i, process in enumerate(self._ganttProcess))       #Largest height 
        totalHeight = self._ganttProcess[-1].turnaround()                                                                                                       #Total height of the chart
        divFac = maxHeight / totalHeight * 0.75                                                                                                                 #Scale
        prevHeight = 0

        for index, process in enumerate(self._ganttProcess):
            height = math.floor((process.turnaround() - prevHeight) * divFac)
            processId = f"p {process.id()}"

            #For printing purposes => center
            total = 10 - len(processId)
            first = math.floor(total / 2)
            second = total - first

            if index == 0:
                print(f"┌──────────┬── {prevHeight}")
            else:
                print(f"├──────────┼── {prevHeight}")
            
            for i in range(height):
                print("│          │")
            print("│" + " " * first + processId + " " * second + "│")
            for i in range(height):
                print("│          │")

            if index == len(self._ganttProcess) - 1:
                turnaround = process.turnaround()
                print(f"└──────────┴── {turnaround}")
            prevHeight = process.turnaround()

        #Prints table
        print("\nProcess\t     Arrival\t       Burst\t     Priority\t      Waiting\t   Turnaround\n")
        for process in self._processes:
            print(process)
            
        print(f"Average Waiting Time: {self._averageWaiting} ms")
        print(f"Average Turnaround Time: {self._averageTurnaround} ms")

def parse(file: str):
    processes: List[Process] = []

    with open(file) as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if i == 0:
                continue

            infos = [int(info) for info in line.split()]
            processes.append(Process(infos[0], infos[1], infos[2], infos[3]))
    return processes

def main():
    os.chdir('C:\\Users\\Vlad\\Desktop\\SKOL\\3rd yr\\Codes\\CMSC 125')
    # cwd = os.getcwd()
    # print("Current working directory is:", cwd)

    algo = SchedulingAlgorithms()
    fileId = input("What File to read:\n1. process1.txt\n2. process2.txt\nFile? ")
    
    os.system('cls')
    print("\nP R O G R A M | S I M U L A T I O N  | O F |  S C H E D U L I N G | A L G O R I T H M S \n\n")

    if fileId == "process1.txt":
        file = ["process1.txt"]
        for f in file:
            processes = parse(f)
            print("\n------ FCFS -----")
            algo.fcfs(processes).printGantt()
            print("\n------ SJF -----")
            algo.sjf(processes).printGantt()
            print("\n------ SRPT -----")
            algo.srpt(processes).printGantt()
            print("\n------ PRIORITY -----")
            algo.priority(processes).printGantt()
            print("\n------ ROUND ROBIN -----")  
            algo.roundRobin(processes).printGantt()

    elif fileId == "process2.txt":
        file = ["process2.txt"]
        for f in file:
            processes = parse(f)
            print("\n------ FCFS -----")
            algo.fcfs(processes).printGantt()
            print("\n------ SJF -----")
            algo.sjf(processes).printGantt()
            print("\n------ SRPT -----")
            algo.srpt(processes).printGantt()
            print("\n------ PRIORITY -----")
            algo.priority(processes).printGantt()
            print("\n------ ROUND ROBIN -----")   
            algo.roundRobin(processes).printGantt()

    else:
        print("File not found")

if __name__ == '__main__':
    main()    