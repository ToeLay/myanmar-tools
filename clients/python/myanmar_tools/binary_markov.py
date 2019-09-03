import struct

class BinaryMarkov:
    """
    A class that behaves as if it were two Markov chains, called Chain A and Chain B. Whereas a
    normal Markov chain would expose the log probability of a transition, this class exposes the
    difference between the log probabilities of the two Markov chains. When training, you can specify
    which Markov chain a transition should be added to.
    
    The reasoning behind this class is that it has a smaller data footprint than two separate
    Markov chain objects.
    """

    # Magic number used to identify this object in byte streams. (Reads in ASCII as "BMARKOV ")
    __BINARY_TAG = 0x424D41524B4F5620

    # Current serial format version number, used in association with the magic number. */
    __BINARY_VERSION = 0

    __logProbabilityDifferences = []

    def __init__(self, stream):
        #check magic number and serial version number
        binaryTag = int.from_bytes(stream.read(8), byteorder='big')
        if binaryTag != self.__BINARY_TAG:
            raise IOError(f'Unexpected magic number; expected {hex(self.__BINARY_TAG)} but got {hex(binaryTag)}')
        binaryVersion = int.from_bytes(stream.read(4), byteorder='big')
        
        if binaryVersion != self.__BINARY_VERSION:
            raise IOError(f'Unexpected serial version number; expected {self.__BINARY_VERSION} but got {binaryVersion}')

        size = int.from_bytes(stream.read(2), byteorder='big')

        for index1 in range(size):
            entries = int.from_bytes(stream.read(2), byteorder='big')
            fallback = 0.0 if entries == 0 else struct.unpack('>f', stream.read(4))[0]
            
            next = -1
            logProbabilityDifferencesRow = []

            for index2 in range(size):
                if entries > 0 and next < index2:
                    next = int.from_bytes(stream.read(2), byteorder='big')
                    entries-=1
                
                if next == index2:
                    [entry] = struct.unpack('>f',stream.read(4))
                    logProbabilityDifferencesRow.append(entry)
                else:
                    logProbabilityDifferencesRow.append(fallback)
            
            self.__logProbabilityDifferences.append(logProbabilityDifferencesRow)

        
    def _getLogProbabilityDifference(self, i1, i2):
        """
        Gets the difference in log probabilities between chain A and chain B. This behaves as if you
        had two Markov chains and called
        chainA.getLogProbability(i1, i2) - chainB.getLogProbability(i1, i2).

        Parameters
        ----------
        i1 : int
            The index of the source node to transition from.
        i2 : int
            The index of the destination node to transition to.

        Returns
        -------
        float : The difference between A and B in log probabilities of transitioning from i1 to i2.
        """
        return self.__logProbabilityDifferences[i1][i2]