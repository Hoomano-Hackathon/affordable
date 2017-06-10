import math
from copy import copy, deepcopy

class Signatures(object):

    def __init__(self):
        self.values=[[[[0 for y in range(100)] for x in range(100)] for layer in range(4)] for interaction in range(10)]

        # define signature for each interaction

        # forward : no object in front of the robot (pos : [50;50])
        for layer in range(4):
            for i in range(47,54):
                for j in range(54,60):
                    self.values[0][layer][i][j]=-1

        # bump : wall in front of the robot
        for i in range(47,54):
            for j in range(54,60):
                self.values[1][3][i][j]=1

        # push : red or green cube in front of the robot
        for layer in range(1,3):
            for i in range(47,54):
                for j in range(54,60):
                    self.values[2][layer][i][j]=1

        # eat : green cube in front of the robot
        for i in range(47,54):
            for j in range(54,60):
                self.values[3][2][i][j]=1

        # miss : no cube in front of the robot
        for i in range(47,54):
            for j in range(54,60):
                self.values[4][1][i][j]=-1
                self.values[4][2][i][j]=-1

        # charge : red cube in front of the robot
        for i in range(47,54):
            for j in range(54,60):
                self.values[5][1][i][j]=1


        # turns : always true : no changes


        # TODO : projections
        self.projection=[[[[None for y in range(100)] for x in range(100)] for layer in range(4)] for interaction in range(10)]

        # initialize
        for inter in range(6):
            for layer in range(4):
                for i in range(100):
                    for j in range(100):
                        if self.values[inter][layer][i][j]!=0:
                            self.projection[inter][layer][i][j]=[]

        # project
        for step in range(3):
            projection_buff=deepcopy(self.projection)
            for inter in range(6):
                for layer in range(4):
                    for i in range(100):
                        for j in range(100):
                            if projection_buff[inter][layer][i][j]!=None:
                                #-------------------------------------------
                                # project through forward
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(0)  # new sequence

                                # insert sequence "forward"
                                if j+10<100:
                                    if self.projection[inter][layer][i][j+10]==None: # TODO calibration
                                        self.projection[inter][layer][i][j+10]=sequence
                
                                #-------------------------------------------
                                # project through push
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(2)  # new sequence

                                # object in front of the agent does not move
                                if j+10<100:
                                    if i<47 or i>54 or j<54 or j>60:    # exclude object in front
                                        if self.projection[inter][layer][i][j+10]==None: # TODO calibration
                                            self.projection[inter][layer][i][j+10]=sequence
                        
                                #-------------------------------------------
                                # project through eat
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(3)  # new sequence
                                
                                # change color of object in front of the agent
                                if layer==2 and i>=47 and i<54 and j>=54 and j<60:  # red object in front was green before eat
                                    if self.projection[inter][1][i][j]==None:
                                        self.projection[inter][1][i][j]=sequence

                                
                                #-------------------------------------------
                                # project through charge
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(5)  # new sequence

                                # change color of object in front of the agent
                                if layer==1 and i>=47 and i<54 and j>=54 and j<60:  # green object in front was red before charge
                                    if self.projection[inter][2][i][j]==None:
                                        self.projection[inter][2][i][j]=sequence
            
                                #-------------------------------------------
                                # project through turn right 90deg
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(6)  # new sequence

                                # rotate objects TODO : check rotation direction
                                x=i-50
                                y=j-50
                                x2=x*math.cos(math.radians(90)) - y*math.sin(math.radians(90))
                                y2=x*math.sin(math.radians(90)) + y*math.cos(math.radians(90))
                                if x2>=-50 and x2<50 and y2>=-50 and y2<50:
                                    if self.projection[inter][layer][int(x2+50)][int(y2+50)]==None:
                                        self.projection[inter][layer][int(x2+50)][int(y2+50)]=sequence

                                #-------------------------------------------
                                # project through turn left 90deg
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(7)  # new sequence

                                # rotate objects TODO : check rotation direction
                                x=i-50
                                y=j-50
                                x2=x*math.cos(math.radians(-90)) - y*math.sin(math.radians(-90))
                                y2=x*math.sin(math.radians(-90)) + y*math.cos(math.radians(-90))
                                if x2>=-50 and x2<50 and y2>=-50 and y2<50:
                                    if self.projection[inter][layer][int(x2+50)][int(y2+50)]==None:
                                        self.projection[inter][layer][int(x2+50)][int(y2+50)]=sequence

                                #-------------------------------------------
                                # project through turn right 45deg
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(8)  # new sequence

                                # rotate objects TODO : check rotation direction
                                x=i-50
                                y=j-50
                                x2=x*math.cos(math.radians(45)) - y*math.sin(math.radians(45))
                                y2=x*math.sin(math.radians(45)) + y*math.cos(math.radians(45))
                                if x2>=-50 and x2<50 and y2>=-50 and y2<50:
                                    if self.projection[inter][layer][int(x2+50)][int(y2+50)]==None:
                                        self.projection[inter][layer][int(x2+50)][int(y2+50)]=sequence


                                #-------------------------------------------
                                # project through turn left 45deg
                                sequence=list(projection_buff[inter][layer][i][j])
                                sequence.append(9)  # new sequence

                                # rotate objects TODO : check rotation direction
                                x=i-50
                                y=j-50
                                x2=x*math.cos(math.radians(-45)) - y*math.sin(math.radians(-45))
                                y2=x*math.sin(math.radians(-45)) + y*math.cos(math.radians(-45))
                                if x2>=-50 and x2<50 and y2>=-50 and y2<50:
                                    if self.projection[inter][layer][int(x2+50)][int(y2+50)]==None:
                                        self.projection[inter][layer][int(x2+50)][int(y2+50)]=sequence

    def predict(self, inter, env):
        if inter<6:

            sum=0
            for layer in range(4):
                for i in range(100):
                    for j in range(100):
                        sum+=env[layer][i][j]*self.values[inter][layer][i][j]

            if inter==0: # forward
                return sum==0

            elif inter==1: # bump
                return sum>0

            elif inter==2: # puch
                return sum>0

            elif inter==3: # eat
                return sum>0

            elif inter==4: # miss
                return sum==0

            elif inter==5: # charge
                return sum>0

        else: return True   # turns interactions    

    def of(self, interaction):
        self.values[interaction]

    def getPositions(self, environment):
        sequences=[ [] for y in range(6)]

        # detect sequences
        for inter in range(6):
            for layer in range(4):
                for i in range(100):
                    for j in range(100):
                        if (environment[layer][i][j]!=0 and
                                self.signatures[inter][layer][i][j]!=None):
                            sequences[inter.append(self.signatures[inter][layer][i][j])]
        return sequences


