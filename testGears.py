#!/usr/bin/env python3

import unittest
import gears

class CTestGears(unittest.TestCase):
    def setUp(self):
        pass

    def util_test_ratio(self, front, rear):
        ratio = float(front)/rear
        ratioAsStr = "{:.3f}".format(ratio)
        gc = gears.CGearCombo(front, rear)
        self.assertEqual(gc.ratio(), ratio)
        self.assertEqual(gc.as_string(True), "Front: {}, Rear: {}, Ratio {}".format(front, rear, ratioAsStr))
        self.assertEqual(gc.as_string(False), "F:{} R:{} Ratio {}".format(front, rear, ratioAsStr))

    def test_gear_combo(self):
        # Simple first test case (with hard-coded results to be really, really sure)
        gc = gears.CGearCombo(23, 45)
        self.assertEqual(gc.ratio(), (float(23) / 45))
        self.assertEqual(gc.as_string(True), "Front: 23, Rear: 45, Ratio 0.511")
        self.assertEqual(gc.as_string(False), "F:23 R:45 Ratio 0.511")

        # Another straightforward case
        self.util_test_ratio(38, 19)

        # One more straightforward case
        self.util_test_ratio(38, 16)

        # What if the denominator is zero?  We should get a None response and no crash.
        gc = gears.CGearCombo(38, 0)
        ratio = gc.ratio()
        self.assertIsNone(ratio)
        self.assertEqual(gc.as_string(True), "Front: 38, Rear: 0, Ratio None")
        self.assertEqual(gc.as_string(False), "F:38 R:0 Ratio None")

    def test_drive_train(self):
        dt = gears.CDriveTrain()
        f_cogs = [38, 30]
        r_cogs = [28, 23,  19, 16]
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertTrue(success)

        # try different (but still legal) numbers
        f_cogs = [54, 44, 38]
        r_cogs = [32, 28, 22, 18, 14, 10]
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertTrue(success)

        # should fail if they aren't sorted
        f_cogs = [44, 54, 38]
        r_cogs = [32, 28, 22, 18, 14, 10]
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertFalse(success)

        # (again, but this time the rear sones are in the wrong order)
        f_cogs = [54, 44, 38]
        r_cogs = [10, 32, 28, 22, 18, 14]
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertFalse(success)

        # They must be sorted in DESCENDING order
        f_cogs = [38, 44, 54]
        r_cogs = [10, 14, 18, 22, 28, 32]
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertFalse(success)

        # Empty cog lists aren't good, either.
        f_cogs = []
        r_cogs = [10, 14, 18, 22, 28, 32]
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertFalse(success)

        # (again, with the rear list empty)
        f_cogs = [38, 44, 54]
        r_cogs = []
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertFalse(success)

        # Of course, the cog lists had better be lists!
        f_cogs = "string"
        r_cogs = [1, 2, 3]
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertFalse(success)

        f_cogs = [3, 5, 7]
        r_cogs = 3.1415926
        success = dt.initCogs(f_cogs, r_cogs)
        self.assertFalse(success)

    def test_get_gear_combination(self):
        # Start with the example from the questions
        f_cogs = [38, 30]
        r_cogs = [28, 23, 19, 16]
        target_ratio = 1.6
        rval = gears.get_gear_combination(f_cogs, r_cogs, target_ratio)
        self.assertEqual(rval, "Front: 30, Rear: 19, Ratio 1.579")

        # try a few other ratios
        rval = gears.get_gear_combination(f_cogs, r_cogs, 2.0)
        self.assertEqual(rval, "Front: 38, Rear: 19, Ratio 2.000")
        rval = gears.get_gear_combination(f_cogs, r_cogs, 1.8)
        self.assertEqual(rval, "Front: 38, Rear: 23, Ratio 1.652")
        rval = gears.get_gear_combination(f_cogs, r_cogs, 1.9)
        self.assertEqual(rval, "Front: 30, Rear: 16, Ratio 1.875")
        rval = gears.get_gear_combination(f_cogs, r_cogs, 1.1)
        self.assertEqual(rval, "Front: 30, Rear: 28, Ratio 1.071")

        # try a ridiculously high ratio that we can't reach, but we should
        # still find the highest...
        rval = gears.get_gear_combination(f_cogs, r_cogs, 105.0)
        self.assertEqual(rval, "Front: 38, Rear: 16, Ratio 2.375")

        # Now try one that's so low that there's no solution
        rval = gears.get_gear_combination(f_cogs, r_cogs, 0.4)
        self.assertTrue(rval.startswith("No combination"))

        # Verify that when there's more than one way to achieve the
        # target ratio, we select the first of the matches.  (NOTE: In
        # the following, we could achieve a ratio of 6.0 with either 
        # (36, 6) or (24, 4), but we expect to select (36, 6).  Let's 
        # see if that's what happens.)
        f_cogs = [36, 24]
        r_cogs = [6, 4]
        target_ratio = 6.0
        rval = gears.get_gear_combination(f_cogs, r_cogs, target_ratio)
        self.assertEqual(rval, "Front: 36, Rear: 6, Ratio 6.000")





if __name__ == "__main__":
    unittest.main()
