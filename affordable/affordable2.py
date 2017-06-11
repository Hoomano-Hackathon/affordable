import cozmo
import time
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.util import degrees

enacted=0

pos_robot=1
pos_user=1

hunger_robot=1
hunger_user=1

cube1=1 # green
cube2=1 # green

last_observed_user_pos=1

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


def handle_tapped(evt, **kw):
    global cube1
    global cube2

    print("Tapped: ", evt.obj.object_id)
    if evt.obj.object_id == 0:
        if cube1 == 1:
            evt.obj.set_lights(cozmo.lights.red_light)
            cube1=0
    elif evt.obj.object_id == 2:
        if cube2 == 1:
            evt.obj.set_lights(cozmo.lights.red_light)
            cube2=0



def mainLoop(robot: cozmo.robot.Robot):
    global hunger_robot
    global pos_robot
    global cube1
    global cube2
    global last_observed_user_pos

    robot.add_event_handler(cozmo.objects.EvtObjectTapped, handle_tapped)

    light_cube1 = robot.world.get_light_cube(LightCube1Id)  # looks like a paperclip
    # light_cube2 = robot.world.get_light_cube(LightCube2Id)  # looks like a lamp / heart
    light_cube3 = robot.world.get_light_cube(LightCube3Id)  # looks like the letters 'ab' over 'T'

    if light_cube1:
        light_cube1.set_lights(cozmo.lights.green_light)

    # light_cube2.set_lights(cozmo.lights.green_light)
    if light_cube3:
        light_cube3.set_lights(cozmo.lights.green_light)

    f = open('activity_trace', 'w')
    i = 1

    exitOrNot = ""
    found = False
    text_help = 0
    while exitOrNot != "q":
        f.write("STEP " + str(i))
        f.write("\nROBOT\n")
        sequences=getSequences(pos_robot)
        print(sequences)
        f.write(str(sequences))
        valences=[]
        for seq in sequences:
            valences.append(getValence(seq,hunger_robot))
    
        print(valences)
        f.write(str(valences))

        # define expected user valences as defined by the robot
        f.write("\nUSER\n")
        sequences_user = getSequences(last_observed_user_pos)
        print(sequences_user)
        f.write(str(sequences))
        valences_user = []
        for seq in sequences_user:
            valences_user.append(getValence(seq, hunger_user))
        print(valences_user)
        f.write(str(valences_user))

        # try to define intention of the user
        sorted_list = sorted(valences_user)

        if sorted_list[-1] > sorted_list[-2]:  # intention of the user is obvious
            index_max_user = -1
            val_max_user = -1000

            for i in range(len(valences_user)):
                if valences_user[i] > val_max_user:
                    index_max_user = i
                    val_max_user = valences_user[i]

                    # get most possible profitable sequence for the user
            best_sequence = sequences_user[index_max_user]
            print(best_sequence)
            # look for impossible interactions
            i = 0
            found=False
            while i < len(best_sequence) and not found:
                if best_sequence[i] == 3: found = True
                i += 1

            if found:
                if text_help==0:
                    robot.say_text("Help", voice_pitch=1.5).wait_for_completed()
                    text_help=1
                # hard-coded relation between objects in robot and user point of view
                print("found")
                if pos_robot == 0:
                    if last_observed_user_pos == 0:
                        valences[0] += val_max_user
                    elif last_observed_user_pos == 2:
                        valences[4] += val_max_user
                elif pos_robot == 1:
                    if last_observed_user_pos == 0:
                        valences[0] += val_max_user
                    elif last_observed_user_pos == 2:
                        valences[5] += val_max_user
                elif pos_robot == 2:
                    if last_observed_user_pos == 0:
                        valences[0] += val_max_user
                    elif last_observed_user_pos == 2:
                        valences[4] += val_max_user
            else:
                text_help=0

        index_max=-1
        val_max=-1000
    
        for i in range(len(valences)):
            if valences[i]>val_max:
                index_max=i
                val_max=valences[i]
    
        intended=sequences[index_max][0]

        print(intended)

        if found:
            f.write("\nINTENDED: " + str(intended) + " Assistance\n\n")
        else:
            f.write("\nINTENDED: " + str(intended) + " Exploitation\n\n")

        # intend interaction with robot
        if intended == 0: # turn left
            robot.turn_in_place(degrees(45)).wait_for_completed()
            pos_robot+=1
        elif intended == 1: # turn right
            robot.turn_in_place(degrees(-45)).wait_for_completed()
            pos_robot-=1
        elif intended == 2: # eat
            if pos_robot == 0:
                if cube1 == 1:
                    light_cube1.set_lights(cozmo.lights.red_light)
                    cube1=0
            elif pos_robot == 2:
                if cube2 == 1:
                    light_cube3.set_lights(cozmo.lights.red_light)
                    cube2 = 0
            hunger_robot=-0.5
            robot.set_lift_height(0.7).wait_for_completed()
            time.sleep(0.5)
            robot.set_lift_height(1.0).wait_for_completed()
            time.sleep(1)
            robot.say_text("Delicious", voice_pitch=1.5).wait_for_completed()
        elif intended == 3: # charge
            if pos_robot == 0:
                if cube1 == 0:
                    light_cube1.set_lights(cozmo.lights.green_light)
                    cube1=1
            elif pos_robot == 2:
                if cube2 == 0:
                    light_cube3.set_lights(cozmo.lights.green_light)
                    cube2=1
            robot.set_lift_height(0.7).wait_for_completed()
            time.sleep(0.5)
            robot.set_lift_height(1.0).wait_for_completed()
            time.sleep(1)
            #robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()
        elif intended == 4:
            time.sleep(2)

        if pos_robot == 1:
            cube = robot.world.wait_for_observed_light_cube(timeout=5)

            if cube is not None:
                line=str(cube.pose).split(" ")
                angle=float(line[21].replace('(', ''))
                print(angle)

                if angle < 45 and angle > -45:
                    last_observed_user_pos=1
                elif angle >= 45:
                    last_observed_user_pos=0
                elif angle < -45:
                    last_observed_user_pos=2

                print(last_observed_user_pos)


        if hunger_robot<1:hunger_robot+=0.05
        i+=1
        # exitOrNot = input('Press ENTER to continue.')


# if __name__ == "__main__":
#    mainLoop()

def main():
    cozmo.run_program(mainLoop)
