# Storage, viewing, and editing for guitar tablature.

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
    smooth = TabReader().parse_tab("test_tab.txt")
    print(smooth)

class TabReader:
    """Takes a text file formatted like a guitar tab
    and parses it to create a Tab object."""

    def __init__(self):
        pass

    def parse_tab(self, tab_file):
        """Takes a file name to extract the text for a guitar
        tab from and returns a Tab object."""

        # Read from a tab file, turning it into one
        # continuous tab with no line breaks
        print("reading from",tab_file)
        with open(tab_file) as tab:
            title = tab.readline()[1:-2]
            strings = [tab.readline() for x in range(6)]
            while "|" not in strings[0][2:]:
                print(strings[0][-2])
                for s in strings:
                    s += tab.readline()[:-1] # strip off that newline

        # tuning is first letter of each line of tab
        tuning = [s[0] for s in strings][::-1]

        loc = 2
        current = [s[loc] for s in strings]
        noteBeingBuilt = ""
        # move through the tab one column at a time until
        # we hit another pipe, which signals the end of the tab
        song = []
        while "|" not in current:
            current = [s[loc] for s in strings]
            # print(current)

            # if that column is "blank"
            if set(current) == set("-"):
                if noteBeingBuilt == "":
                    loc += 1
                    continue
                else:
                    song.append(Note(noteBeingBuilt,7 - noteString))
                    noteBeingBuilt = ""

            # if there are exactly five blank spaces in the column
            # then we know it's a Note
            elif current.count("-") == 5:
                noteString = 1
                for s in current:
                    if s != "-":
                        noteBeingBuilt += s
                        break
                    noteString += 1
            # two or more strings with notes on them mean a chord
            elif current.count("-") <= 4:
                chordBeingBuilt = []
                jump = False
                # check the next column if it's a two-digit chord
                peek = [s[loc + 1] for s in strings]
                # add each fret number of the chord
                for s, p in zip(current, peek):
                    if s != "-" and p != "-":
                        chordBeingBuilt.append(s+p)
                        jump = True
                    elif s != "-":
                        chordBeingBuilt.append(s)
                    else:
                        chordBeingBuilt.append(None)
                if jump:
                    loc += 1

                song.append(Chord(chordBeingBuilt[::-1]))
            loc += 1

        print(song[-1].chord)
        return Tab(song[:-1:], title, tuning=tuning)

class Tab:
    """Stores a guitar tab as a series of Note and Chord objects."""

    def __init__(self, tune, name,
                tuning=("E","A","D","G","B","e"),
                line_length=60):
        self.tuning = tuning
        self.lineLength = 60 # line_length
        self.tune = tune
        self.name = name

    def __str__(self):
        return self.display_tab()

    def display_tab(self):
        """Returns a string representing the guitar tab in a viewable format."""
        location = 2
        offset = 0
        strings = [
        [self.tuning[0],"|", "-"],
        [self.tuning[1],"|", "-"],
        [self.tuning[2],"|", "-"],
        [self.tuning[3],"|", "-"],
        [self.tuning[4],"|", "-"],
        [self.tuning[5],"|", "-"]
        ]
        for sound in self.tune:
            if location >= self.lineLength:
                # strings = map(lambda s: s.append("\n"), strings)
                location = 0
            if type(sound) == Note:
                offset = len(sound  .note)
                c = 1
                for string in strings:
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
            for s in strings: s.append("-")
        for s in strings: s.append("|")
        title = "[{}]\n".format(self.name)
        return title + "\n".join(["".join(s) for s in strings][::-1])

class Note:
    """Represents a single note as a fret and string number, with
    optional special command.
    Note: Fret numbers or fret numbers + command, as string
    String: int from 1 to 6"""
    def __init__(self, note, string, command=None):
        self.note = note
        self.string = string

class Chord:
    """Represents a chord as a set of fret numbers.
    chord: tuple of 6 ints, "x" characters. A string not played
    is represented as None.
    ex: c chord: (None, 3, 2, 0, 1, 0)"""
    def __init__(self, chord, blank_char="-"):
        self.chord = chord
        self.blankCharacter = blank_char
        self.chord = self.get_notes()

    def get_notes(self):
        notes = []
        for note in self.chord:
            if note is None:
                notes.append(self.blankCharacter)
            else:
                notes.append(str(note))
        return notes

if __name__ == "__main__":
    main()
