

enacted=0

pos_robot=1
pos_user=1

hunger_robot=1
hunger_user=1

cube1=1 # green
cube2=1 # green

# 0 turn left, 1 turn right, 2 eat , 3 charge, 4 observe

def getSequences(position):
    sequences=[]
    if position==0:
        if cube1==1:
            sequences.append([2])
            sequences.append([2,3])
        else:
            sequences.append([3])
            sequences.append([3,2])

        sequences.append([0])
        sequences.append([0,4])

        if cube2==1:
            sequences.append([0,0,2])
            sequences.append([0,0,2,3])
        else:
            sequences.append([0,0,3])
            sequences.append([0,0,3,2])

    if position==1:
        if cube1==1:
            sequences.append([1,2])
            sequences.append([1,2,3])
        else:
            sequences.append([1,3])
            sequences.append([1,3,2])

        sequences.append([0])
        sequences.append([1])
        sequences.append([4])

        if cube2==1:
            sequences.append([0,2])
            sequences.append([0,2,3])
        else:
            sequences.append([0,3])
            sequences.append([0,3,2])

    if position==2:
        if cube1==1:
            sequences.append([1,1,2])
            sequences.append([1,1,2,3])
        else:
            sequences.append([1,1,3])
            sequences.append([1,1,3,2])

        sequences.append([1])
        sequences.append([1,4])

        if cube2==1:
            sequences.append([2])
            sequences.append([2,3])
        else:
            sequences.append([3])
            sequences.append([3,2])

    return sequences


def getValence(sequence, hunger):
    valence=0
    for i in range(len(sequence)):
        if   sequence[i]==0: valence+=-1
        elif sequence[i]==1: valence+=-1
        elif sequence[i]==2: valence+=50*hunger
        elif sequence[i]==3: valence+=-5
        elif sequence[i]==4: valence+=0
    return valence


def mainLoop():
    sequences=getSequences(pos_robot)
    print(sequences)
    valences=[]
    for seq in sequences:
         valences.append(getValence(seq,hunger_robot))
    
    print(valences)
    
    index_max=-1
    val_max=-1000
    
    for i in range(len(valences)):
        if valences[i]>val_max:
            index_max=i
            val_max=valences[i]
    
    intended=sequences[index_max][0]
    
    print(intended)
    
    # intend interaction with robot
    
    if hunger_robot<1: hunger_robot+=0.1


if __name__ == "__main__":
    mainLoop()

