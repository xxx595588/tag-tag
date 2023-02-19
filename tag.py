from builtins import range
import MalmoPython
from playground_map import playgroundMap
from qLearingAgent import QL_agent
from map import map
import os
import sys
import time
import math
import json
import numpy as np
import matplotlib.pyplot as plt

# length of the playground
SIZE = 6
ACTIONS = ["movesouth", "moveeast", "movenorth", "movewest"]
ITERATION = 1000
RUNNER_Z = 0.5
RUNNER_X = -0.5
TAGGER_Z = 0.5
TAGGER_X = -(SIZE-0.5)
SUR_TIME = []
FINAL = []

plain_map = np.array([[0,  0,  0,  0,  0,  0],
                      [0,  0,  1,  0,  0,  0],
                      [0,  0,  0,  0,  0,  0],
                      [0,  0,  0,  0,  0,  0],
                      [0,  0,  0,  0,  1,  0],
                      [0,  1,  0,  0,  0,  0]])

my_map = None

# call this function only when need a new map, copy map_txt to plain_map & pg_str into <DrawingDecorator> field in tag.xml 
def playground(x, y, z, blocktype):
    pg_str = ""

    # density of obstacles
    d = 0.1

    # back fence
    pg_str += '<DrawLine x1="' + str(x) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x) + '" y2="'+ str(y) +'" z2="' + str(z+int(SIZE/2)+1) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x) + '" y2="'+ str(y) +'" z2="' + str(z-int(SIZE/2)) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x) + '" y1="' + str(y+1) + '" z1="' + str(z) + '" x2="' + str(x) + '" y2="'+ str(y+1) +'" z2="' + str(z+int(SIZE/2)+1) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x) + '" y1="' + str(y+1) + '" z1="' + str(z) + '" x2="' + str(x) + '" y2="'+ str(y+1) +'" z2="' + str(z-int(SIZE/2)) + '" type="' + blocktype + '"/>\n'

    # front fence
    pg_str += '<DrawLine x1="' + str(x-SIZE-1) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x-SIZE-1) + '" y2="'+ str(y) +'" z2="' + str(z+int(SIZE/2)+1) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-SIZE-1) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x-SIZE-1) + '" y2="'+ str(y) +'" z2="' + str(z-int(SIZE/2)) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-SIZE-1) + '" y1="' + str(y+1) + '" z1="' + str(z) + '" x2="' + str(x-SIZE-1) + '" y2="'+ str(y+1) +'" z2="' + str(z+int(SIZE/2)+1) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-SIZE-1) + '" y1="' + str(y+1) + '" z1="' + str(z) + '" x2="' + str(x-SIZE-1) + '" y2="'+ str(y+1) +'" z2="' + str(z-int(SIZE/2)) + '" type="' + blocktype + '"/>\n'

    # side fence
    pg_str += '<DrawLine x1="' + str(x-SIZE) + '" y1="' + str(y) + '" z1="' + str(z+int(SIZE/2)+1) + '" x2="' + str(x) + '" y2="'+ str(y) +'" z2="' + str(z+int(SIZE/2)+1) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-SIZE) + '" y1="' + str(y) + '" z1="' + str(z-int(SIZE/2)) + '" x2="' + str(x) + '" y2="'+ str(y) +'" z2="' + str(z-int(SIZE/2)) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-SIZE) + '" y1="' + str(y+1) + '" z1="' + str(z+int(SIZE/2)+1) + '" x2="' + str(x) + '" y2="'+ str(y+1) +'" z2="' + str(z+int(SIZE/2)+1) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-SIZE) + '" y1="' + str(y+1) + '" z1="' + str(z-int(SIZE/2)) + '" x2="' + str(x) + '" y2="'+ str(y+1) +'" z2="' + str(z-int(SIZE/2)) + '" type="' + blocktype + '"/>\n'
    # randomly place obstacles
    obs = np.zeros((SIZE **2,), dtype = np.int8)
    obs[np.random.choice(SIZE**2, replace = False, size = int((SIZE**2)*d) )] = 1
    obs = np.reshape(obs, (SIZE ,SIZE))
    map_txt = np.rot90(obs, 1)
    map_txt[abs(int(RUNNER_X))][int(SIZE/2-RUNNER_Z)] = 0
    map_txt[abs(int(TAGGER_X))][int(SIZE/2-TAGGER_Z)] = 0
  
    x = -(SIZE)
    z = -(int(SIZE/2))

    for i, j in zip(np.where(obs == 1)[1], np.where(obs == 1)[0]):
        pg_str += '<DrawLine x1="' + str(x+i) + '" y1="' + str(y) + '" z1="' + str(z+j+1) + '" x2="' + str(x+i) + '" y2="' + str(y+1) + '" z2="' + str(z+j+1) + '" type="bedrock"/>\n'
            
    return map_txt, pg_str

