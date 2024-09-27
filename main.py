from collections import deque
from functools import reduce
from itertools import accumulate
from typing import Generator, Iterable, Literal

from data import N


Direction = Literal[-1, 0, 1]
TuringTransition = tuple[str, Direction, str]
TuringTransitionTable = dict[str, dict[str, tuple[str, Direction, str]]]
DFATransitionTable = dict[str, dict[str, str]]


def walk_dfa(string: str, transitions: DFATransitionTable, start: str) -> Iterable[str]:
    """Walks through the steps of computation for a DFA
    when given an input string and transitions.
    """
    return accumulate(string, lambda x, y: transitions[x][y], initial=start)


def execute_dfa(string: str, transitions: DFATransitionTable, start: str) -> str:
    """Takes an input string and returns the final state
    when given the starting state and transitions.
    """
    return reduce(lambda x, y: transitions[x][y], string, start)


def walk_turing(
    string: str, transitions: TuringTransitionTable, start: str, final_states: set[str]
) -> Generator[tuple[str, TuringTransition], None, tuple[deque[str], str]]:
    """Traces the steps and execution of a turing machine. This is
    implemented as an iterator because it is entirely possible
    that the turing machine itself doesn't halt when given an
    input string.
    """
    tape = deque(string) if string else deque()
    i, state = 0, start
    while state not in final_states:
        if not tape:
            yield "", ("", N, "")
            break
        read_symbol = tape[i]
        write_symbol, direction, next_state = transitions[state][read_symbol]
        yield read_symbol, (write_symbol, direction, next_state)
        tape[i] = write_symbol
        i += direction
        if i == len(tape):
            tape.append(" ")
        elif i == -1:
            tape.appendleft(" ")
            i = 0
        state = next_state
    return tape, state


def execute_turing(
    string: str, transitions: TuringTransitionTable, start: str, final_states: set[str]
) -> tuple[deque[str], str]:
    """Executes instructions on a turing machine when given
    a string/input tape, transition table, starting state,
    and set of states to halt on.

    Returns a two-tuple containing the symbols written on the tape
    as well as the final state that the machine has halted on.
    """
    tape = deque(string) if string else deque()  # Handle the empty string.
    i, state = 0, start
    while state not in final_states and tape:
        read_symbol = tape[i]
        write_symbol, direction, next_state = transitions[state][read_symbol]
        tape[i] = write_symbol
        i += direction
        if i == len(tape):
            tape.append(" ")
        elif i == -1:
            tape.appendleft(" ")
            i = 0
        state = next_state
    return tape, state
