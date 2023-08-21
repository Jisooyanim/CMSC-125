# 1. Generate a random number of resources (1-30). Label them by resource number, between 1-30. 
# 2. Generate a random number of users (1-30). Label them by user number between, 1-30.
# 3. Generate the random resource that a user will need and the length of the time that the user will 
#    use the resource (1-30 seconds). The resource(s) that a user will request must only be those 
#    randomly generated resources (from #1).
# 4. The program should be able to display the status of the resources, including the user currently 
#    using the resource, the time (or time left) that the user needs to use the resource.
# 5. The program should also be able to list the users “in waiting” of a resource, if there are any, 
#    and when these users will be able to start using the resource.
# 6. Finally, the program should be able to say when the resources will be free of users (meaning, 
#    no user needs to use the resource). 

# Additional specs:
# - A user can only request for a specific resource once. User cannot request for a resource multiple 
# times.
# - User request is to be sorted according to priority (by order number, in increasing order)

from typing import Optional, List
import random
import math
import termcolor 
import time
import os

#For resources, user, and time
RANDOM_NUMBER = 3                   #Testing Purposes
# RANDOM_NUMBER = 30
MAX_CHAR_WIDTH = 24                 #For terminal characters


class Process:
    def __init__(self, user, resource, currTime: Optional[int] = None):
        self._user = user
        self._resource = resource
        self._currTime = random.randint(1, RANDOM_NUMBER) if currTime is None else currTime
        self._initTime = self._currTime
        self._startTime = 0
        self._endTime = self._currTime
        self._isProcessing = False
        self._isDone = False
    
    #Getter Functions
    def user(self):
        return self._user
    
    def resource(self):
        return self._resource
    
    def currTime(self):
        return self._currTime
    
    def startTime(self):
        return self._startTime
    
    def endTime(self):
        return self._endTime

    def isProcessing(self):
        return self._isProcessing
    
    def isDone(self):
        return self._isDone
    
    #Helper Functions
    #Records the time when the process of a resource would start and end
    def processTime(self, time: int):
        self._startTime += time
        self._endTime += time

    #Updates the time
    def passTime(self):
        if self._isDone:
            return
        
        if not self._isProcessing:
            if self._startTime == 0:
                self._isProcessing = True
            self._startTime -= 1
            
        else:
            if self._currTime == 0:
                self._isProcessing = False
                self._isDone = True
            self._currTime -= 1
    
    def printIsProcessing(self):
        if self._currTime == 0:
            return "|== D O N E ==|"
        elif self._isProcessing:
             return "|== P R O C E S S I N G ==|"
            # termcolor.cprint("|==  P R O C E S S I N G == |", "red")
        else:
            return ""
    
    def printStartTime(self):
        return f"Time to Start: {self._startTime + 1}" if not self._isProcessing else ""
    
    #Progress bar
    def printCurrTime(self):
        dec: float
        integer: float
        # print(f"Init: {self._initTime}\nCurr: {self._currTime}")
        (dec, integer) = math.modf((self._initTime - self._currTime) / self._initTime * MAX_CHAR_WIDTH)                         #Completeness percentage of the progress bar
        # print(f"Decimal: {dec}\nInteger: {integer}")
        return ("█" * int(integer) + "░" * (MAX_CHAR_WIDTH - int(integer)) + "\n" + str(self._initTime - self._currTime) + "/" + str(self._initTime) + "\n" if self._isProcessing else "░" * MAX_CHAR_WIDTH + "\n")
    
    def __str__(self):
        return f"{self.printIsProcessing()} \nUser: {self._user} \n\n{self.printCurrTime()} {self.printStartTime()} \n"
    
Resource = List[Process]
Processes = List[Resource]


