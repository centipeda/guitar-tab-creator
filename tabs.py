# Lets you create, edit, store, and view tablature for guitar.

import curses

# TODO
# Implement tab display functions
# Implement tab storage functions
# Implement tab editing functions

# Sample:
# e|-----------------------------|
# B|-----------------------------|
# G|-------12----12h14-----------|
# D|-12h14----14-----------------|
# A|-----------------------------|
# E|-----------------------------|

def main():
    smooth = Tab(Note((12,14),4,command="h"),
                 Note((12,),3),
                 Note((14,),3)
                 Note((12,14),3,command="h"))


class Tab:
    """Stores a guitar tab as a series of Note and Chord objects."""
    def __init__(self,
                tune,
                tuning=("E","A","D","G","B","e"),
                line_length = 40):
        self.tuning = tuning
        self.lineLength = line_length
        self.tune = tune
        strings = {tuning[0] :
        }

    def __str__(self):
        final = ""
        for note in self.tune:
            if type(note) == Note:

            elif type(note) == Chord:

class Note:
    """Represents a single note as a fret and string number, with
    optional special command.
    Fret: tuple containing ints
    String: int from 1 to 6
    command: see command listing"""
    def __init__(self, fret, string, command=None):
        self.fret = fret
        self.string = string
        self.note = str(fret[0])
        if command is not None:
            self.command = command
            self._process_command()

    def _process_command(self):
        if self.command in ["~","b"]:
            self.note = str(self.fret) + self.command
        elif self.command in ["/","\\","h","p"]:
            self.note = "".join([self.fret[0],self.command,self.fret[1]])

class Chord:
    """Represents a chord as a set of fret numbers.
    chord: set of 6 ints, "x" characters. A string not played
    is represented as None.
    ex: c chord: (None, 3, 2, 0, 1, 0)"""
    def __init__(self, chord, blank_char="-"):
        self.chord = chord
        self.blankCharacter = blank_char

    def get_notes(self):
        notes = []
        for note in self.chord:
            if note is None:
                notes.append(self.blankCharacter)
            else:
                notes.append(str(note))
