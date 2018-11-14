#!/usr/bin/env python3

class CGearCombo(object):
    def __init__(self, nFront, nRear):
        self._num_front = nFront
        self._num_rear = nRear

    def ratio(self):
        try:
            rval = float(self._num_front) / self._num_rear
        except Exception as e:
            print("ERROR calculating ratio for f={}. r={}: {}".
                    format(self._num_front, self._num_rear, str(e)))
            rval = None
        return rval

    def as_string(self, verbose=False):
        fmt = "Front: {}, Rear: {}, Ratio {:.3f}" if verbose else "F:{} R:{} Ratio {:.3f}"
        return fmt.format(self._num_front, self._num_rear, self.ratio())


