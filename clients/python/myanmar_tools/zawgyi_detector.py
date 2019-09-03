from .zawgyi_unicode_markov_model import ZawgyiUnicodeMarkovModel
from pkg_resources import resource_stream

class ZawgyiDetector:
    """
    Uses a machine learning model to determine whether a string of text is Zawgyi or Unicode.
    """
    
    def __init__(self):
        #Loads the model from the resource and returns a ZawgyiDetector instance.

        stream = resource_stream('myanmar_tools.resources', 'zawgyiUnicodeModel.dat')
        self.__model = ZawgyiUnicodeMarkovModel(stream)
        stream.close()
         
    def getZawgyiProbability(self, input_string, verbose = False):
        """
        Performs detection on the given string. Returns the probability that the string is Zawgyi given
        that it is either Unicode or Zawgyi. Values approaching 1 are strong Zawgyi; values approaching 0 
        are strong Unicode; and values close to 0.5 are toss-ups.
        
        If the string does not contain any Myanmar range code points, -math.inf is returned.

        Parameters
        ----------
        input_string : str
            The string on which to run detection.
        verbose : bool, optional
            If True, print debugging information to standard output (default False)
        """
        return self.__model._predict(input_string, verbose)