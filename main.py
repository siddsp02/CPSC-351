from copy import deepcopy
from dataclasses import dataclass, field
from functools import reduce
from itertools import accumulate, chain, islice, repeat, starmap, tee
from typing import Any, Generator, Iterable, Iterator, Literal

from data import anbn, dfa

Direction = Literal[-1, 0, 1]
TuringTransition = tuple[str, Direction, str]
TuringTransitionTable = dict[str, dict[str, tuple[str, Direction, str]]]
DFATransitionTable = dict[str, dict[str, str]]


def partition(it: Iterable[Any], i: int) -> tuple[Iterable[Any], Iterable[Any]]:
    "Partition an iterable at an index `i`."
    it1, it2 = tee(deepcopy(it))
    return islice(it1, 0, i, 1), islice(it2, i, None, 1)


def to_tm_string(it: Iterable[str]) -> str:
    ret = "".join(it)
    ret = ret if ret else "⊔"
    return ret


def walk_dfa(string: str, transitions: DFATransitionTable, start: str) -> Iterator[str]:
    """Walks through the steps of computation for a DFA
    when given an input string and transitions.
    """
    return accumulate(string, lambda x, y: transitions[x][y], initial=start)


def execute_dfa(string: str, transitions: DFATransitionTable, start: str) -> str:
    """Takes an input string and returns the final state
    when given the starting state and transitions.
    """
    return reduce(lambda x, y: transitions[x][y], string, start)


@dataclass
class DFA:
    alphabet: set[str]
    transitions: DFATransitionTable
    accepting_states: set[str]
    start: str
    states: set[str] = field(init=False)

    def __post_init__(self) -> None:
        self.states = set(self.transitions)

    def walk(self, string: str) -> Iterator[str]:
        return walk_dfa(string, self.transitions, self.start)

    def execute(self, string: str) -> str:
        return execute_dfa(string, self.transitions, self.start)


class Tape:
    """Class for the tape of a Turing machine. Since the tape is infinite,
    indices have to be a non-negative integer since negative indexing
    wouldn't make sense in this case.
    """

    def __init__(self, string: str = "") -> None:
        self.cursor = 0
        self.cells = list(to_tm_string(string))

    @property
    def cursor(self) -> int:
        return self._cursor

    @cursor.setter
    def cursor(self, i: int) -> None:
        self._cursor = max(0, i)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.cells})"

    def peek(self) -> str:
        return self[self.cursor]

    def shift(self, direction: Direction) -> None:
        if direction not in {-1, 0, 1}:
            raise ValueError(f"direction can only be -1, 0, or 1, and not {direction}.")
        self.cursor += direction

    def mark(self, symbol: str) -> None:
        if len(symbol) != 1:
            raise ValueError("Can only mark one character at a time.")
        self[self.cursor] = symbol

    def write(self, symbol: str, shift: Direction = 1) -> None:
        self.mark(symbol)
        self.shift(shift)

    def __str__(self) -> str:
        return "".join(self.cells) + "..."

    def __setitem__(self, i: int, v: str) -> None:
        if i < 0:
            raise IndexError("Tape index can only be positive.")
        if i >= len(self.cells):
            self.cells.extend("⊔" * (len(self.cells) + 1 - i))
        self.cells[i] = v

    def __getitem__(self, i: int) -> str:
        if i < 0:
            raise IndexError("Tape index can only be positive.")
        if i >= len(self.cells):
            return "⊔"
        return self.cells[i]

    def __iter__(self) -> Iterator[str]:
        "Iterates through the contents of the tape cells. Note that this is an infinite iterator."
        return chain(self.cells, repeat("⊔"))

    def iter_cells(self) -> Iterator[str]:
        "Iterates only through the actual written cells of the tape."
        return iter(self.cells)


@dataclass
class TuringMachine:
    rejecting_states: set[str]
    accepting_states: set[str]
    tape_alphabet: set[str]
    input_alphabet: set[str]
    transitions: TuringTransitionTable
    start_state: str
    tape: Tape = field(init=False, default_factory=Tape)

    def __post_init__(self) -> None:
        if not self.tape_alphabet >= self.input_alphabet | {"⊔"}:
            raise ValueError("Tape alphabet must include the blank symbol.")

    @property
    def head(self) -> int:
        return self.tape.cursor

    @property
    def halting_states(self) -> set[str]:
        return self.accepting_states | self.rejecting_states

    def walk(
        self, string: str
    ) -> Generator[tuple[str, TuringTransition], None, tuple[Tape, str]]:
        """Traces the steps and execution of a turing machine. This is
        implemented as an iterator because it is entirely possible
        that the turing machine itself doesn't halt when given an
        input string.
        """
        self.tape = Tape(string)
        state = self.start_state

        while True:
            read_symbol = self.tape.peek()
            write_symbol, direction, next_state = self.transitions[state][read_symbol]

            yield read_symbol, (write_symbol, direction, next_state)

            self.tape.write(write_symbol, direction)
            if state in self.halting_states:
                break

            state = next_state

        tape, self.tape = self.tape, Tape()
        return tape, state

    def execute(self, string: str) -> Tape:
        "Executes the Turing machine on an input string, and returns the result."
        steps = self.walk(string)
        while True:
            try:
                next(steps)
            except StopIteration as e:
                return e.value

    def accepts(self, string: str) -> bool:
        _, state = self.execute(string)
        return state in self.accepting_states

    def rejects(self, string: str) -> bool:
        _, state = self.execute(string)
        return state in self.rejecting_states

    def get_state_configurations(self, string: str) -> Iterator[tuple[str, str, str]]:
        """Iterates over the state configurations of the Turing machine
        when it's given an input string/tape to process.
        """
        state = self.start_state
        for step in self.walk(string):
            _, (*_, next_state) = step

            left, right = partition(self.tape.iter_cells(), self.head)

            left = to_tm_string(left)
            right = to_tm_string(right)

            yield left, state, right

            state = next_state

    def print_configurations(self, string: str, /, fmt: str = "{!r} {} {!r}") -> None:
        """Prints the sequence of Turing machine configurations when the instance
        runs on a given input string.
        """
        print(" ⊢ ".join(starmap(fmt.format, self.get_state_configurations(string))))


def main() -> None:
    # An example of a Turing machine that checks for membership
    # in a non-regular language.
    tm = TuringMachine(
        rejecting_states={"qr"},
        accepting_states={"qa"},
        tape_alphabet={"a", "b", "X", "Y", "⊔"},
        input_alphabet={"a", "b"},
        transitions=anbn,  # type: ignore
        start_state="q0",
    )
    print(tm.accepts("aaaababb"))


if __name__ == "__main__":
    main()
