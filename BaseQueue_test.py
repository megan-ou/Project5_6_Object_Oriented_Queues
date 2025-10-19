from unittest import TestCase
import math
import BaseQueue as q

class TestBaseQueue(TestCase):
    def setUp(self):
        self.queue = q.BaseQueue(20, 15)

    def test_init(self):
        #Before seeing Dr. Mitchell's test cases, I used self.queue.lamda, but that would test the setter/getter
        # I think we want to test to see if init calls the proper setters and everything works.
        self.assertAlmostEqual(20, self.queue._lamda)
        self.assertAlmostEqual(15, self.queue._mu)
        self.assertTrue(math.isnan(self.queue._lq))
        self.assertTrue(math.isnan(self.queue._p0))
        self.assertFalse(self.queue._recalc_needed)

    def test_lamda(self):
        #First test the getter method
        self.assertAlmostEqual(20, self.queue.lamda)

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
        self.assertAlmostEqual(15, self.queue.mu)

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

        #test functionality of recalc_needed boolean; if it is true, is calc_metrics called and is the
        # variable then set to false? The value of lq should still be nan because that is what calc_metrics
        # was set to do.
        self.queue._lq = 20
        #Sets recalc_needed to true
        self.queue.lamda = 15
        self.queue.mu = 20
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertFalse(self.queue._recalc_needed)

        #test to see if getter will work when lq is not nan
        self.queue._lq = 20
        self.assertAlmostEqual(20,self.queue.lq)

    def test_p0(self):
        #p0 should always be math.nan for BaseQueue
        self.assertTrue(math.isnan(self.queue.p0))

    def test_l(self):
        self.fail()

    def test_r(self):
        self.fail()

    def test_ro(self):
        self.fail()

    def test_w(self):
        self.fail()

    def test_wq(self):
        self.fail()

    def test_utilization(self):
        self.fail()

    def test_is_valid(self):
        self.fail()

    def test_is_feasible(self):
        self.fail()

    def test__simplify_lamda(self):
        self.fail()

    def test__calc_metrics(self):
        self.fail()
