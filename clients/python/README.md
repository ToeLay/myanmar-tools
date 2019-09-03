# Myanmar Tools Python Documentation

This documentation is for Python specific usage of *Myanmar Tools*.  For general documentation, see [the top-level README](../../README.md).

## Python Usage

To detect Zawgyi, create a singleton instance of ZawgyiDetector, and call `getZawgyiProbability` with your string.

```python
from myanmar_tools import ZawgyiDetector
detector = ZawgyiDetector()
score = detector.getZawgyiProbability("မ္း")
# score is now 0.999772 (very likely Zawgyi)
```

To convert between Zawgyi and Unicode, use the methods zg2uni and uni2zg as shown below.

```python
from zawgyi_converter import ZawgyiConverter
converter = ZawgyiConverter()
output = converter.zg2uni("မ္း")
# output is now "မ်း"
```

For a complete working example, see [samples/python/demo.py](../../samples/python/demo.py).