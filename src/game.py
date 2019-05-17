import numpy as np
from numpy import random
import scipy.stats
import sys
sys.path.append('../')

import pynfg

NEW_NODE_PROBS = {'chance' : 0.2,
                  'deter' : 0.3,
                  'decis': 0.5}

NUM_NODES_PROBS = {1: 0.5,
                   2: 0.25,
                   3: 0.125,
                   4: 0.125}

NUM_DECIS_PROBS = {2: 0.5,
                   3: 0.25,
                   4: 0.25}

# the state vector that is modified by deterministic nodes is of
# the form [a_1, a_2, ..., a_N] where a_k is in the discrete interval [0, M]
STATE_SIZE = [5, 5]


def rand_select_dictval(d):
    rv = np.random.random()
    smallest = 1.0
    rkey = None

    for key, value in d.items():
        if value < smallest and value < rv:
            smallest = value
            rkey = key

    return rkey

class RACG(object):
    '''
    Random AFEG Class Game

    A randomly constructed asymetrical, imperfect information
    network form game implemented in pynfg.
    '''

    def __init__(self, _depth=5):
        rparams = {'tmp': 0}
        self.root_node = pynfg.DeterNode('root', lambda x: 1, rparams, False, [1], 'root node', 0, 'root_null')
        self.state_v = np.random.randint(STATE_SIZE[0], size=STATE_SIZE[1])
        self.depth = _depth

        self.__add_rand_node(self.root_node, 0, [0,0,0])    # Set up nodes

        # Define reward functions
        # p1r = lambda 

    def __add_rand_node(self, parent, _depth, state):
        '''Pick a node type to add to a parent and add it. Recursively add nodes until desired depth'''
        type_key = rand_select_dictval(NEW_NODE_PROBS)
        node = None

        if type_key == 'deter':
            node = pynfg.DeterNode('deter_' + str(depth),
                                   self.state_v, 
                                   False,
                                   rangearand_select_dictval(NUM_DECIS_PROBS),
                                   'deter node at depth ' + str(depth),
                                   _depth,
                                   parent)

        elif type_key == 'rand':
            _distip = (scipy.stats.boltzmann, [np.random.random() * 5, rand_select_dictval(NUM_DECIS_PROBS)])
            node = pynfg.ChanceNode('chance_' + str(depth),
                                    distip = _distip,
                                    descrption='chance node at depth ' + str(_depth))
        elif type_key == 'decis':
            node = pynfg.DecisionNode('decis_' + str(_depth),
                                      player=str(int(np.random() > 0.5)),
                                      space=range(rand_select_dictval(NUM_DECIS_PROBS)),
                                      parents=parent,
                                      description='decision node at depth ' + str(_depth))
        if _depth < self.depth:
            self.__add_rand_node([node], _depth + 1, state)