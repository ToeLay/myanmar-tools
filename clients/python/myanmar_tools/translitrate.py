from .phase import Phase

class Translitrate():

    def __init__(self, id):
        self.translitPhases = []
        self.name = id
        self.debugMode = False

    def _addPhase(self):
        newPhase = Phase()
        newPhase._setInfo(f" {len(self.translitPhases)}")
        self.translitPhases.append(newPhase)
        newPhase._setDebugMode(self.debugMode)
        return newPhase

    def _setDebugMode(self, newMode):
        self.debugMode = newMode
        for phase in self.translitPhases:
            phase._setDebugMode(self.debugMode)

    def toString(self):
        s = f"Transliterator name = {self.name}\n Phase count : {len(self.translitPhases)}\n"
        for phase in self.translitPhases:
            s+= phase._printPhase()

        return s

    # Apply the transliteration to the input string,
    # returning the converted result.
    def convert(self, inString):
        return self.__runAllPhases(inString)

    def __runAllPhases(self, inString):
        count = 0
        outString = inString
        for phase in self.translitPhases:
            count+=1
            outString = phase._runPhase(phase, outString)

        return outString