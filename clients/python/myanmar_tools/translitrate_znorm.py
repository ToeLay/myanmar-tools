from .translitrate import Translitrate
from .rule import Rule

class TranslitrateZNorm(Translitrate):
    """
    Class implementing transliteration initialization of phases and rules for Zawgyi normalization.
    """

    def __init__(self, id):
        super().__init__(id)

        # Rules for phase 0
        phase0 = self._addPhase()
        phase0._addRule(Rule("\u00a0", "")) # custom rule ; this will remove non breaking space \xa0 in python
        phase0._addRule(Rule("\u1009\u1039", "\u1025\u1039"))
        phase0._addRule(Rule("\u1025\u102E", "\u1026"))
        phase0._addRule(Rule("\u102F([\u102D\u1036])", "\\g<1>\u102F"))
        phase0._addRule(Rule("\u1039([\u1037\u1094\u1095])", "\\g<1>\u1039"))
        phase0._addRule(Rule("\u103C([\u102E\u1032])", "\\g<1>\u103C"))
        phase0._addRule(Rule("\u1033\u102D", "\u102D\u1033"))
        phase0._addRule(Rule("\u103D\u102D", "\u102D\u103D"))
        phase0._addRule(Rule("\u1089", "\u103D\u1034"))
        phase0._addRule(Rule("\u1064\u103A", "\u103A\u1064"))
        phase0._addRule(Rule("\u1067", "\u1066"))
        phase0._addRule(Rule("\u1072", "\u1071"))
        phase0._addRule(Rule("\u1074", "\u1073"))
        phase0._addRule(Rule("\u1093", "\u107B"))

        # Rules for phase 1
        phase1 = self._addPhase()
        phase1._addRule(Rule("\u102D+", "\u102D"))
        phase1._addRule(Rule("\u102E+", "\u102E"))
        phase1._addRule(Rule("\u102F+", "\u102F"))
        phase1._addRule(Rule("\u1030+", "\u1030"))
        phase1._addRule(Rule("\u1032+", "\u1032"))
        phase1._addRule(Rule("\u1033+", "\u1033"))
        phase1._addRule(Rule("\u1034+", "\u1034"))
        phase1._addRule(Rule("\u1036+", "\u1036"))
        phase1._addRule(Rule("\u1037+", "\u1037"))
        phase1._addRule(Rule("\u1039+", "\u1039"))
        phase1._addRule(Rule("\u103A+", "\u103A"))
        phase1._addRule(Rule("\u103B+", "\u103B"))
        phase1._addRule(Rule("\u103C+", "\u103C"))
        phase1._addRule(Rule("\u103D+", "\u103D"))
        phase1._addRule(Rule("\u103E+", "\u103D"))

        # Rules for phase 2
        phase2 = self._addPhase()
        phase2._addRule(Rule("[\u1037\u1094\u1095]+", "\u1037"))
        phase2._addRule(Rule("\u1005\u103A", "\u1008"))
        phase2._addRule(Rule("\u101D", "\u1040"))
        phase2._addRule(Rule("\u104E$", "\u1044"))
        phase2._addRule(Rule("\u102F\u1088", "\u1088"))
        phase2._addRule(Rule("\u103B\u103A", "\u103A\u103B"))
        phase2._addRule(Rule("\u103D\u102F", "\u1088"))
        phase2._addRule(Rule("\u103D\u1088", "\u1088"))
        phase2._addRule(Rule("\u103B([\u1000-\u1021])\u103B$", "\u103B\\g<1>"))

        # Rules for phase 3
        phase3 = self._addPhase()
        phase3._addRule(Rule("[\u103B\u107E-\u1084]+", "\u103B"))
        phase3._addRule(Rule("\u1031\u1031+", "\u1031"))

        # Rules for phase 4
        phase4 = self._addPhase()
        phase4._addRule(Rule("([\u103B\u107E-\u1084])([\u1000-\u1021])\u1036\u102F", "\\g<1>\\g<2>\u1033\u1036"))

        # Rules for phase 5
        phase5 = self._addPhase()
        phase5._addRule(Rule("\u1033", "\u102F"))

        # Rules for phase 6
        phase6 = self._addPhase()
        phase6._addRule(Rule("\u1036\u102F", "\u102F\u1036"))
        phase6._addRule(Rule("\u1037\u1039\u1037", "\u1037\u1039"))
        #phase6._addRule(Rule("[|\u106A\u106B]", "\u100A"))
        phase6._addRule(Rule("[\u106A\u106B]", "\u100A")) # above rule should be like that

        # Rules for phase 7
        phase7 = self._addPhase()
        phase7._addRule(Rule("[    -‍⁠  　﻿]+([\u1000-\u109F])", "\\g<1>")
            ._setRevisitPosition(0))
        phase7._addRule(Rule("\u200B+", "")
            ._setMatchOnStart())
        phase7._addRule(Rule("\u200B+$", ""))