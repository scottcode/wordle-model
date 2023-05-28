"""Implementation of a wordle-like game"""

import enum
from dataclasses import dataclass
from typing import Sequence, Iterable


class Color(enum.Enum):
    green = '✅'
    yellow = '🤨'
    grey = '❌'


class Feedback:
    def __init__(self, colorseq: Sequence[Color]) -> None:
        self.colorseq = colorseq

    def is_correct(self):
        return all(item == Color.green for item in self.colorseq)

    def __repr__(self) -> str:
        return repr(self.colorseq)


@dataclass
class Attempt:
    guess: Iterable
    feedback: Sequence[Color]

    def is_correct(self):
        return all(item == Color.green for item in self.feedback)

    def pairs(self):
        return tuple(zip(self.guess, self.feedback))

    def __repr__(self) -> str:
        return str([
            (char, result.value)
            for char, result in self.pairs()
        ])


def give_feedback(guess, actual) -> Attempt:
    if not len(guess) == len(actual):
        raise ValueError
    unseen = set(actual)
    colors = []
    for i in range(len(guess)):
        if guess[i] == actual[i]:
            colors.append(Color.green)
        elif guess[i] in unseen:
            unseen.remove(guess[i])
            colors.append(Color.yellow)
        else:
            colors.append(Color.grey)
    return Attempt(guess, colors)


class Game:
    def __init__(self, word: str):
        self.word = word
        self.attempts = []

    def guess_word(self, guess: str) -> Attempt:
        attempt = give_feedback(guess=guess, actual=self.word)
        self.attempts.append(attempt)
        if attempt.is_correct():
            print(f"Congrats! The word was {guess}")
        return attempt

    @property
    def n_attempts(self):
        return len(self.attempts)


if __name__ == '__main__':
    game = Game('helps')
    print(game.guess_word('smile'))
    print(game.guess_word('tells'))
