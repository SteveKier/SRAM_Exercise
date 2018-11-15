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

    def __str__(self):
        return self.as_string()

    def __eq__(self, other):
        return self._num_front == other._num_front and self._num_rear == other._num_rear

    def __ne__(self, other):
        return not (self == other)


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
        self._front_cogs = front
        self._rear_cogs = rear
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
        for numFront in self._front_cogs:
            for numRear in self._rear_cogs:
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

    def nextStepTowards(self, fromCombo, toCombo):
        '''
        Given CGearCombos 'fromCombo' and 'toCombo', figure out the next 
        'adjacent' combo after 'fromCombo' that moves us towards 'toCombo.'
        Our strategy is to adjust the front cog until it matches to.front,
        and then adjust the rear cog until both match.  If the caller 
        passes us equal combos (i.e., if from == to), we just return from.
        '''
        combo = fromCombo
        if fromCombo == toCombo:
            print ("ERROR: nextStepTowards() receives equal CGearCombos ({})".format(fromCombo))
        else:
            idxFrom = self._front_cogs.index(fromCombo._num_front)
            idxTo = self._front_cogs.index(toCombo._num_front)
            distance = idxTo - idxFrom
            if distance:
                # Still need to adjust the front cog
                incr = int(distance / abs(distance))
                combo = CGearCombo(self._front_cogs[idxFrom + incr], fromCombo._num_rear)
            else:
                # need to adjust the rear cog
                idxFrom = self._rear_cogs.index(fromCombo._num_rear)
                idxTo = self._rear_cogs.index(toCombo._num_rear)
                distance = idxTo - idxFrom
                incr = int(distance / abs(distance))
                # print (fromCombo)
                # print (fromCombo._num_front)
                # print (idxFrom)
                # print (incr)
                # print (self._rear_cogs[idxFrom + incr])
                combo = CGearCombo(fromCombo._num_front, self._rear_cogs[idxFrom + incr])

        # print ("nextStepTowards(fr={}, to={}) returns {}".format(fromCombo, toCombo, combo))
        return combo

    def getShiftSequence(self, target_ratio, start_combo):
        sequence = None
        end_combo = self.getGearCombo(target_ratio)
        if not end_combo:
            print ("No path to desired target ({}).  Return None".format(target_ratio))
            sequence = None
        else:
            sequence = [start_combo]
            cur_combo = start_combo
            while cur_combo != end_combo:
                cur_combo = self.nextStepTowards(cur_combo, end_combo)
                sequence.append(cur_combo)
        return sequence



def get_gear_combination(f_cogs, r_cogs, target_ratio):
    '''
    Create a CDriveTrain with the given cog lists and call its getGearCombo()
    method to find the gear combination whose ratio is closest to target_ratio.
    If getGearCombo() returns None (see above), return None to indicate the 
    failure.  Otherwise, print the string representation of the CGearCombo (and 
    return that string).
    '''
    # print ("===== get_gear_combination(f, r, {})".format(target_ratio))
    rval = None
    drive_train = CDriveTrain()
    if drive_train.initCogs(f_cogs, r_cogs):
        combo = drive_train.getGearCombo(target_ratio)
        if combo is None:
            print ("No combination yields a ratio at or below the target ({})".format(target_ratio))
            rval = None
        else:
            rval = combo.as_string(True)
            print (rval)
    return rval

def get_shift_sequence(f_cogs, r_cogs, ratio, initial_combination):
    '''
    Create a CDriveTrain with the given cog lists and call its getShiftSequence()
    method to get the list of CGearCombos that represents the "path" from 
    "initial_combination" to a gear combo that gets us as close as possible to
    "ratio."  If there's no path, return None and print a message.  If things
    go well, print the path (and return it to the caller).
    '''
    # print ("===== get_shift_sequence(f, r, tgt= {}, init={})".format(ratio, initial_combination))
    path = None
    drive_train = CDriveTrain()
    if not drive_train.initCogs(f_cogs, r_cogs):
        print ("ERROR: Unable to initialize CDriveTrain")
    else:
        path = drive_train.getShiftSequence(ratio, initial_combination)
        if path is None:
            print ("No path to target ({})".format(ratio))
        else:
            for idx, combo in enumerate(path):
                print ("{} - {}".format(idx+1, combo.as_string(False)))
    return path

def demo():
    print ("===== Problem #1: get_gear_combination()")
    f_cogs = [38, 30]
    r_cogs = [28, 23, 19, 16]
    target_ratio = 1.6
    get_gear_combination(f_cogs, r_cogs, target_ratio)

    print ("===== Problem #2: get_shift_sequence()")
    f_cogs = [38, 30]
    r_cogs = [28, 23, 19, 16]
    ratio = 1.6
    initial_combination = CGearCombo(38, 28)
    get_shift_sequence(f_cogs, r_cogs, ratio, initial_combination)

if __name__ == "__main__":
    demo()
