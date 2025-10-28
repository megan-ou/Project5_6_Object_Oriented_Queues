from unittest import TestCase
import math
import MD1Queue as q

class TestMD1Queue(TestCase):
    def setUp(self):
        self.queue = q.MD1Queue(15, 20)

    def test_init(self):
        self.assertAlmostEqual(15, self.queue._lamda)
        self.assertAlmostEqual(20, self.queue._mu)
        self.assertTrue(self.queue._recalc_needed)

    def test__calc_metrics(self):
        # test with valid values
        self.queue.lamda = 20
        self.queue.mu = 25
        self.queue._calc_metrics()
        self.assertAlmostEqual(1.6, self.queue.lq)
        self.assertAlmostEqual(0.2, self.queue.p0)

        # test with invalid values
        # negative lamda
        self.queue.lamda = -12
        self.queue._calc_metrics()
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        # negative mu
        self.queue.lamda = 20
        self.queue.mu = -25
        self.queue._calc_metrics()
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        # test with infeasible values
        self.queue.lamda = 26
        self.queue.mu = 25
        self.assertTrue(math.isinf(self.queue.lq))
        self.assertTrue(math.isinf(self.queue.p0))

        # check is recalc_needed is false
        self.assertFalse(self.queue._recalc_needed)

    def test_properties(self):
        """
        Tests all queue attributes & if they inherit/calculate properly with a valid and feasible
        queue
        Returns: none
        """
        self.queue.lamda = 20
        self.queue.mu = 25
        self.queue.sigma = 0.04

        self.assertAlmostEqual(0.8, self.queue.ro)
        self.assertAlmostEqual(2.4, self.queue.l)
        self.assertAlmostEqual(0.08, self.queue.wq)
        self.assertAlmostEqual(0.12, self.queue.w)
