from .translitrate_u2z import TranslitrateU2Z
from .translitrate_z2u import TranslitrateZ2U
from .translitrate_znorm import TranslitrateZNorm

class ZawgyiConverter:
    """
    Class implementing the converter for Zawgyi and Unicode
    """

    def __init__(self):
        self.__u2z = TranslitrateU2Z("Unicode -> Zawgyi")
        self.__z2u = TranslitrateZ2U("Zawgyi -> Unicode")
        self.__znorm = TranslitrateZNorm("Normalize Zawgyi")

    def uni2zg(self, inputString, normalize=False):
        """
        Convert Unicode string to Zawgyi string
        """

        convetedString = self.__u2z.convert(inputString)
        return self.normalizeZg(convetedString) if normalize else convetedString

    def zg2uni(self, inputString):
        """
        Convert Zawgyi string to Unicode string
        """
        
        return self.__z2u.convert(inputString)

    def normalizeZg(self, inputString):
        """
        Normalize the Zawgyi string
        """
        
        return self.__znorm.convert(inputString)