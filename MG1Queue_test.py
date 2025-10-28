from unittest import TestCase
import math
import MG1Queue as q

class TestMG1Queue(TestCase):
    def setUp(self):
        self.queue = q.MG1Queue(15, 20)

    def test_init(self):
        #test first with no explicit sigma
        self.assertAlmostEqual(15, self.queue._lamda)
        self.assertAlmostEqual(20, self.queue._mu)
        self.assertAlmostEqual(0.0,self.queue._sigma)
        self.assertTrue(self.queue._recalc_needed)

        #test now with explicit sigma
        self.queue = q.MG1Queue(15, 20, 1)
        self.assertAlmostEqual(1,self.queue._sigma)

    def test_sigma(self):
        #test getter
        self.assertAlmostEqual(0.0, self.queue.sigma)

        #test setter
        #test valid values: 1.2
        self.queue.sigma = 1.2
        self.assertAlmostEqual(1.2, self.queue.sigma)

        #test the invalid values
        #negative values
        self.queue.sigma = -1
        self.assertTrue(math.isnan(self.queue.sigma))

        #not a Number
        self.queue.sigma = "2"
        self.assertTrue(math.isnan(self.queue.sigma))

        #test to see if recalc_needed is true
        self.assertTrue(self.queue._recalc_needed)


    def test_is_valid(self):
        # Test for valid values
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue.sigma = 3.4
        self.assertTrue(self.queue.is_valid())

        # Test for invalid values for lamda
        self.queue.lamda = 0
        self.assertFalse(self.queue.is_valid())

        self.queue.lamda = -5
        self.assertFalse(self.queue.is_valid())

        self.queue.lamda = "10"
        self.assertFalse(self.queue.is_valid())

        # Test for invalid values for mu
        self.queue.lamda = 15
        self.queue.mu = 0
        self.assertFalse(self.queue.is_valid())

        self.queue.mu = -5
        self.assertFalse(self.queue.is_valid())

        self.queue.mu = "10"
        self.assertFalse(self.queue.is_valid())

        #Test for invalid values for sigma
        self.queue.mu = 20
        self.queue.sigma = -1
        self.assertFalse(self.queue.is_valid())

        self.queue.sigma = "3.4"
        self.assertFalse(self.queue.is_valid())

    def test__calc_metrics(self):
        #test with valid values
        self.queue.lamda = 20
        self.queue.mu = 25
        self.queue.sigma = 0.04
        self.queue._calc_metrics()
        self.assertAlmostEqual(3.2, self.queue.lq)
        self.assertAlmostEqual(0.2, self.queue.p0)

        #test with invalid values
        #negative lamda
        self.queue.lamda = -12
        self.queue._calc_metrics()
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #negative mu
        self.queue.lamda = 20
        self.queue.mu = -25
        self.queue._calc_metrics()
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #negative sigma
        self.queue.mu = 25
        self.queue.sigma = -0.04
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #test with infeasible values
        self.queue.lamda = 26
        self.queue.sigma = 0.04
        self.assertTrue(math.isinf(self.queue.lq))
        self.assertTrue(math.isinf(self.queue.p0))

        #check is recalc_needed is false
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
        self.assertAlmostEqual(4, self.queue.l)
        self.assertAlmostEqual(0.16, self.queue.wq)
        self.assertAlmostEqual(0.2, self.queue.w)


