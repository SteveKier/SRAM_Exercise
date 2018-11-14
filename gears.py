#!/usr/bin/env python3

class CGearCombo(object):
    def __init__(self, nFront, nRear):
        self._nFront = nFront
        self._nRear = nRear

    def ratio(self):
        try:
            rval = float(self._nFront) / self._nRear
        except Exception as e:
            print("ERROR calculating ratio for f={}. r={}: {}".
                    format(self._nFront, self._nRear, str(e)))
            rval = None
        return rval

    def asString(self, verbose=False):
        fmt = "Front: {}, Rear: {}, Ratio {:.3f}" if verbose else "F:{} R:{} Ratio {:.3f}"
        return fmt.format(self._nFront, self._nRear, self.ratio())


