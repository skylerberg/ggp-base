'''
@author: Skyler Berg
'''

from __future__ import with_statement
from time import time

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


def save_states(state_machine):
    hash = state_machine.getInitialState().hashCode()
    with open("~/ggp_state/game" + str(hash) + ".csv", "a") as out:
        for state in states:
            row= ",".join(state, states[state].count, states[state].total) + "\n"
            out.write(row)


def load_states(state_machine):
    hash = state_machine.getInitialState().hashCode()
    try:
        with open("~/ggp_state/game" + str(hash) + ".csv") as state_file:
            global states
            for row in state_file:
                state_hash, count, total = map(int, row.split(","))
                state = KnownState()
                state.count = count
                state.total = total
                states[state_hash] = state
    except IOError:
        pass


class CustomPythonGamer(StateMachineGamer):

    def getName(self):
        return "Skyler's Gamer"

    def stateMachineMetaGame(self, timeout):
        load_states(self.getStateMachine())

    def stateMachineSelectMove(self, timeout):
        current_state = self.getCurrentState()
        print time(), timeout / 1000.0, time() < (timeout / 1000.0) - 1
        while time() < (timeout / 1000.0) - 1:
            self._depth_charge(current_state)
        chance_to_win, selection = self._select_move(current_state)
        print chance_to_win, selection
        print "There are %d states seen so far" % len(states)
        return selection

    def stateMachineStop(self):
        #save_states(self.getStateMachine())
        pass

    def stateMachineAbort(self):
        #save_states(self.getStateMachine())
        pass

    def getInitialStateMachine(self):
        return ProverStateMachine()

    def _select_move(self, current_state):
        """ Returns a chance to win and the move """
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
            result = self.getStateMachine().getGoal(current_state, self.getRole())
        else:
            next_state = self.getStateMachine().getRandomNextState(current_state)
            result = self._depth_charge(next_state)
        states[hash].count += 1
        states[hash].total += result
        return result
