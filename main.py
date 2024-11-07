from dataclasses import dataclass, field
from functools import reduce
from itertools import accumulate, chain, islice, repeat
from typing import Generator, Iterable, Iterator, Literal

from data import anbn

Direction = Literal[-1, 0, 1]
TuringTransition = tuple[str, Direction, str]
TuringTransitionTable = dict[str, dict[str, tuple[str, Direction, str]]]
DFATransitionTable = dict[str, dict[str, str]]


class Tape:
    """Class for the tape of a Turing machine. Since the tape is infinite,
    indices have to be a non-negative integer since negative indexing
    wouldn't make sense in this case.
    """

    def __init__(self, string: str = "") -> None:
        self.cells = ["⊔"] if not string else list(string)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.cells})"

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
        yield from chain(self.cells, repeat("⊔"))


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
        if not self.tape_alphabet | {"⊔"} <= self.input_alphabet:
            raise ValueError("Tape alphabet must include the blank symbol.")

    def walk(
        self, string: str
    ) -> Generator[tuple[str, TuringTransition], None, tuple[Tape, str]]:
        """Traces the steps and execution of a turing machine. This is
        implemented as an iterator because it is entirely possible
        that the turing machine itself doesn't halt when given an
        input string.
        """
        self.tape = Tape(string)
        i, state = 0, self.start_state
        halting_states = self.accepting_states | self.rejecting_states

        while state not in halting_states:
            read_symbol = self.tape[i]
            write_symbol, direction, next_state = self.transitions[state][read_symbol]
            yield read_symbol, (write_symbol, direction, next_state)
            self.tape[i] = write_symbol
            # If transition direction reads left and tape head
            # is at the leftmost cell, stay.
            i = max(i + direction, 0)
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

    def print_configurations(self, string: str, skip_reads: bool = False) -> None:
        """Prints the sequence of Turing machine configurations when the instance
        runs on a given input string.
        """
        i = 0
        state = self.start_state
        for step in self.walk(string):
            read_symbol, (write_symbol, direction, next_state) = step
            left = "".join(x for x in islice(self.tape, 0, i, 1))
            it = islice(self.tape, i, None, 1)

            # Skip instructions/configurations where cells effectively aren't
            # changed, and the tape head just moves one cell to the left/right.
            if skip_reads:
                if read_symbol == write_symbol:
                    continue

            print(
                (left if left else "⊔"),
                f" {state} ",
                "".join(x for x in iter(lambda: next(it), "⊔")) + "⊔",
                end="",
                sep="",
            )
            if state not in self.accepting_states | self.rejecting_states:
                print(" ⊢", end=" ")

            state = next_state
            i += direction
        print()


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
    tm.print_configurations("aaabbb", skip_reads=True)


if __name__ == "__main__":
    main()
