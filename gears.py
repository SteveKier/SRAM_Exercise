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


class CDriveTrain(object):
    def __init__(self):
        pass

    def initCogs(self, front, rear):
        '''
        Initialize the front and rear "cog" lists.
        Run a sanity check to be sure they are sorted (descending) and are not empty.
        Also be sure they are lists (!)
        Return True if all is well, False otherwise
        '''
        self._frontCogs = front
        self._rearCogs = rear
        rval = False
        if not(isinstance(front, list) and isinstance(rear, list)):
            print ("initCogs() passed non-list argument(s): front={}, rear={}".format(front, rear))
        elif not(front and rear):
            print ("initCogs() finds empty list argument: front={}, rear={}".format(front, rear))
        else:
            sortedFront = sorted(front, reverse=True)
            sortedRear = sorted(rear, reverse=True)
            if sortedFront != front or sortedRear != rear:
                print ("initCogs() expects cogs sorted high-to-low.  front={}, rear={}".format(front, rear))
            else:
                rval = True

        return rval

    def getGearCombo(self, target_ratio):
        closestRatio = 0
        closestCombo = None
        for numFront in self._frontCogs:
            for numRear in self._frontCogs:
                combo = CGearCombo(numFront, numRear)
                ratio = combo.ratio()
                if ratio > target_ratio:
                    # Denominators are getting smaller, so ratios are increasing.  Once
                    # we get a ratio greater than target, we're done.
                    break
                else:
                    diff = target_ratio -ratio
                    if diff < closestRatio:
                        closestRatio = diff
                        closestCombo = combo
        return closestCombo
