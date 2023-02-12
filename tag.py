from builtins import range
import MalmoPython
from playground_map import playgroundMap
import os
import sys
import time
import json
import numpy as np

# length of the playground
SIZE = 30
RUNNER_Z = 0.5
RUNNER_X = -0.5
TAGGER_Z = 0.5
TAGGER_X = -29.5

map = []

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

def playground(x, y, z, blocktype):
    global map
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
    map = np.rot90(obs, 1)  
  
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
                  ''' + playground(0, 2, 0, "bedrock") + '''
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
                  <Placement x="-29.5" y="2" z="0.5" yaw="-90"/>
                </AgentStart>
                <AgentHandlers>
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

  pmap = playgroundMap(map, int(SIZE/2-RUNNER_Z+1), abs(int(RUNNER_X)), int(SIZE/2-TAGGER_Z+1), abs(int(TAGGER_X)))

  # Loop until mission ends:
  #while world_state.is_mission_running:
  while True:
      #print(".", end="")
      time.sleep(0.1)
      runner_world_state = runner.getWorldState()
      tagger_world_state = tagger.getWorldState()
      #print(f"Runner at ({RUNNER_Z}, {RUNNER_X})")
      #print(f"Tagger at ({TAGGER_Z}, {TAGGER_X})")

      if runner_world_state.number_of_observations_since_last_state > 0:
          runner_obs = json.loads(runner_world_state.observations[0].text)
          grid = runner_obs.get(f"floor3x3", 0)
          if runner_obs.get("ZPos", 0)-RUNNER_Z < -0.5:
              pmap.render(int(SIZE/2-runner_obs.get("ZPos", 0)+1), abs(int(runner_obs.get("XPos", 0))), 0)
              RUNNER_Z -= 1
          elif runner_obs.get("ZPos", 0)-RUNNER_Z > 0.5:
              pmap.render(int(SIZE/2-runner_obs.get("ZPos", 0)+1), abs(int(runner_obs.get("XPos", 0))), 0)
              RUNNER_Z += 1
          elif RUNNER_X-runner_obs.get("XPos", 0) < -0.5:
              pmap.render(int(SIZE/2-runner_obs.get("ZPos", 0)+1), abs(int(runner_obs.get("XPos", 0))), 0)
              RUNNER_X += 1
          elif RUNNER_X-runner_obs.get("XPos", 0) > 0.5:
              pmap.render(int(SIZE/2-runner_obs.get("ZPos", 0)+1), abs(int(runner_obs.get("XPos", 0))), 0)
              RUNNER_X -= 1

      if tagger_world_state.number_of_observations_since_last_state > 0:
          tagger_obs = json.loads(tagger_world_state.observations[0].text)
          grid = tagger_obs.get(f"floor3x3", 0)
          if tagger_obs.get("ZPos", 0)-TAGGER_Z < -0.5:
              pmap.render(int(SIZE/2-tagger_obs.get("ZPos", 0)+1), abs(int(tagger_obs.get("XPos", 0))), 1)
              TAGGER_Z -= 1
          elif tagger_obs.get("ZPos", 0)-TAGGER_Z > 0.5:
              pmap.render(int(SIZE/2-tagger_obs.get("ZPos", 0)+1), abs(int(tagger_obs.get("XPos", 0))), 1)
              TAGGER_Z += 1
          elif TAGGER_X-tagger_obs.get("XPos", 0) < -0.5:
              pmap.render(int(SIZE/2-tagger_obs.get("ZPos", 0)+1), abs(int(tagger_obs.get("XPos", 0))), 1)
              TAGGER_X += 1
          elif TAGGER_X-tagger_obs.get("XPos", 0) > 0.5:
              pmap.render(int(SIZE/2-tagger_obs.get("ZPos", 0)+1), abs(int(tagger_obs.get("XPos", 0))), 1)
              TAGGER_X -= 1

      for error in runner_world_state.errors:
          print("Error:",error.text)
      for error in tagger_world_state.errors:
          print("Error:",error.text)

  print("Mission ended")
  # Mission has ended.

if __name__ == "__main__":
    main()
