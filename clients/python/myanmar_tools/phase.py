import re

class Phase:
    """
    Class implementing a transliteration phase as an array of rules.
    """

    def __init__(self):
        self.phaseRules = []
        self.info = ""
        self.debugMode = False

    def _setInfo(self, newInfo):
        self.info = newInfo

    def _setDebugMode(self, newMode):
        self.debugMode = newMode

    def _addRule(self, newRule):
        self.phaseRules.append(newRule)
        # Put the rule number within the phase.
        newRule._setInfo(f"{len(self.phaseRules)}")

    def _printPhase(self):
        s = f" Phase has {len(phaseRules)} rules\n" 
        for rule in self.phaseRules:
            s+=f'{rule._printRule()}'
        return s

    def _runPhase(self, phase, inString):
        #Run all the rules of this phase.
        outString = []
        midString = inString
        startOfString = True
        changed = False

        if self.debugMode:
            print(f"Phase {info}, input= {inString} ({len(inString)})")

        while len(midString) > 0:
            # Move through the string, matching / applying rules .
            foundRule = False
            for rule in self.phaseRules:
                if not rule.matchOnStart or startOfString:
                    pattern = rule.pattern
                    m = pattern.match(midString)
                    if m:
                        foundRule = True
                        rightPartSize = len(midString) - len(m.group(0))
                        midString = re.sub(pattern, rule.substitution, midString)
                        changed = True

                        if rule.revisitPosition < 0:
                            # Reset the new position to the end of the subsitution.
                            newStart = len(midString) - rightPartSize
                            outString.append(midString[0:newStart])
                            midString = midString[newStart:]

            # All rules applied at this position.
            if not foundRule:
                # Move forward by 1
                outString.append(midString[0])
                midString = midString[1:]

            startOfString = False

        if self.debugMode and changed:
            print(f" Return changed result = {outString} ({len(outString)})")

        return "".join(outString)