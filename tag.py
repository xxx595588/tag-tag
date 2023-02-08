from builtins import range
import MalmoPython
import os
import sys
import time
import numpy as np

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

def playground(x, y, z, blocktype):
    pg_str = ""
    # length of the playground
    size = 30

    # density of obstacles
    d = 0.05

    # back fence
    pg_str += '<DrawLine x1="' + str(x+1) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x+1) + '" y2="'+ str(y) +'" z2="' + str(z+int(size/2)) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x+1) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x+1) + '" y2="'+ str(y) +'" z2="' + str(z-int(size/2)) + '" type="' + blocktype + '"/>\n'

    # front fence
    pg_str += '<DrawLine x1="' + str(x-size) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x-size) + '" y2="'+ str(y) +'" z2="' + str(z+int(size/2)) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-size) + '" y1="' + str(y) + '" z1="' + str(z) + '" x2="' + str(x-size) + '" y2="'+ str(y) +'" z2="' + str(z-int(size/2)) + '" type="' + blocktype + '"/>\n'

    # side fence
    pg_str += '<DrawLine x1="' + str(x-size) + '" y1="' + str(y) + '" z1="' + str(z+int(size/2)) + '" x2="' + str(x+1) + '" y2="'+ str(y) +'" z2="' + str(z+int(size/2)) + '" type="' + blocktype + '"/>\n'
    pg_str += '<DrawLine x1="' + str(x-size) + '" y1="' + str(y) + '" z1="' + str(z-int(size/2)) + '" x2="' + str(x+1) + '" y2="'+ str(y) +'" z2="' + str(z-int(size/2)) + '" type="' + blocktype + '"/>\n'

    # randomly place obstacles
    obs = np.zeros(((size - 3)**2,), dtype = np.int8)
    obs[np.random.choice((size - 3)**2, replace = False, size = int(((size - 3)**2)*d) )] = 1
    obs = np.reshape(obs, (size - 3, size - 3))
  
    x = -(size - 2)
    z = -(int(size / 2) - 2)

    for i, j in zip(np.where(obs == 1)[1], np.where(obs == 1)[0]):
        pg_str += '<DrawLine x1="' + str(x+i) + '" y1="' + str(y) + '" z1="' + str(z+j) + '" x2="' + str(x+i) + '" y2="' + str(y+1) + '" z2="' + str(z+j) + '" type="bedrock"/>\n'
            
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
                  ''' + playground(0, 2, 0, "fence") + '''
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="3000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>Runner</Name>
                <AgentStart>
                  <Placement x="0" y="2" z="0" yaw="90"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print("Mission running ", end=' ')

# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print("Mission ended")
# Mission has ended.