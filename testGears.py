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




if __name__ == "__main__":
    unittest.main()
