'''
@author: Skyler Berg
'''

import random

from org.ggp.base.util.statemachine import MachineState
from org.ggp.base.util.statemachine.implementation.prover import ProverStateMachine
from org.ggp.base.player.gamer.statemachine import StateMachineGamer


class CustomPythonGamer(StateMachineGamer):

    def getName(self):
        return "Skyler's Gamer"

    def stateMachineMetaGame(self, timeout):
        pass

    def stateMachineSelectMove(self, timeout):
        print timeout
        chance_to_win, selection = self._select_move(self.getCurrentState())
        print chance_to_win, selection
        #moves = self.getStateMachine().getLegalMoves(self.getCurrentState(), self.getRole())
        #selection = random.choice(moves)
        return selection

    def stateMachineStop(self):
        pass

    def stateMachineAbort(self):
        pass

    def getInitialStateMachine(self):
        return ProverStateMachine()

    def _select_move(self, current_state):
        """ Returns a chance to win and the move """
        if self.getStateMachine().isTerminal(current_state):
            return self.getStateMachine().getGoal(current_state, self.getRole()), None
        state_map = self.getStateMachine().getNextStates(current_state, self.getRole())
        moves = list(state_map.keySet().iterator())
        results = {}  # Maps moves to tuple (chance_to_win)
        for move in moves:
            for i in xrange(100):
                next_state = random.choice(state_map.get(move))
                result = self._depth_charge(next_state)
                results[move] = results.get(move, 0) + result
            print move, results[move]
        score, move = max((score, move) for (move, score) in results.iteritems())
        return score, move

    def _depth_charge(self, current_state):
        if self.getStateMachine().isTerminal(current_state):
            return self.getStateMachine().getGoal(current_state, self.getRole())
        state_map = self.getStateMachine().getNextStates(current_state, self.getRole())
        moves = list(state_map.keySet().iterator())
        random_move = random.choice(moves)
        next_state = random.choice(state_map.get(random_move))
        return self._depth_charge(next_state)
