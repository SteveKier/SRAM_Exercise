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
        fmt = "Front: {}, Rear: {}, Ratio {}" if verbose else "F:{} R:{} Ratio {}"
        ratio = self.ratio()
        ratioAsStr = "{:.3f}".format(ratio) if ratio else "None"
        return fmt.format(self._num_front, self._num_rear, ratioAsStr)


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
        '''
        Find and return the CGearCombo that gets us closest to the given
        'target_ratio' (closest without going over).  If all possible ratios
        exceed 'target_ratio," return None.
        '''
        closestRatio = 2 * target_ratio
        closestCombo = None
        for numFront in self._frontCogs:
            for numRear in self._rearCogs:
                combo = CGearCombo(numFront, numRear)
                ratio = combo.ratio()
                # print ("for f={}, r={}, combo={}, ratio={}".format(numFront, numRear, combo, ratio))
                if ratio > target_ratio:
                    # Denominators are getting smaller, so ratios are increasing.  Once
                    # we get a ratio greater than target, we're done.
                    break
                else:
                    diff = target_ratio - ratio
                    if diff < closestRatio:
                        # print ("...so update our idea of the closest...")
                        closestRatio = diff
                        closestCombo = combo
        return closestCombo


def get_gear_combination(f_cogs, r_cogs, target_ratio):
    # print ("===== get_gear_combination(f, r, {})".format(target_ratio))
    drive_train = CDriveTrain()
    if drive_train.initCogs(f_cogs, r_cogs):
        combo = drive_train.getGearCombo(target_ratio)
        if combo is None:
            rval = "No combination yields a ratio at or below the target ({})".format(target_ratio)
        else:
            rval = combo.as_string(True)
    print (rval)
    return rval
