import unittest
from myanmar_tools import ZawgyiDetector
from math import inf
from pkg_resources import resource_string

class ZawgyiDetectorTest(unittest.TestCase):

    def setUp(self):
        self.detector = ZawgyiDetector()
    
    def test_IgnoreNonMyanmarCodePoints(self):
        allASCII = "blah blah blah blah blah"
        mixedUnicode = "<span>blah blah ဒဂုန်ဦးစန်းငွေ </span> blah blah blah blah"
        mixedZawgyi = "blah blah blah blah blah သို႔သြားပါ။ blah blah blah"

        allASCII_actual_score = self.detector.getZawgyiProbability(allASCII)
        mixedUnicode_actual_score = self.detector.getZawgyiProbability(mixedUnicode)
        mixedZawgyi_actual_score = self.detector.getZawgyiProbability(mixedZawgyi)

        self.assertEqual(allASCII_actual_score, -inf)
        self.assertLess(mixedUnicode_actual_score, 0.01)
        self.assertGreater(mixedZawgyi_actual_score, 0.99)

    def test_strongUnicodeReturnsLowScore(self):
        strongUnicode = "အပြည်ပြည်ဆိုင်ရာ လူ့အခွင့်အရေး ကြေညာစာတမ်း"
        actual_score = self.detector.getZawgyiProbability(strongUnicode)
        self.assertLess(actual_score, 0.001)

    def test_strongZawgyiReturnsHighScore(self):
        strongZawgyi = "အျပည္ျပည္ဆိုင္ရာ လူ႔အခြင့္အေရး ေၾကညာစာတမ္း"
        actual_score = self.detector.getZawgyiProbability(strongZawgyi)
        self.assertGreater(actual_score, 0.999)

    def test_ignoreNumerals(self):
        self.assertEqual(self.detector.getZawgyiProbability("၉၆.၀ kHz"), -inf)
        self.assertEqual(self.detector.getZawgyiProbability("၂၄၀၉ ဒဂုန်"), self.detector.getZawgyiProbability("ဒဂုန်"))

    def test_compatibility(self):
        for line in resource_string('myanmar_tools.resources', 'compatibility.tsv').decode('utf-8').split('\n'):
            if line != "":
                expected_score, input_sring = line.split('\t')
                if expected_score == "-Infinity":
                    expected_score = -inf
                else:
                    expected_score = float(expected_score)
                actual_score = self.detector.getZawgyiProbability(input_sring)
                self.assertEqual(expected_score, actual_score)

if __name__ == '__main__':
    unittest.main()