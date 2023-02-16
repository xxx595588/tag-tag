from builtins import range
import MalmoPython
from playground_map import playgroundMap
from map import map
import os
import sys
import time
import json
import random
import math
import numpy as np

# length of the playground
SIZE = 20
RUNNER_Z = 0.5
RUNNER_X = -0.5
TAGGER_Z = 0.5
TAGGER_X = -(SIZE-0.5)

plain_map = np.array([
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                     [0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0],
                     [0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1],
                     [1,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0],
                     [0,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  1,  0,  1,  0,  0,  0,  0],
                     [0,  0,  0,  1,  0,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0],
                     [0,  1,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  0,  0,  1,  0,  0,  0,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                     [0,  0,  0,  0,  1,  0,  1,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0],
                     [0,  1,  0,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0],
                     [0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0,  0,  0,  0,  0,  0,  1,  0],
                     [0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  1,  0]])

my_map = None

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

def playground(x, y, z, blocktype):
    global plain_map
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
    plain_map = np.rot90(obs, 1)
    print((abs(int(RUNNER_X)), int(SIZE/2-RUNNER_Z+1)))
    plain_map[abs(int(RUNNER_X))][int(SIZE/2-RUNNER_Z)] = 0
    plain_map[abs(int(TAGGER_X))][int(SIZE/2-TAGGER_Z)] = 0

    print(plain_map)
  
    x = -(SIZE)
    z = -(int(SIZE/2))

    for i, j in zip(np.where(obs == 1)[1], np.where(obs == 1)[0]):
        pg_str += '<DrawLine x1="' + str(x+i) + '" y1="' + str(y) + '" z1="' + str(z+j+1) + '" x2="' + str(x+i) + '" y2="' + str(y+1) + '" z2="' + str(z+j+1) + '" type="bedrock"/>\n'
            
    return pg_str

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Tag Game</Summary>
              </About>
              
              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;1*minecraft:bedrock,1*minecraft:grass;2;village"/>
                  <DrawingDecorator>
                  <DrawLine x1="0" y1="2" z1="0" x2="0" y2="2" z2="11" type="bedrock"/>
                    <DrawLine x1="0" y1="2" z1="0" x2="0" y2="2" z2="-10" type="bedrock"/>
                    <DrawLine x1="0" y1="3" z1="0" x2="0" y2="3" z2="11" type="bedrock"/>
                    <DrawLine x1="0" y1="3" z1="0" x2="0" y2="3" z2="-10" type="bedrock"/>
                    <DrawLine x1="-21" y1="2" z1="0" x2="-21" y2="2" z2="11" type="bedrock"/>
                    <DrawLine x1="-21" y1="2" z1="0" x2="-21" y2="2" z2="-10" type="bedrock"/>
                    <DrawLine x1="-21" y1="3" z1="0" x2="-21" y2="3" z2="11" type="bedrock"/>
                    <DrawLine x1="-21" y1="3" z1="0" x2="-21" y2="3" z2="-10" type="bedrock"/>
                    <DrawLine x1="-20" y1="2" z1="11" x2="0" y2="2" z2="11" type="bedrock"/>
                    <DrawLine x1="-20" y1="2" z1="-10" x2="0" y2="2" z2="-10" type="bedrock"/>
                    <DrawLine x1="-20" y1="3" z1="11" x2="0" y2="3" z2="11" type="bedrock"/>
                    <DrawLine x1="-20" y1="3" z1="-10" x2="0" y2="3" z2="-10" type="bedrock"/>
                    <DrawLine x1="-6" y1="2" z1="-9" x2="-6" y2="3" z2="-9" type="bedrock"/>
                    <DrawLine x1="-20" y1="2" z1="-8" x2="-20" y2="3" z2="-8" type="bedrock"/>
                    <DrawLine x1="-18" y1="2" z1="-8" x2="-18" y2="3" z2="-8" type="bedrock"/>
                    <DrawLine x1="-15" y1="2" z1="-8" x2="-15" y2="3" z2="-8" type="bedrock"/>
                    <DrawLine x1="-2" y1="2" z1="-7" x2="-2" y2="3" z2="-7" type="bedrock"/>
                    <DrawLine x1="-18" y1="2" z1="-6" x2="-18" y2="3" z2="-6" type="bedrock"/>
                    <DrawLine x1="-13" y1="2" z1="-6" x2="-13" y2="3" z2="-6" type="bedrock"/>
                    <DrawLine x1="-6" y1="2" z1="-6" x2="-6" y2="3" z2="-6" type="bedrock"/>
                    <DrawLine x1="-5" y1="2" z1="-6" x2="-5" y2="3" z2="-6" type="bedrock"/>
                    <DrawLine x1="-18" y1="2" z1="-5" x2="-18" y2="3" z2="-5" type="bedrock"/>
                    <DrawLine x1="-17" y1="2" z1="-5" x2="-17" y2="3" z2="-5" type="bedrock"/>
                    <DrawLine x1="-10" y1="2" z1="-5" x2="-10" y2="3" z2="-5" type="bedrock"/>
                    <DrawLine x1="-10" y1="2" z1="-4" x2="-10" y2="3" z2="-4" type="bedrock"/>
                    <DrawLine x1="-17" y1="2" z1="-3" x2="-17" y2="3" z2="-3" type="bedrock"/>
                    <DrawLine x1="-19" y1="2" z1="-1" x2="-19" y2="3" z2="-1" type="bedrock"/>
                    <DrawLine x1="-15" y1="2" z1="-1" x2="-15" y2="3" z2="-1" type="bedrock"/>
                    <DrawLine x1="-13" y1="2" z1="-1" x2="-13" y2="3" z2="-1" type="bedrock"/>
                    <DrawLine x1="-12" y1="2" z1="-1" x2="-12" y2="3" z2="-1" type="bedrock"/>
                    <DrawLine x1="-13" y1="2" z1="0" x2="-13" y2="3" z2="0" type="bedrock"/>
                    <DrawLine x1="-11" y1="2" z1="0" x2="-11" y2="3" z2="0" type="bedrock"/>
                    <DrawLine x1="-4" y1="2" z1="0" x2="-4" y2="3" z2="0" type="bedrock"/>
                    <DrawLine x1="-19" y1="2" z1="1" x2="-19" y2="3" z2="1" type="bedrock"/>
                    <DrawLine x1="-15" y1="2" z1="3" x2="-15" y2="3" z2="3" type="bedrock"/>
                    <DrawLine x1="-12" y1="2" z1="4" x2="-12" y2="3" z2="4" type="bedrock"/>
                    <DrawLine x1="-17" y1="2" z1="5" x2="-17" y2="3" z2="5" type="bedrock"/>
                    <DrawLine x1="-20" y1="2" z1="6" x2="-20" y2="3" z2="6" type="bedrock"/>
                    <DrawLine x1="-15" y1="2" z1="6" x2="-15" y2="3" z2="6" type="bedrock"/>
                    <DrawLine x1="-14" y1="2" z1="6" x2="-14" y2="3" z2="6" type="bedrock"/>
                    <DrawLine x1="-12" y1="2" z1="6" x2="-12" y2="3" z2="6" type="bedrock"/>
                    <DrawLine x1="-10" y1="2" z1="6" x2="-10" y2="3" z2="6" type="bedrock"/>
                    <DrawLine x1="-9" y1="2" z1="6" x2="-9" y2="3" z2="6" type="bedrock"/>
                    <DrawLine x1="-18" y1="2" z1="7" x2="-18" y2="3" z2="7" type="bedrock"/>
                    <DrawLine x1="-9" y1="2" z1="7" x2="-9" y2="3" z2="7" type="bedrock"/>
                    <DrawLine x1="-20" y1="2" z1="9" x2="-20" y2="3" z2="9" type="bedrock"/>
                    <DrawLine x1="-19" y1="2" z1="9" x2="-19" y2="3" z2="9" type="bedrock"/>
                    <DrawLine x1="-3" y1="2" z1="9" x2="-3" y2="3" z2="9" type="bedrock"/>
                    <DrawLine x1="-7" y1="2" z1="10" x2="-7" y2="3" z2="10" type="bedrock"/>
                    <DrawLine x1="-6" y1="2" z1="10" x2="-6" y2="3" z2="10" type="bedrock"/>
                    <DrawLine x1="-5" y1="2" z1="10" x2="-5" y2="3" z2="10" type="bedrock"/>
                    <DrawLine x1="-3" y1="2" z1="10" x2="-3" y2="3" z2="10" type="bedrock"/>
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>Runner</Name>
                <AgentStart>
                  <Placement x="-0.5" y="2" z="0.5" yaw="90"/>
                </AgentStart>
                <AgentHandlers>
                <DiscreteMovementCommands/>
                <ObservationFromGrid>
                <Grid name="floor3x3">
                <min x="-1" y="0" z="-1"/>
                <max x="1" y="0" z="1"/>
                </Grid>
                </ObservationFromGrid>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>

              <AgentSection mode="Survival">
                <Name>Tagger</Name>
                <AgentStart>
                  <Placement x="-19.5" y="2" z="0.5" yaw="-90"/>
                </AgentStart>
                <AgentHandlers>
                <DiscreteMovementCommands/>
                <ObservationFromGrid>
                <Grid name="floor3x3">
                <min x="-1" y="0" z="-1"/>
                <max x="1" y="0" z="1"/>
                </Grid>
                </ObservationFromGrid>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

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

def runner_movement(runner, runner_cur_pos):
    global RUNNER_Z, RUNNER_X
    move = dict()
    # check right
    if SIZE-1-runner_cur_pos[0]-1 >= 0:
        if plain_map[runner_cur_pos[1]][SIZE-1-runner_cur_pos[0]-1] != 1:
            dis = math.sqrt((RUNNER_Z+1-TAGGER_Z)**2 + (RUNNER_X-TAGGER_X)**2)
            move["movenorth"] = dis
    # check left
    if SIZE-1-runner_cur_pos[0]+1 < SIZE:
        if plain_map[runner_cur_pos[1]][SIZE-1-runner_cur_pos[0]+1] != 1:
            dis = math.sqrt((RUNNER_Z-1-TAGGER_Z)**2 + (RUNNER_X-TAGGER_X)**2)
            move["movesouth"] = dis
    # check forward
    if runner_cur_pos[1]+1 < SIZE:
        if plain_map[runner_cur_pos[1]+1][SIZE-1-runner_cur_pos[0]] != 1:
            dis = math.sqrt((RUNNER_Z-TAGGER_Z)**2 + (RUNNER_X+1-TAGGER_X)**2)
            move["movewest"] = dis
    # check back
    if runner_cur_pos[1]-1 >= 0:
        if plain_map[runner_cur_pos[1]-1][SIZE-1-runner_cur_pos[0]] != 1:
            dis = math.sqrt((RUNNER_Z-TAGGER_Z)**2 + (RUNNER_X-1-TAGGER_X)**2)
            move["moveeast"] = dis

    move = dict(sorted(move.items(), key=lambda item:item[1]))

    available = list(move.keys())
    cost = list(move.values())
    best_cost = cost[0]
    best = [available[0]]

    for i, c in enumerate(cost):
        if i == 0:
            continue
        if c <= best_cost:
            best.append(available[i])

    print(best)

    if len(best) == 1:
        next_action = best[0]
    else:
        next_action = random.choice(best)

    if next_action == "movenorth":
        runner.sendCommand("movenorth")
        RUNNER_Z -= 1
    elif next_action == "movesouth":
        runner.sendCommand("movesouth")
        RUNNER_Z += 1
    elif next_action == "moveeast":
        runner.sendCommand("moveeast")
        RUNNER_X += 1
    elif next_action == "movewest":
        runner.sendCommand("movewest")
        RUNNER_X -= 1

def gameover(runner_cur_pos, tagger_cur_pos):
    if ((runner_cur_pos[0] - tagger_cur_pos[0])**2 + (runner_cur_pos[1] - tagger_cur_pos[1])**2) <= 2:
        return True
    return False
    
def main():
  # Create default Malmo objects:
  runner = MalmoPython.AgentHost()
  tagger = MalmoPython.AgentHost()

  my_mission = MalmoPython.MissionSpec(missionXML, True)
  runner_mission_record = MalmoPython.MissionRecordSpec()
  tagger_mission_record = MalmoPython.MissionRecordSpec()

  client_pool = MalmoPython.ClientPool()
  client_pool.add( MalmoPython.ClientInfo("127.0.0.1",10000) )
  client_pool.add( MalmoPython.ClientInfo("127.0.0.1",10001) )

  safeStartMission(runner, my_mission, client_pool, runner_mission_record, 0, "")
  safeStartMission(tagger, my_mission, client_pool, tagger_mission_record, 1, "")
  safeWaitForStart([runner, tagger])

  print("Mission running ", end=' ')

  global RUNNER_Z, RUNNER_X, TAGGER_Z, TAGGER_X

  pmap = playgroundMap(plain_map, int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X)), int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X)))
  my_map = map(SIZE, SIZE, plain_map)

  # Loop until mission ends:
  while True:
      
      print("\n\n")
      #print(".", end="")
      
      #print(f"tagger at {int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X))}")
      #print(f"runner at {int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X))}")
      runner_world_state = runner.getWorldState()
      tagger_world_state = tagger.getWorldState()

      my_map.reset()
      my_map.find_shortest_path()

      if gameover((int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X))), (int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X)))):
        break
      else:
        tagger_action = my_map.retrieve()[-1]

      my_map.update_start(tagger_action)
      tagger_movement(tagger, tagger_action, (int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X))))
      runner_movement(runner, (int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X))))
      pmap.render(int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X)), 0)
      pmap.render(int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X)), 1)
      my_map.update_end((int(SIZE/2-RUNNER_Z+1), int(abs(RUNNER_X))))
      print(plain_map)

      for error in runner_world_state.errors:
          print("Error:",error.text)
      for error in tagger_world_state.errors:
          print("Error:",error.text)
      time.sleep(2)

  print("Game over!")
  # Mission has ended.

if __name__ == "__main__":
    main()