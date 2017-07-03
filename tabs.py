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
    smooth = Tab((Note((12,14),4,command="h"),
                 Note((12,),3),
                 Note((14,),4),
                 Note((12,14),3,command="h")),
                 "Smooth")

    print(smooth)


class Tab:
    """Stores a guitar tab as a series of Note and Chord objects."""
    def __init__(self,
                tune,
                name,
                tuning=("E","A","D","G","B","e"),
                line_length = 60):
        self.tuning = tuning
        self.lineLength = line_length
        self.tune = tune
        self.name = name

    def __str__(self):
        return self.display_tab()

    def display_tab(self):
        """Returns a string representing the guitar tab in a viewable format."""
        location = 2
        offset = 0
        strings = [
        [self.tuning[0],"|"],
        [self.tuning[1],"|"],
        [self.tuning[2],"|"],
        [self.tuning[3],"|"],
        [self.tuning[4],"|"],
        [self.tuning[5],"|"]
        ]
        for sound in self.tune:
            print(self.tune)
            if location >= self.lineLength:
                # strings = map(lambda s: s.append("\n"), strings)
                location = 0
            if type(sound) == Note:
                offset = len(sound.note)
                c = 1
                for string in strings:
                    print(strings)
                    print(string)
                    if c == sound.string:
                        string.append(sound.note)
                    else:
                        string.append("-" * offset)
                    c+= 1
            elif type(sound) == Chord:
                offset = 1
                c = 1
                for string in strings:
                    if sound.chord[c-1] is None:
                        string.append(sound.blankCharacter)
                    else:
                        string.append(sound.chord[c - 1])
                        c += 1
            location += offset + 1
            strings = map(lambda s: s.append("-"),strings)
        strings = map(lambda s: s.append("|"),strings)
        return "\n".join(["".join(s) for s in strings])

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
            self.note = "".join([str(self.fret[0]),self.command,str(self.fret[1])])

class Chord:
    """Represents a chord as a set of fret numbers.
    chord: tuple of 6 ints, "x" characters. A string not played
    is represented as None.
    ex: c chord: (None, 3, 2, 0, 1, 0)"""
    def __init__(self, chord, blank_char="-"):
        self.chord = chord
        self.blankCharacter = blank_charself

    def get_notes(self):
        notes = []
        for note in self.chord:
            if note is None:
                notes.append(self.blankCharacter)
            else:
                notes.append(str(note))
        return notes
