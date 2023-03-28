# tag-tag


## Project Summary

&emsp;&emsp;Our project is based on an implementation of a tag game. It involves the programming of two Artificial Intelligence: the runner and the tagger. The tagger is programmed with logic that allows it to approach and try to tag the runner. Additionally, the tagger may attempt to further predict the runner’s next action and involve it as a factor in the tagger’s action determination. The runner is programmed with machine learning algorithms that allow it to gradually learn how to survive longer - avoid being tagged by the tagger.

&emsp;&emsp;The goal of our project is to implement the semantics stated above. In this semantics, the performance of the tagger is supposed to be constant because the tagger does not possess any learning capability. The performance of the runner is supposed to vary based on the effectiveness of the machine-learning algorithm. With these premises in mind, the quality of our project can be determined by assessing the growth of the runner’s survival time after a certain amount of game iterations. Thus, the major focus of our project is to implement and continuously improve the runner’s backend machine-learning algorithm, so that the runner’s survival time can be improved as we train the runner through game iterations.
  
##  Approaches
&emsp;&emsp;To summarize the approach, our project is composed of a runner and tagger component, and we're utilizing `tabular q-learning with epsilon greedy exploration` for the runner as our reinforcement learning algorithm. The q table would be updated by the following equation:
  
<br />

$$Q(s,a) = Q(s,a) + \alpha * (reward + \gamma * maxQ(s',a) - Q(s,a)), \space \epsilon = 0.05, \space \alpha = 0.3, \space \gamma = 1$$

<br />

&emsp;&emsp;The runner redward function was defined as the displacement of post-action & pre-action distance from runner to tagger. It was defined as:

```
if caught:
	reward = -5000
else if surrounded:
	if  Δdis > 0  and  dis_post_action >=3: 
		reward = 50 ⋅ dis_pre_action
	else:
		reward = 1000 ⋅ Δdis/dis_pre_action
else if Δdis > 0:
 	reward = 50 ⋅ Δdis ⋅ dis_pre_action
else if  Δdis < 0:
  	reward = 1000 ⋅ Δdis/dis_pre_action 
else:
  	reward = -2000
```
<br />

  The state is determined by the coordinate combination of both the runner and tagger, and we have four possible actions - `movenorth`, `movesouth`, `moveeast`, and `movewest` - available for each state. For n*n map, we would have n4 states and four actions per state.
The state in q table looks like:

<div align="center">
	
| runner      | tagger      | movesouth   | moveeast    | movenorth  | movewest    |
| ----------- | ----------- | ----------- | ----------- |----------- | ----------- |
| (0, 0)      | (0, 1)      | 0           | 0           | 199.56     | -250.87     |
| (0, 1)      | (1, 2)      | 0           | 215.31      | -518.44    | -485.42     |
	
</div>

<br />

  For runner setup, we applied `A* search` to guarantee the shortest path from tagger to runner, the cost of one grid is defined by following equation:
  

$$f(n) = g(n) + h(n)$$

$$g(n) represents the cost from start point to current point$$

$$h(n)  represents the heuristic cost at point n, h(n)actual distance from n to end point$$


## Pros & Cons:

### Advantages:
- Every combination of states is precisely defined in our Q-table, so there exist corresponding values for each state.
- The tagger can do the prediction of the runner. Therefore, as the performance of tagger grows as well as the runner’s.
- The runner’s survival time will keep increasing since it takes the advantage of epsilon greedy exploration throughout the training process.
- The runner will not only keep the distance from the tagger, but also will escape from the deadend.
- The shortest path is guaranteed to be found in tagger agent.

### Disadvantages:
- According to our definition of state, the memory requirement grows as the increasement of the map.
- The waste of memory would be expected in our Q-table, because not every state & actions would be explored during the training process.
- Base on the prediction functionality in tagger agent, it will require two addition optimal A* searches for each prediction .
- The runner is trained by a given map (map based). Namely, the runner needs to be re-trained if a new map was given.


## Evaluation
&emsp;&emsp;The main focus of our project is to implement, tune, and continuously improve the runner’s backend machine learning algorithm so that the runner’s survival time can be increased as we train the runner through many game iterations. To evaluate our tag game project, we designed a series of experiments that would test the effectiveness of our machine learning algorithms. Essentially, the growth in the runner’s survival time will be monitored as an indicator of our project’s achievement. The longer time the runner survives, the more effective our algorithm will be, and vice versa. We evaluated the project using both quantitative and qualitative metrics. 

### Quantitative evaluation: 
&emsp;&emsp;For the `quantitative evaluation`, we measured the survival time of the runner before being tagged by the tagger. We ran multiple iterations of the game in our initial AI program as well as our final AI program. At the same time, we collected the runner’s survival time for each iteration and model to plot two linear graphs to visualize how the survival time changed throughout the iteration in each model. 

&emsp;&emsp;Below are the two plots to visualize of two models’ performances:

<p align="center">
  <img src="https://user-images.githubusercontent.com/61955371/228103296-d9aae59e-f4dd-490d-af86-469ef58c8e50.png">
</p>
                                                                             
&emsp;&emsp;By comparing those two linear graphs, we can find that after any amount of iterations the runner's survival time in our enhanced AI model is much larger than the survival time in the initial AI model. The maximum survival time in the initial model is around 0.35 second, but the survival time gets improved to more than 50 seconds in the enhanced AI model.

&emsp;&emsp;Additionally, in the enhanced AI model the survival time maintains an increased trend in the survival time. However, survival time in the initial model fluctuates rapidly after 10 iterations. From this perspective, the enhanced AI’s ability to learn and improve from its previous experiences is stronger and this resulted in a remarkable increase in performance with each learning cycle.



### Qualitative evaluation: 
&emsp;&emsp;For the `qualitative evaluation`, we introduced three participants to play our game. The participants played the game with the tagger(which can predict the next move of the player) and provided feedback on their experience. The participants found the game to be more challenging than they thought and also enjoyable. They also appreciated the clear user interface with the character's name displayed above their respective header, allowing players to quickly identify and differentiate between those two characters in the game.

&emsp;&emsp;In addition, the runner's training quality can be guaranteed even if the tag game is trained in different environments/maps. To achieve this effect, we made sure that the tagger always makes its best decision in an attempt to catch the runner by adopting the A* search algorithm which always finds the shortest path to the runner (the reward was defined as the displacement of pre-action and post-action between the tagger and the runner). This minimizes the effect of the tagger's action on the training result because the tagger always makes its best decision, so it becomes a control value to the training process. While the tagger is a control value, and the map is another control value(because it does not change throughout the training process), the runner's backend machine learning algorithm becomes the only variable in each independent complete training. With these premises in effect, we can guarantee the training quality in every map is similar and solely dependent on the runner's backend. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/61955371/228103374-a43604e6-3e4a-4710-94c8-51548ec2644e.png">
</p>

&emsp;&emsp;To validify our effort in ensuring a consistent training quality map-wise, we have conducted two trainings A and B on different maps. As we can see above, the survival time grew proportionally with the iteration of both training A and B. Therefore, we can conclude that the quality of our project is guaranteed with crucial training standards and map-wise performance consistency.
