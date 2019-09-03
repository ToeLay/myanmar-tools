from .binary_markov import BinaryMarkov
from math import inf, exp

class ZawgyiUnicodeMarkovModel:
    """
    A Markov model to predict whether a string is more likely Unicode or Zawgyi.
    
    Internally, this class maintains two Markov chains, one representing Unicode and the other
    representing Zawgyi. An input string is evaluated against both chains, and the chain that returns
    the higher probability becomes the prediction.
    
    A string is evaluated as a sequence of transitions between states, including transitions to
    the edges of the string. For example, the string "ABC" contains 4 transitions: NULL to A, A to B,
    B to C, and C to NULL.
    
    For the purposes of Unicode/Zawgyi detection, all characters are treated as the NULL state
    except for characters in the Myanmar script or characters in the Unicode whitespace range U+2000
    through U+200B.
    """

    # Magic number used to identify this object in byte streams. (Reads in ASCII as "UZMODEL")
    __BINARY_TAG = 0x555A4D4F44454C20

    # Standard Myanmar code point range before digits
    __STD_CP0 = 0x1000
    __STD_CP1 = 0x103F
  
    # Standard Myanmar code point range after digits
    __AFT_CP0 = 0x104A
    __AFT_CP1 = 0x109F
  
    # Extended Myanmar code point range A
    __EXA_CP0 = 0xAA60
    __EXA_CP1 = 0xAA7F
  
    # Extended Myanmar code point range B
    __EXB_CP0 = 0xA9E0
    __EXB_CP1 = 0xA9FF
  
    # Unicode space characters
    __SPC_CP0 = 0x2000
    __SPC_CP1 = 0x200B
  
    # Indices into Markov nodes
    __STD_OFFSET = 1
    __AFT_OFFSET = __STD_OFFSET + __STD_CP1 - __STD_CP0 + 1
    __EXA_OFFSET = __AFT_OFFSET + __AFT_CP1 - __AFT_CP0 + 1
    __EXB_OFFSET = __EXA_OFFSET + __EXA_CP1 - __EXA_CP0 + 1
    __SPC_OFFSET = __EXB_OFFSET + __EXB_CP1 - __EXB_CP0 + 1
    __END_OFFSET = __SPC_OFFSET + __SPC_CP1 - __SPC_CP0 + 1
  
    
    """ 
     SSV: An ID representing which Unicode code points to include in the model:
    
     <p>SSV_STD_EXA_EXB_SPC - include Myanmar, Extended A, Extended B, and space-like
     <p>STD_EXA_EXB - same as above but no space-like code points
    
      <p>"SSV" originally stands for State Set Version. 
    """
     
    __SSV_STD_EXA_EXB_SPC = 0
    __SSV_STD_EXA_EXB = 1
    __SSV_COUNT = 2

    __ssv = 0

    def __init__(self, stream):
        # check magic number and serial version number
        binaryTag = int.from_bytes(stream.read(8), byteorder='big')
        if binaryTag != self.__BINARY_TAG:
            raise IOError(f'Unexpected magic number; expected {hex(self.__BINARY_TAG)} but got {hex(binaryTag)}')
        binaryVersion = int.from_bytes(stream.read(4), byteorder='big')
        if binaryVersion == 1:
            # Binary version 1 has no SSV field; SSV_STD_EXA_EXB_SPC is always used
            self.__ssv = self.__SSV_STD_EXA_EXB_SPC
        elif binaryVersion == 2:
            # Binary version 2 add SSV field
            self.__ssv = int.from_bytes(stream.read(4), byteorder='big')
        else:
            raise IOError(f'Unexpected serial version number; expected 1 or 2 but got {binaryVersion}')
        
        if self.__ssv < 0 or self.__ssv >= self.__SSV_COUNT:
            raise IOError(f'Unexpected value in ssv position; expected 0 or 1 but got {self.__ssv}')
        
        self.__classifier = BinaryMarkov(stream)
    
    def _getIndexForCodePoint(self, cp, ssv):
        """
        Returns the index of the state in the Markov chain corresponding to the given code point.
        
        Code points in the standard Myanmar range, Myanmar Extended A, Myanmar Extended B, and
        Unicode Whitespace each have a unique state assigned to them. All other code points are mapped
        to state 0.

        Parameters
        ----------
        cp : int
            The code point to convert to a state index.
        ssv : int
            The SSV corresponding to which code points included in the model.

        Returns
        -------
        int : The index of the state in the markov chain.
        """

        if self.__STD_CP0 <= cp and cp <= self.__STD_CP1:
            return cp - self.__STD_CP0 + self.__STD_OFFSET
        
        if self.__AFT_CP0 <= cp and cp <= self.__AFT_CP1:
            return cp - self.__AFT_CP0 + self.__AFT_OFFSET
        
        if self.__EXA_CP0 <= cp and cp <= self.__EXA_CP1:
            return cp - EXA_CP0 + EXA_OFFSET
        
        if self.__EXB_CP0 <= cp and cp <= self.__EXB_CP1:
            return cp - self.__EXB_CP0 + self.__EXB_OFFSET
            
        if ssv == self.__SSV_STD_EXA_EXB_SPC and self.__SPC_CP0 <= cp and cp <= self.__SPC_CP1:
            return cp - self.__SPC_CP0 + self.__SPC_OFFSET
            
        return 0

    def __char_count(self, codepoint):
        return (2 if codepoint >= 0x10000 else 1)

    def _predict(self, input_string, verbose):
        """
        Runs the given input string on both internal Markov chains and computes the probability of the
        string being unicode or zawgyi.

        Parameters
        ----------
        input_string : str
            The input string to evaluate.
        verbose : bool
            Whether to print the log probabilities for debugging.

        Returns
        -------
        float : The probability that the string is Zawgyi givent that it
        is either Unicode or Zawgyi, or -math.inf if there are no Myanmar
        range code points are in the string.
        """

        if verbose:
            print(f'Running detector on string: {input_string}')

        # start at the base state
        prevCp = 0
        prevState = 0

        totalDelta = 0.0
        seenTransition = False
        offset = 0
        while offset <= len(input_string):
            cp, currState = (0, 0) if offset == len(input_string) else (ord(input_string[offset]), self._getIndexForCodePoint(ord(input_string[offset]), self.__ssv))    

            #ignore 0-to-0 transitions
            if prevState != 0 or currState != 0:
                delta = self.__classifier._getLogProbabilityDifference(prevState, currState)
                if verbose:
                    print(f'U+{hex(prevCp)} -> U+{hex(cp)}: delta={delta}')
                    print(''.join(['!' for _ in range(int(abs(delta)))]))
                    print('')
                totalDelta+=delta
                seenTransition = True

            offset+= self.__char_count(cp)
            prevCp = cp
            prevState = currState

        if verbose:
            print(f'Final: delta={totalDelta}')

        #Special case: if there is no signal, return -Infinity,
        # which will get interpreted by users as strong Unicode.
        # This happens when the input string contains no Myanmar-range code points.
        if not seenTransition:
            return -inf

        # result = Pz/(Pu+Pz)
        #  = exp(logPz)/(exp(logPu)+exp(logPz))
        #  = 1/(1+exp(logPu-logPz))
        return 1 / (1 + exp(totalDelta))