import math

class SpaceMemory(object):
    """ A structure that stores and keeps trace of observed objects """

    
    def __init__(self):
        self.cubes=[[0 for y in range(5)] for x in range(3)]    # position of the three cubes, (X,Y,theta, color,age)
        for i in range(3):
            self.cubes[i][4]=21 # age greater than 20 indicates no information

        self.bumps=[]                       # position of detected bumps  (X,Y,theta,age)


    def update(self,enacted):
        
        if enacted==0:  # forward : everything move backward
            for i in range(3):
                self.cubes[i][1]-=10    # TODO : calibration
                self.cubes[i][4]+=1

            for i in range(len(self.bumps)):
                self.bumps[i][1]-=10    # TODO : calibration
                self.bumps[i][3]+=1

        if enacted==1:  #  bump : no movement
            for i in range(3):
                self.cubes[i][4]+=1
            for i in range(len(self.bumps)):
                self.bumps[i][3]+=1

        if enacted==2:  # push : everything move backward except pushed cube
            for i in range(3):
                if cubes[i][0]<-5 or cubes[i][0]>5 or cubes[i][1]<0 or cubes[i][1]>10: # TODO : calibration
                    self.cubes[i][1]-=10    # TODO : calibration
                self.cubes[i][4]+=1

            for i in range(len(self.bumps)):
                self.bumps[i][1]-=10    # TODO : calibration
                self.bumps[i][3]+=1

        if enacted==3:  # eat : cube changes to red
            for i in range(3):
                if cubes[i][0]>-5 and cubes[i][0]<5 and cubes[i][1]>0 or cubes[i][1]<10: # TODO : calibration
                    self.cubes[i][3]=1  # cube becomes red
                self.cubes[i][4]+=1

            for i in range(len(self.bumps)):
                self.bumps[i][3]+=1

        if enacted==4:  #  miss : no movement
            for i in range(3):
                self.cubes[i][4]+=1
            for i in range(len(self.bumps)):
                self.bumps[i][3]+=1

        if enacted==5:  # charge : cube changes to green
            for i in range(3):
                if cubes[i][0]>-5 and cubes[i][0]<5 and cubes[i][1]>0 or cubes[i][1]<10: # TODO : calibration
                    self.cubes[i][3]=0  # cube becomes red
                self.cubes[i][4]+=1

            for i in range(len(self.bumps)):
                self.bumps[i][1]-=10    # TODO : calibration
                self.bumps[i][3]+=1

        if enacted>=6: # rotations
            angle=90            # TODO : check rotation direction
            if enacted==7: angle=-90
            elif enacted==8: angle=45
            elif enacted==9: angle=-45

            for i in range(3):
                x=self.cubes[i][0]
                y=self.cubes[i][1]
                self.cubes[i][0]= math.cos(math.radians(angle)) - math.sin(math.radians(angle))
                self.cubes[i][1]= math.sin(math.radians(angle)) + math.cos(math.radians(angle))
                self.cubes[i][2]+=angle
                self.cubes[i][4]+=1

            for i in range(len(self.bumps)):
                x=self.bumps[i][0]
                y=self.bumps[i][1]
                self.bumps[i][0]= math.cos(math.radians(angle)) - math.sin(math.radians(angle))
                self.bumps[i][1]= math.sin(math.radians(angle)) + math.cos(math.radians(angle))
                self.bumps[i][2]+=angle
                self.bumps[i][3]+=1

        # remove old bumps
        for i in range(len(self.bumps)):
            if self.bumps[i][3]>20: # keep elements for 20 cycles
                del self.bumps[i]
                i-=1


    def cubeDetected(self, index, pos_x, pos_y, color, angle):
        self.cubes[index][0]=pos_x
        self.cubes[index][1]=pos_y
        self.cubes[index][2]=angle
        self.cubes[index][3]=color
        self.cubes[index][4]=0

    def bumpDetected(self):
        self.cube.append([0,0,0,0])



    def getMatrix(self):    # get the matrix characterizing the environment according to memory
        env=[[[0 for y in range(100)] for x in range(100)] for l in range(4)]   # layer 0 : user, layer 1 : red cube, layer 2 : green cube, layer 3 : bump

        # user
        if self.cubes[0][4]<20: # position not too old
            for i in range (-3,4):  # TODO : define size of the cube
                for j in range (-3,4):  
                    if self.cubes[0][0]+50+i>=0 and self.cubes[0][0]+50+i<100 and self.cubes[0][1]+50+j>=0 and self.cubes[0][1]+50+j<100:
                        env[0][self.cubes[0][0]+50+i][self.cubes[0][1]+50+j]=1

        # cubes
        for c in range(1,3):
            if self.cubes[c][4]<20:
                for i in range (-3,4):  # TODO : define size of the cube
                    for j in range (-3,4):  
                        if self.cubes[c][0]+50+i>=0 and self.cubes[c][0]+50+i<100 and self.cubes[c][1]+50+j>=0 and self.cubes[c][1]+50+j<100:
                            env[self.cubes[c][3]+1][self.cubes[c][0]+50+i][self.cubes[c][1]+50+j]=1

        # bumps
        for b in range(len(self.bumps)):
            if self.bumps[b][3]<20:
                for i in range (-3,4):  # TODO : define size of the cube
                    for j in range (-3,4):  
                        if self.bumps[b][0]+50+i>=0 and self.bumps[b][0]+50+i<100 and self.bumps[b][1]+50+j>=0 and self.bumps[b][1]+50+j<100:
                            env[3][self.bumps[b][0]+50+i][self.bumps[b][1]+50+j]=1

        return env


