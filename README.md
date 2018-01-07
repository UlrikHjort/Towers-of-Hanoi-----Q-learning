Reinforcement Q-learning algoeithm for solving the Towers of Hanoi problem.



The following nomenclature is used for state representation:  
State : S->[Pa,Pb,Pc] Where value of Px is pin number where 
disc x is located Index of S is equal to disc number so disc A = 0, B = 1, etc. 
The index also give the size of the disk so disk A < B < C ... etc 




Usage:
	Instantiate the Hanoi class with number of discs as parameter.
	Train the system by calling the train method.
	Get solutions/policies by calling the solution method.

	Number of episodes (self.episodes) for the training can be adjusted in the constructor of the Hanoi class.

	Discount factor (self.discount) can be set in the the constructor of the Q class	

Example of training the system with 2 discs:

Q matrix converged to its optimal valueafter 300 episodes:
[[   0.     0.     0.    64.     0.     0.    51.2    0.     0. ]

 [   0.     0.    80.     0.    51.2    0.     0.    51.2    0. ]

 [   0.    64.     0.     0.     0.    80.     0.     0.   100. ]

 [  51.2    0.     0.     0.     0.    80.    51.2    0.     0. ]

 [   0.    64.     0.     0.     0.     0.     0.    51.2    0. ]

 [   0.     0.    80.    64.     0.     0.     0.     0.   100. ]

 [  51.2    0.     0.    64.     0.     0.     0.    51.2    0. ]

 [   0.    64.     0.     0.    51.2    0.    51.2    0.     0. ]

 [   0.     0.     0.     0.     0.     0.     0.     0.     0. ]]



Optimal policity after 300 episodes:
[[0, 0], (1, 0), (1, 2), (2, 2)]



Reference for basic RL concepts:
Sutton, Richard S.; Barto, Andrew G. (1998). Reinforcement Learning: An Introduction. MIT Press. ISBN 0-262-19398-1.