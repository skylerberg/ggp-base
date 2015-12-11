'''
@author: Skyler Berg
'''

import random
import signal
from contextlib import contextmanager

#from org.ggp.base.util.statemachine import MachineState
from org.ggp.base.util.statemachine.implementation.prover import ProverStateMachine
from org.ggp.base.player.gamer.statemachine import StateMachineGamer


class KnownState(object):

    def __init__(self):
        self.count = 0
        self.total = 0
        # TODO factor in roles

    def score(self):
        try:
            return self.total / self.count
        except ZeroDivisionError:
            return 0

    def __repr__(self):
        return "<KnownState count={}, total={}" % (self.count, self.total)


states = {}


class CustomPythonGamer(StateMachineGamer):

    def getName(self):
        return "Skyler's Gamer"

    def stateMachineMetaGame(self, timeout):
        pass

    def stateMachineSelectMove(self, timeout):
        print timeout
        current_state = self.getCurrentState()
        while True:
            self._depth_charge(current_state)
        chance_to_win, selection = self._select_move(current_state)
        print chance_to_win, selection
        print "There are %d states seen so far" % len(states)
        return selection

    def stateMachineStop(self):
        pass

    def stateMachineAbort(self):
        pass

    def getInitialStateMachine(self):
        return ProverStateMachine()

    def _select_move(self, current_state):
        """ Returns a chance to win and the move """
        #if self.getStateMachine().isTerminal(current_state):
            #return self.getStateMachine().getGoal(current_state, self.getRole()), None
        state_map = self.getStateMachine().getNextStates(current_state, self.getRole())
        moves = list(state_map.keySet().iterator())
        scores = {}
        for move in moves:
            scores_for_move = []
            for state in state_map.get(move):
                hash = state.hashCode()
                if hash in states:
                    scores_for_move.append(states[hash].score())
            scores[move] = min(scores_for_move)
        for move, score in scores.iteritems():
            print move, score
        return max((score, move) for (move, score) in scores.iteritems())

    def _depth_charge(self, current_state):
        hash = current_state.hashCode()
        if hash not in states:
            states[hash] = KnownState()
        if self.getStateMachine().isTerminal(current_state):
            return self.getStateMachine().getGoal(current_state, self.getRole())
        state_map = self.getStateMachine().getNextStates(current_state, self.getRole())
        moves = list(state_map.keySet().iterator())
        random_move = random.choice(moves)
        next_state = random.choice(state_map.get(random_move))
        result = self._depth_charge(next_state)
        states[hash].count += 1
        states[hash].total += result
        return result
