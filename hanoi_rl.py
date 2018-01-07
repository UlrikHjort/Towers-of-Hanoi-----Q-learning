########################################################################
#                                                                           
#                                                                    
#                Towers of Hanoi - Reinforcement learning                                                           
#                             Hanoi_rl.py                                      
#                                                                           
#                                MAIN                                      
#                                                                           
#                 Copyright (C) 2004 Ulrik Hoerlyk Hjort                   
#                                                                           
#  Towers of Hanoi is free software;  you can  redistribute it                          
#  and/or modify it under terms of the  GNU General Public License          
#  as published  by the Free Software  Foundation;  either version 2,       
#  or (at your option) any later version.                                   
#  Towers of Hanoi is distributed in the hope that it will be                           
#  useful, but WITHOUT ANY WARRANTY;  without even the  implied warranty    
#  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  
#  See the GNU General Public License for  more details.                    
#  You should have  received  a copy of the GNU General                     
#  Public License  distributed with Yolk.  If not, write  to  the  Free     
#  Software Foundation,  51  Franklin  Street,  Fifth  Floor, Boston,       
#  MA 02110 - 1301, USA.                                                    
########################################################################        

import numpy as np
import itertools
import random

###########################################################################################
#
# State : S->[Pa,Pb,Pc] Where value of Px is pin number where disc x is located
#         Index of S is equal to disc number so disc A = 0, B = 1, etc. The index also 
#         give the size of the disk so disk A < B < C ... etc 
#
#
#
#
###########################################################################################



##############################################################################
#
# Class for R matrix
#
##############################################################################
class R:
    ##########################################################################
    #
    #
    #
    ##########################################################################
    def __init__(self,n):
        self.initial = [0] * n # All discs on pin 1
        self.goal = [2] * n    # All discs on pin 3 
        self.goal_reward = 100

        # generate all states for n discs.
        self.states = list(itertools.product(list(range(3)), repeat=n))
        # Generate all transisions
        self.transitions = list(itertools.permutations(list(range(3)), 2))
        self.size = len(self.states)
        self.R = np.ones((self.size,self.size)) * -1

        self.generate()

    ##########################################################################
    #
    # Get new game state from current state and the given transition
    #
    ##########################################################################
    def get_new_state(self,transition, s_from):
        from_pin = transition[0]
        to_pin = transition[1]
        s_to = s_from[:]

        try:
            d_from=s_from.index(from_pin)
            d_to = 10
            if to_pin in s_from:
                d_to=s_from.index(to_pin)
            if d_to > d_from:
                s_to[d_from] = to_pin
            else:
                s_to = None
        except ValueError:
            return None
        else:
            return s_to


    ##########################################################################
    #
    #
    #
    ##########################################################################
    def valid_transition(self,transition, s_from, s_to):
        if s_from == s_to:
            return False
        s_new = self.get_new_state(transition,s_from)
        return s_to == s_new




    ##########################################################################
    #
    #
    #
    ##########################################################################
    def get_transition(self,s_from, s_to, transitions):
        for t in transitions:
            if self.valid_transition(list(t),s_from, s_to):
                return t
        return None


    ##########################################################################
    #
    #
    #
    ##########################################################################
    def transition_sequence(self,transitions, state):
        s = state
        for transition in transitions:
            s = get_new_state(transition, s)




    ##########################################################################
    #
    # Initialize R matrix with valid state transitions
    #
    ##########################################################################
    def generate(self):
        for x in self.states:
            for y in self.states:
                if self.get_transition(list(x), list(y), self.transitions) != None:
                    if list(y) == self.goal:
                        self.R[self.states.index(x), self.states.index(y)] = self.goal_reward
                    else:
                        self.R[self.states.index(x), self.states.index(y)] = 0



    ##########################################################################
    #
    #
    #
    ##########################################################################
    def dump(self):
        print self.R

    ##########################################################################
    #
    #
    #
    ##########################################################################
    def m_size(self):
        return self.size


    ##########################################################################
    #
    # Get next valid state from current state. If more transitions choose one random
    #
    ##########################################################################
    def get_random_next_state(self,current_state):
        states = self.R[:,self.states.index(tuple(current_state)),]
        next_state = random.choice([i for i,x in enumerate(states) if x != -1])
        return next_state

    ##########################################################################
    #
    #
    #
    ##########################################################################
    def get_state_no(self,state):
        return self.states.index(tuple(state))



    ##########################################################################
    #
    #
    #
    ##########################################################################
    def get_state(self,state_no):
        return self.states[state_no]

    ##########################################################################
    #
    #
    #
    ##########################################################################
    def goal_state(self,state_no):
        return (self.states[state_no] == tuple(self.goal)) 


    ##########################################################################
    #
    #
    #
    ##########################################################################
    def get_reward(self,state,action):
        return self.R[state,action]


    ##########################################################################
    #
    #
    #
    ##########################################################################
    def reward_goal(self):
        return self.goal_reward





##############################################################################
#
# Class for Q matrix
#
##############################################################################
class Q:
    ##########################################################################
    #
    #
    #
    ##########################################################################
    def __init__(self,s):
        self.Q = np.zeros((s,s))
        self.Q_old = np.empty_like(self.Q)
        self.size = s
        self.discount_factor = 0.8

    ##########################################################################
    #
    #
    #
    ##########################################################################
    def dump(self):
        print self.Q



    ##########################################################################
    #
    # Q-learning algorithm: 
    #
    # Q(state,action) = R(state,action) * learning_rate + discount_factor + Max[Q(next state, all actions)]
    #
    # (Learning rate is not used here since environment is fully deterministic) 
    #
    ##########################################################################
    def train(self, state, action, r_reward):
        self.Q[state, action] = r_reward + self.discount_factor * max(self.Q[action,:])



    ##########################################################################
    #
    # Generate list with the optimal policy
    #
    ##########################################################################
    def optimal_policy(self, initial_state,r):
        state_list = [initial_state]
        state = r.get_state_no(initial_state)
        
        while True:
            max_val = max(self.Q[state,:])         
            # Get indices for all max Q values in current state row and choose 
            # random action between them
            indices = [i for i, x in enumerate(self.Q[state,:]) if x == max_val]
            state = random.choice(indices)
            state_list.append(r.get_state(state))

            if r.goal_state(state):
                return state_list

            
            
##############################################################################
#
# Class for the tower of Hanoi game
#
##############################################################################
class Hanoi:
    ##########################################################################
    #
    #
    #
    ##########################################################################
    def __init__(self,n):
        self.r = R(n)
        self.q = Q(self.r.m_size())
        self.episodes = 100
        self.initial_state = [0] * n



    ##########################################################################
    #
    # Q-Learning stage. Train and create Q matrix.
    #
    ##########################################################################
    def train(self):
        for j in range(self.episodes):
            st = self.initial_state
            state = self.r.get_state_no(st)

            reward = 0
            while reward < self.r.reward_goal():
                action =  self.r.get_random_next_state(st)

                reward = self.r.get_reward(state,action)
                self.q.train(state, action, reward)

                st = self.r.get_state(action)

                state = self.r.get_state_no(st)




    ##########################################################################
    #
    # Get optimal policy from Q matrix.
    #
    ##########################################################################
    def solution(self):
        print self.q.optimal_policy(self.initial_state, self.r)

h = Hanoi(3)
h.train()
h.solution()