# start the mission safely by catching any exception
def safeStartMission(agent_host, mission, client_pool, recording, role, experimentId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            agent_host.startMission(mission, client_pool, recording, role, experimentId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")

# wait all agent start their mission
def safeWaitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow two minutes for mission to start.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')

    if time.time() - start_time >= time_out:
        print("Timed out waiting for mission to begin. Bailing.")
        exit(1)
    print("Mission has started.")

# control the movement of tagger
def tagger_movement(tagger, tagger_action, tagger_cur_pos):
    global TAGGER_Z, TAGGER_X

    if tagger_cur_pos[0] - tagger_action[0] == 1:
        tagger.sendCommand("movesouth")
        TAGGER_Z += 1
    elif tagger_cur_pos[0] - tagger_action[0] == -1:
        tagger.sendCommand("movenorth")
        TAGGER_Z -= 1
    elif tagger_cur_pos[1] - tagger_action[1] == 1:
        tagger.sendCommand("moveeast")
        TAGGER_X += 1
    elif tagger_cur_pos[1] - tagger_action[1] == -1:
        tagger.sendCommand("movewest")
        TAGGER_X -= 1

# control the movement of runner
def runner_movement(runner, A, runner_cur_pos, tagger_cur_pos):
    global RUNNER_Z, RUNNER_X, TAGGER_Z, TAGGER_X
    
    """
    position 4 is runner's current position

               W (-x)
               |
             6 3 0
    S (+z)-- 7 4 1 --N (-z)
             8 5 2
               |
               E (+x)
    
    """
    
    ori_dis = math.sqrt((runner_cur_pos[0]-tagger_cur_pos[0])**2 + (runner_cur_pos[1]-tagger_cur_pos[1])**2)

    if A == "movenorth":
        if SIZE-1-runner_cur_pos[0]-1 >= 0 and plain_map[runner_cur_pos[1]][SIZE-1-runner_cur_pos[0]-1] != 1:
            runner.sendCommand("movenorth")
            RUNNER_Z -= 1
            next_S = ((int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))), tagger_cur_pos)
        else:
            next_S = (runner_cur_pos, tagger_cur_pos)
    elif A == "movesouth":
        if SIZE-1-runner_cur_pos[0]+1 < SIZE and plain_map[runner_cur_pos[1]][SIZE-1-runner_cur_pos[0]+1] != 1:
            runner.sendCommand("movesouth")
            RUNNER_Z += 1
            next_S = ((int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))), tagger_cur_pos)
        else:
            next_S = (runner_cur_pos, tagger_cur_pos)
    elif A == "movewest":
        if runner_cur_pos[1]+1 < SIZE and plain_map[runner_cur_pos[1]+1][SIZE-1-runner_cur_pos[0]] != 1:
            runner.sendCommand("movewest")
            RUNNER_X -= 1
            next_S = ((int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))), tagger_cur_pos)
        else:
            next_S = (runner_cur_pos, tagger_cur_pos)
    elif A == "moveeast":
        if runner_cur_pos[1]-1 >= 0 and plain_map[runner_cur_pos[1]-1][SIZE-1-runner_cur_pos[0]] != 1:
            runner.sendCommand("moveeast")
            RUNNER_X += 1
            next_S = ((int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))), tagger_cur_pos)
        else:
            next_S = (runner_cur_pos, tagger_cur_pos)

    new_dis = math.sqrt((runner_cur_pos[0]-tagger_cur_pos[0])**2 + (runner_cur_pos[1]-tagger_cur_pos[1])**2)

    if new_dis <= math.sqrt(2):
        reward = -100
    elif new_dis - ori_dis < 0:
        reward = 100*(new_dis - ori_dis)/ori_dis
    elif new_dis == ori_dis:
        reward = 5
    else:
        reward = 10
  
    return next_S, reward

