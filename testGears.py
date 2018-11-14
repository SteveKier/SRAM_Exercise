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



if __name__ == "__main__":
    unittest.main()
