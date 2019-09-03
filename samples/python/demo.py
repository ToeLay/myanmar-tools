from myanmar_tools import ZawgyiDetector
from myanmar_tools import ZawgyiConverter

detector = ZawgyiDetector()
converter = ZawgyiConverter()

# Unicode string:
input1 = "အပြည်ပြည်ဆိုင်ရာ လူ့အခွင့်အရေး ကြေညာစာတမ်း";
# Zawgyi string:
input2 = "အျပည္ျပည္ဆိုင္ရာ လူ႔အခြင့္အေရး ေၾကညာစာတမ္း";

# Detect that the second string is Zawgyi:
score1 = detector.getZawgyiProbability(input1)
score2 = detector.getZawgyiProbability(input2)
assert score1 < 0.001
assert score2 > 0.999
print(f"Unicode Score : {score1}")
print(f"Zawgyi Score : {score2}")

# Convert the second string to Unicode:
input2_converted = converter.zg2uni(input2)
assert input1 == input2_converted
print(f"Converted Text : {input2_converted}")