def gameover(runner_cur_pos, tagger_cur_pos):
    if ((runner_cur_pos[0] - tagger_cur_pos[0])**2 + (runner_cur_pos[1] - tagger_cur_pos[1])**2) <= 1:
        return True
    return False
    
def main():
    global RUNNER_Z, RUNNER_X, TAGGER_Z, TAGGER_X, ACTIONS, SIZE, ITERATION, plain_map, my_map, SUR_TIME, FINAL

    runner_coor = (int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X)))
    tagger_coor = (int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X)))

    pmap = playgroundMap(plain_map, runner_coor[0], runner_coor[1], tagger_coor[0], tagger_coor[1])
    my_map = map(plain_map)
    agent = QL_agent(ACTIONS, len(plain_map[0]), len(plain_map))
    copy_map = plain_map

    mission_file = "./tag.xml"
    with open(mission_file, "r") as f:
        print(f"Loading mission from {mission_file}")
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)

    runner = MalmoPython.AgentHost()
    tagger = MalmoPython.AgentHost()

    runner_mission_record = MalmoPython.MissionRecordSpec()
    tagger_mission_record = MalmoPython.MissionRecordSpec()

    client_pool = MalmoPython.ClientPool()
    client_pool.add( MalmoPython.ClientInfo("127.0.0.1",10000) )
    client_pool.add( MalmoPython.ClientInfo("127.0.0.1",10001) )

    safeStartMission(runner, my_mission, client_pool, runner_mission_record, 0, "")
    safeStartMission(tagger, my_mission, client_pool, tagger_mission_record, 1, "")
    safeWaitForStart([runner, tagger])

    print("Mission running ", end=' ')

    for i in range(ITERATION):
        print(f"Iteration {i+1}")
        start = time.time()
        plain_map = copy_map
        terminated = False

        RUNNER_Z = 0.5
        RUNNER_X = -0.5
        TAGGER_Z = 0.5
        TAGGER_X = -(SIZE-0.5)

        my_map.update_start((int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X))))
        my_map.update_end((int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))))

        runner.sendCommand("tp -0.5 2 0.5")
        tagger.sendCommand("tp -5.5 2 0.5")
        while True:
            S =((int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X))), (int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X))))
            #print("\n\n")
            #print(".", end="")
            #print(f"tagger at {int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X))}")
            #print(f"runner at {int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X))}")

            my_map.reset()
            my_map.find_shortest_path()

            if gameover((int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X))), (int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X)))):
                end = time.time()
                terminated = True
            else:
                tagger_action = my_map.retrieve()[-1]

            my_map.update_start(tagger_action)
            tagger_movement(tagger, tagger_action, (int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X))))
            A = agent.choose_action(S)
            next_S, R = runner_movement(runner, A, (int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))), (int(SIZE/2-TAGGER_Z+1), int(abs(TAGGER_X))))
            agent.update_qtable(A, S, next_S, R, terminated)
            pmap.render(int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X)), 0)
            pmap.render(int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X)), 1)
            my_map.update_end((int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))))

            if terminated:
                break

        SUR_TIME.append(end-start)

        if len(SUR_TIME) == 50:
            med = np.average(SUR_TIME)
            FINAL.append(med)
            SUR_TIME = []
        print("Game over!")

    plt.plot(range(len(FINAL)), FINAL)
    plt.show()
    agent.export_data()   
    # Mission has ended.

if __name__ == "__main__":
    main()