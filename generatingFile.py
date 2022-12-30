
from itertools import count
from random import random
from tokenize import String
import random
import math
from typing import Counter

COLUMNS = 100
ROWS = 50

for i in range(1,51) : 
    with open("coordinates_" + str(i) + ".txt", "w") as testFile:
        list = []
        nonBlockedList = []
        n = (COLUMNS + 1)*(ROWS + 1)*(0.1)
        n = math.ceil(n)

        #randomly get the 10% blocked vertexes 
        counter = n 
        for i in range(1,counter+1):
            r_x = random.randint(1, COLUMNS)
            r_y = random.randint(1, ROWS)
            list.append((r_x,r_y))

        # FILL UP THE LIST WITH BLOCKED INFO
        for x in range(1,(COLUMNS + 1)) :
            for y in range(1,(ROWS + 1)) :
                if (x,y) not in list :
                    list.append((x,y,0))
                    nonBlockedList.append((x,y))
                else:
                    list.remove((x,y))
                    list.append((x,y,1))

        # remove the duplicated vertex 
        counter = len(list) - 1
        while(counter):
            if(len(list[counter]) == 2) :
                list.remove(list[counter])
            counter = counter - 1
        
        # check the first index bc while loop stops when counter = 0
        if(len(list[0]) == 2) :
                list.remove(list[0])
        
        start_vertex = nonBlockedList[random.randint(0, len(nonBlockedList) - 1)]
        goal_vertex = nonBlockedList[random.randint(0, len(nonBlockedList) - 1)]
        if (start_vertex == goal_vertex):
            goal_vertex = nonBlockedList[random.randint(0, len(nonBlockedList) - 1)]
        
        # matrix 
        matrix = (COLUMNS,ROWS)

        testFile.write(str(start_vertex[0]) + " " + str(start_vertex[1]) + "\n")
        testFile.write(str(goal_vertex[0]) + " " + str(goal_vertex[1]) + "\n")  
        testFile.write(str(matrix[0]) + " " + str(matrix[1]) + "\n")  
        for i in range (len(list)):
            testFile.write(str(list[i][0]) + " " + str(list[i][1]) + " " +  str(list[i][2]) + "\n")
            
        testFile.close()


