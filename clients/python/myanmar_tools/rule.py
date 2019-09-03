import re

class Rule:
    """
    Class implementing a rule as part of a transliteration phase.
    """

    def __init__(self, patternString, substitutionString):

        # Fields of the rule
        self.pattern = re.compile(f"^{patternString}")
        self.substitution = substitutionString
        self.matchOnStart = False
        self.revisitPosition = -1
        self.info = "" # Id number or other information.
        self.contextBefore = ""
        self.contextAfter = ""

    def _setInfo(self, ruleInfo):
        self.info = ruleInfo
        return self

    def _setMatchOnStart(self):
        self.matchOnStart = True
        return self

    def _setRevisitPosition(self, newPos):
        self.revisitPosition = newPos
        return self

    def _setBeforeContext(self, before):
        self.contextBefore = before
        return self

    def _setAfterContext(self, after):
        self.contextAfter = after
        return self

    def _printRule(self):
        result = f"  R {self.info} p: {self.pattern} s: {self.substitution}"
        result+= " matchOnStart = True " if self.matchOnStart else ""
        result+= f" revisitPosition = {self.revisitPosition}" if self.revisitPosition >= 0 else ""
        result+= f" contextBefore = {self.contextBefore}" if self.contextBefore != "" else ""
        result+= f" contextAfter = {self.contextAfter}" if self.contextAfter != "" else ""
        return result+"\n"