class OperatingSystem:
    def __init__(self):
        self._users = self.removeDuplicates([random.randint(1, RANDOM_NUMBER) for i in range(0, random.randint(1, RANDOM_NUMBER))])
        self._resources = self.removeDuplicates([random.randint(1, RANDOM_NUMBER) for i in range(0, random.randint(1, RANDOM_NUMBER))])
        self._numberOfUsers = len(self._users)
        self._numberOfResources = len(self._resources)
        self._users.sort()
        self._resources.sort()
        self._processes = [[None for i in range(self._users[-1] + 1)] for i in range(self._resources[-1] + 1)]

        self.allocateResources()
        self.cleanProcess()
        self.calculateTime()

    def removeDuplicates(self, items):
        return list(dict.fromkeys(items))
    
    #Create process for each resource
    def allocateResources(self):
        for resource in self._resources:                                                                                           #Create requests for each resource
            requests = random.randint(1, self._numberOfUsers)
            users = self._users.copy()
        
            for r in range(requests):                                                                                              #Select available users for the current resource and creates a new process
                user = users[random.randrange(0, len(users))]
                self._processes[resource][user] = Process(user, resource)
                users.remove(user)

    #Removes any unused resources
    def cleanProcess(self):
        for i, resource in enumerate(self._processes):
            if i not in self._resources:
                self._processes[i] = None

    #Calculate the time for each request
    def calculateTime(self):
        for user in self._users:
            userRequests: List[Process] = []
            for resource in self._processes:
                if resource is None:
                    continue

                if resource[user] is not None:
                    self.timeResource(resource, user)
                    userRequests.append(resource[user])
            self.checkOverlap(userRequests)

    #Waiting time
    def timeResource(self, resource: Resource, user: int):
        for i in range(user -1, 0, -1):
            process = resource[i]

            if process is None:
                continue

            else:
                resource[user].processTime(process.endTime() - resource[user].startTime())
                break
    
    #Check any concurrent processes
    def checkOverlap(self, processes: List[Process]):
        processes.sort(key = lambda x:x.startTime())

        for outIdx in range(len(processes)):
            outProcess = processes[outIdx]
            for inIdx in range(outIdx + 1, len(processes)):
                inProcess = processes[inIdx]

                if (outProcess.endTime() > inProcess.startTime() and inProcess.endTime() > outProcess.startTime()):
                    inProcess.processTime(outProcess.endTime() - inProcess.startTime())
    
    def program(self):
        seconds = -1
        newProcess: Processes = [[process for process in resource if process is not None] if resource is not None else None for resource in self._processes]

        os.system('cls')
        print("P R O G R A M | S I M U L A T I O N  | O F |  T I M E S H A R I N G | O . S . \n\n")
        while True:
            print("Users: ", end = "")
            termcolor.cprint(self._users, attrs=["bold"])
            print("Resources: ", end="")
            termcolor.cprint(self._resources, attrs=["bold"])
            termcolor.cprint("\n====== ", "magenta", end="")
            print("TIME: " + str(seconds) + "s", end="")
            termcolor.cprint(" ======\n", "magenta")
            self.printProcess(newProcess)

            for resources in newProcess:
                if resources is None:
                    continue
                
                for process in resources:
                    if process is not None:
                        process.passTime()
            
            newProcess[:] = [[process for process in resource if process is None or not process.isDone()] if resource is not None else None for resource in newProcess]
            terminate = True

            for resources in newProcess:
                if resources is None:
                    continue
                if len(resources) > 0:
                    terminate = False
            
            if terminate:
                break
            seconds += 1
            time.sleep(1)
    
    def printProcess(self, processes: List[Process]):
        for i, resource in enumerate(processes, 0):
            if resource is None:
                continue
            print("\n" + "-" * MAX_CHAR_WIDTH)
            
            termcolor.cprint("=====| Resource " + str(i) +" |=====\n", "magenta")
        
            if len(resource) > 0:
                for r in resource:
                    if r is not None:
                        if r.currTime() == 0:
                            termcolor.cprint(r, "green")
                        elif r.isProcessing():
                            termcolor.cprint(r, "red")
                        else:
                            termcolor.cprint(r, attrs=["dark"])
            
            else:
                termcolor.cprint("\nNo Processes in Queue\n", "blue")
        print("\n" + "-" * MAX_CHAR_WIDTH)

def main():
    operatingSystem = OperatingSystem()
    operatingSystem.program()

if __name__ == '__main__':
    main()