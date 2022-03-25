import random, stringcolor as color
from enum import Enum

class LetterStatus(Enum):
    UNGUESSED = 1
    INCORRECT = 2
    MISPLACED = 3
    CORRECT = 4

class WordleLetter:
    def __init__(self, letter, status):
        self.letter = letter
        self.status = status

    def display(self):
        print(color.cs(self.letter.upper(), self._get_color()), end="")
    
    def _get_color(self):
        if self.status == LetterStatus.CORRECT:
            return "GREEN"
        elif self.status == LetterStatus.INCORRECT:
            return "GRAY"
        elif self.status == LetterStatus.MISPLACED:
            return "YELLOW"
        elif self.status == LetterStatus.UNGUESSED:
            return "WHITE"

class Wordle:
    def __init__(self):
        self.words = open('words.txt',"r").read().split()

    def play(self):
        secret_word = random.choice(self.words)
        
        rounds = 0
        guesses = []
        while (rounds < 6):
            guesses += self._play_round(secret_word)
            rounds += 1
            self._print_guesses(guesses)
            if self._all_correct(guesses[-5:]):
                print(color.cs("You win!\n", "GREEN"))
                break
            
        if rounds >= 6:
            print(color.cs("You lose!\n", "RED"))
        print("Word was:")
        for l in secret_word:
            WordleLetter(l, LetterStatus.CORRECT).display()
        print()

    def _play_round(self, secret_word):
        guess = input(">").lower()
        while guess not in self.words:
            guess = input("Invalid Word\n>").lower()
        guess_letters = []
        for i in range(len(guess)):
            letter = guess[i]
            status = self._check(letter, i, secret_word)
            guess_letters.append(WordleLetter(letter, status))
        return guess_letters

    def _check(self, letter, i, secret_word):
        if letter not in secret_word:
            return LetterStatus.INCORRECT
        elif secret_word[i] == letter:
            return LetterStatus.CORRECT
        else:
            return LetterStatus.MISPLACED
    
    def _print_guesses(self, guess_letters):
        print()
        for i in range(len(guess_letters)):
            guess_letters[i].display()
            if (i+1) % 5 == 0:
                print()
        print()

    def _all_correct(self, guesses):
        for i in range(len(guesses)):
            if guesses[i].status != LetterStatus.CORRECT:
                return False
        return True

Wordle().play()