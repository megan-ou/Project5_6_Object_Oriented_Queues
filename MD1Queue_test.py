from unittest import TestCase
import math
import MD1Queue as q

class TestMD1Queue(TestCase):
    def setUp(self):
        self.queue = q.MD1Queue(15, 20)

    def test_init(self):
        # Before seeing Dr. Mitchell's test cases, I used self.queue.lamda, but that would test the setter/getter
        # I think we want to test to see if init calls the proper setters and everything works.
        self.assertAlmostEqual(15, self.queue._lamda)
        self.assertAlmostEqual(20, self.queue._mu)
        self.assertTrue(self.queue._recalc_needed)

    def test__calc_metrics(self):
        self.fail()
