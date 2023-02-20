from builtins import range
from playground_map import playgroundMap
from tagger import tagger
from runner import runner
import MalmoPython
import time
import numpy as np
import matplotlib.pyplot as plt

# length of the playground
SIZE = 6
ITERATION = 2000
RUNNER_Z = 0.5
RUNNER_X = -0.5
TAGGER_Z = 0.5
TAGGER_X = -(SIZE-0.5)
SUR_TIME = []
FINAL = []

plain_map = np.array([[0,  0,  8,  0,  0,  0],
                      [0,  0,  1,  0,  0,  0],
                      [0,  0,  0,  0,  0,  0],
                      [0,  0,  0,  0,  0,  0],
                      [0,  0,  0,  0,  1,  0],
                      [0,  1,  4,  0,  0,  0]])

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

def main():
    global RUNNER_Z, RUNNER_X, TAGGER_Z, TAGGER_X, SIZE, ITERATION, plain_map, SUR_TIME, FINAL

    # creating runner & tagger agent 
    runner_agent = runner(MalmoPython.AgentHost(), plain_map, RUNNER_Z, RUNNER_X)
    tagger_agent = tagger(MalmoPython.AgentHost(), plain_map, TAGGER_Z, TAGGER_X)

    # get the most current coordinate for both runner & tagger
    runner_coor = runner_agent.convert_coor()
    tagger_coor = tagger_agent.convert_coor()

    # creating the bird eye view map window
    pmap = playgroundMap(plain_map, runner_coor[0], runner_coor[1], tagger_coor[0], tagger_coor[1])
    
    # read the mission file
    mission_file = "./tag.xml"
    with open(mission_file, "r") as f:
        print(f"Loading mission from {mission_file}")
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)

    runner_mission_record = MalmoPython.MissionRecordSpec()
    tagger_mission_record = MalmoPython.MissionRecordSpec()

    client_pool = MalmoPython.ClientPool()
    client_pool.add( MalmoPython.ClientInfo("127.0.0.1",10000) )
    client_pool.add( MalmoPython.ClientInfo("127.0.0.1",10001) )

    safeStartMission(runner_agent.getAgent(), my_mission, client_pool, runner_mission_record, 0, "")
    safeStartMission(tagger_agent.getAgent(), my_mission, client_pool, tagger_mission_record, 1, "")
    safeWaitForStart([runner_agent.getAgent(), tagger_agent.getAgent()])

    print("Mission running ", end=' ')

    for i in range(ITERATION):
        print(f"Iteration {i+1}")
        start = time.time()
        
        runner_agent.teleport(RUNNER_X, RUNNER_Z)
        tagger_agent.teleport(TAGGER_X, TAGGER_Z)
        runner_coor = runner_agent.convert_coor()
        tagger_coor = tagger_agent.convert_coor()

        while not runner_agent.is_caught(tagger_coor):
            S = (runner_coor, tagger_coor)
            tagger_agent.find_path(runner_coor)

            tagger_coor = tagger_agent.convert_coor()
            if runner_agent.is_caught(tagger_coor):
                break
            S = (runner_coor, tagger_coor)
            runner_agent.next_action(S)

            runner_coor = runner_agent.convert_coor()
            pmap.render(runner_coor[0], runner_coor[1], 0)
            pmap.render(tagger_coor[0], tagger_coor[1], 1)

        end = time.time()
    
        SUR_TIME.append(end-start)

        if len(SUR_TIME) == 50:
            mid = np.average(SUR_TIME)
            FINAL.append(mid)
            SUR_TIME = []
        print("Game over!")

    plt.plot(range(len(FINAL)), FINAL)
    plt.show()
    runner_agent.export_qtable()   
    # Mission has ended.

if __name__ == "__main__":
    main()