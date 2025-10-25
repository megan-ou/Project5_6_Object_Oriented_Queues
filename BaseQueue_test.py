from unittest import TestCase
import math
import BaseQueue as q

class TestBaseQueue(TestCase):
    def setUp(self):
        self.queue = q.BaseQueue(15, 20)

    def test_init(self):
        #Before seeing Dr. Mitchell's test cases, I used self.queue.lamda, but that would test the setter/getter
        # I think we want to test to see if init calls the proper setters and everything works.
        self.assertAlmostEqual(15, self.queue._lamda)
        self.assertAlmostEqual(20, self.queue._mu)
        self.assertTrue(self.queue._recalc_needed)

    def test_lamda(self):
        #First test the getter method
        self.assertAlmostEqual(15, self.queue.lamda)

        #Now test the setters
        #Valid tuple value, see if it aggregates
        #In a way, this also tests simplify_lamda?
        self.queue.lamda = (5,10,15)
        self.assertAlmostEqual(30, self.queue.lamda)

        #Valid single value
        self.queue.lamda = 35
        self.assertAlmostEqual(35, self.queue.lamda)

        #Invalid values, non numbers and out of range
        self.queue.lamda = 0
        self.assertTrue(math.isnan(self.queue.lamda))

        self.queue.lamda = -1
        self.assertTrue(math.isnan(self.queue.lamda))

        self.queue.lamda = "1"
        self.assertTrue(math.isnan(self.queue.lamda))

        #Invalid value hidden inside tuple with valid values
        self.queue.lamda = (5,"10",15)
        self.assertTrue(math.isnan(self.queue.lamda))

        self.queue.lamda = (5,0,15)
        self.assertTrue(math.isnan(self.queue.lamda))

        self.queue.lamda = (5,-5,10)
        self.assertTrue(math.isnan(self.queue.lamda))

        #Test to see if recalc_needed is true after lamda has been changed
        self.assertTrue(self.queue._recalc_needed)

    def test_mu(self):
        #First test the getter method
        self.assertAlmostEqual(20, self.queue.mu)

        #Now test the setter method
        #Valid value
        self.queue.mu = 25
        self.assertAlmostEqual(25, self.queue.mu)

        #Invalid values, out of range and non numbers
        self.queue.mu = 0
        self.assertTrue(math.isnan(self.queue.mu))

        self.queue.mu = -1
        self.assertTrue(math.isnan(self.queue.mu))

        self.queue.mu = "5"
        self.assertTrue(math.isnan(self.queue.mu))

    def test_lq(self):
        #lq should always be math.nan for BaseQueue
        self.assertTrue(math.isnan(self.queue.lq))

        # test to see if getter will work when lq is not nan
        self.queue._lq = 20
        self.assertAlmostEqual(20, self.queue.lq)

        #test functionality of recalc_needed boolean; if it is true, is calc_metrics called and is the
        # variable then set to false? The value of lq should still be nan because that is what calc_metrics
        # was set to do.
        #Sets recalc_needed to true
        self.queue.lamda = 15
        self.queue.mu = 20
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertFalse(self.queue._recalc_needed)

    def test_p0(self):
        #p0 should always be math.nan for BaseQueue
        self.assertTrue(math.isnan(self.queue.p0))

        # test to see if getter will work when p0 is not nan
        self.queue._p0 = 15
        self.assertAlmostEqual(15, self.queue.p0)

        #test recalc_needed function in getter, same as testing for lq
        self.queue.lamda = 16
        self.queue.mu = 18
        self.assertTrue(math.isnan(self.queue.p0))
        self.assertFalse(self.queue._recalc_needed)

    def test_l(self):
        #l should always be nan for BaseQueue
        self.assertTrue(math.isnan(self.queue.l))

        #test to see if it will give correct values if lq is not nan
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue._lq = 5
        self.queue._recalc_needed = False
        self.assertAlmostEqual(5.75,self.queue.l)

    def test_r(self):
        #r should have a value if lamda and mu are valid
        self.queue.lamda = 15
        self.queue.mu = 20
        self.assertAlmostEqual(0.75,self.queue.r)

        self.queue.lamda = 25
        self.assertAlmostEqual(1.25,self.queue.r)

        #test invalid values for lamda and mu
        self.queue.lamda = 0
        self.assertTrue(math.isnan(self.queue.r))

        self.queue.lamda = 15
        self.queue.mu = 0
        self.assertTrue(math.isnan(self.queue.r))

        self.queue.lamda = -3
        self.queue.mu = -5
        self.assertTrue(math.isnan(self.queue.r))

    def test_ro(self):
        #ro should have a value if lamda and mu are valid
        self.queue.lamda = 15
        self.queue.mu = 20
        self.assertAlmostEqual(0.75, self.queue.ro)

        self.queue.lamda = 25
        self.assertAlmostEqual(1.25, self.queue.ro)

        #test invalid values for lamda and mu
        self.queue.lamda = 0
        self.assertTrue(math.isnan(self.queue.ro))

        self.queue.lamda = 15
        self.queue.mu = 0
        self.assertTrue(math.isnan(self.queue.ro))

        self.queue.lamda = -3
        self.queue.mu = -5
        self.assertTrue(math.isnan(self.queue.ro))

    def test_w(self):
        #w should always be nan for BaseQueue
        self.assertTrue(math.isnan(self.queue.w))

        #test to see if it will give correct values if l and lq are not nan
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue._lq = 5
        self.queue._recalc_needed = False
        self.assertAlmostEqual(0.38333333333, self.queue.w)

    def test_wq(self):
        #wq should always be nan for BaseQueue
        self.assertTrue(math.isnan(self.queue.wq))

        #test to see if it will give correct values if l and lq are not nan
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue._lq = 5
        self.queue._recalc_needed = False
        self.assertAlmostEqual(0.3333333333, self.queue.wq)

    def test_utilization(self):
        #utilization should have a value if lamda and mu are valid
        self.queue.lamda = 15
        self.queue.mu = 20
        self.assertAlmostEqual(0.75, self.queue.utilization)

        self.queue.lamda = 25
        self.assertAlmostEqual(1.25, self.queue.utilization)

    def test_is_valid(self):
        #Test for valid values
        self.queue.lamda = 15
        self.queue.mu = 20
        self.assertTrue(self.queue.is_valid())

        #Test for invalid values for lamda
        self.queue.lamda = 0
        self.assertFalse(self.queue.is_valid())

        self.queue.lamda = -5
        self.assertFalse(self.queue.is_valid())

        self.queue.lamda = "10"
        self.assertFalse(self.queue.is_valid())

        #Test for invalid values for mu
        self.queue.lamda = 15
        self.queue.mu = 0
        self.assertFalse(self.queue.is_valid())

        self.queue.mu = -5
        self.assertFalse(self.queue.is_valid())

        self.queue.mu = "10"
        self.assertFalse(self.queue.is_valid())

    def test_is_feasible(self):
        #Test with valid and feasible values
        self.queue.lamda = 15
        self.queue.mu = 20
        self.assertTrue(self.queue.is_feasible())

        #Test with valid and infeasible values
        self.queue.lamda = 20
        self.assertFalse(self.queue.is_feasible())

        self.queue.lamda = 30
        self.assertFalse(self.queue.is_feasible())

        #Test with invalid values
        self.queue.mu = "35"
        self.assertFalse(self.queue.is_feasible())

        self.queue.lamda = -10
        self.queue.mu = -5
        self.assertFalse(self.queue.is_feasible())

    def test__simplify_lamda(self):
        #Test with valid, non-iterable lamda
        self.assertEqual(15, self.queue._simplify_lamda(15))

        #Test with valid iterable lamda
        self.assertEqual(30, self.queue._simplify_lamda((5,10,15)))

    def test__calc_metrics(self):
        #Test with valid and feasible values
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue._lq = 15
        self.queue._p0 = 10
        self.queue._calc_metrics()
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))
        self.assertFalse(self.queue._recalc_needed)

        #Test with valid but infeasible values
        self.queue.lamda = 20
        self.queue._calc_metrics()
        self.assertTrue(math.isinf(self.queue.lq))
        self.assertTrue(math.isinf(self.queue.p0))

        #Test with invalid values
        self.queue.mu = 0
        self.queue._calc_metrics()
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))


