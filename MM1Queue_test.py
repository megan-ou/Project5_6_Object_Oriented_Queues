from unittest import TestCase
import math
import MM1Queue as q


class TestMM1Queue(TestCase):
    def setUp(self):
        self.queue = q.MM1Queue(15, 20)

    def test_init(self):
        #Test for init works
        self.assertAlmostEqual(15, self.queue._lamda)
        self.assertAlmostEqual(20, self.queue._mu)

        #Check metrics computed for MM1
        expected_lq = (15 ** 2) / (20 * (20 - 15))
        expected_p0 = 1 - 15 / 20
        self.assertAlmostEqual(expected_lq, self.queue._lq)
        self.assertAlmostEqual(expected_p0, self.queue._p0)
        self.assertFalse(self.queue._recalc_needed)

    def test_lq_formula_and_recalc(self):
        #Baseline check
        self.assertAlmostEqual(2.25, self.queue.lq)

        #Change lamda should flag recalc, recompute
        self.queue.lamda = 10
        self.assertTrue(self.queue._recalc_needed)
        self.assertAlmostEqual(0.5, self.queue.lq)
        self.assertFalse(self.queue._recalc_needed)

        #Change mu
        self.queue.mu = 25
        self.assertAlmostEqual(100 / 375, self.queue.lq)
        self.assertFalse(self.queue._recalc_needed)

    def test_p0_formula_and_recalc(self):
        #Baseline p0 = 0.25
        self.assertAlmostEqual(0.25, self.queue.p0)

        self.queue.lamda = 12
        #p0 = 1 - 12/20 = 0.4
        self.assertAlmostEqual(0.4, self.queue.p0)

        self.queue.mu = 24
        #p0 = 1 - 12/24 = 0.5
        self.assertAlmostEqual(0.5, self.queue.p0)

    def test_var_relationships(self):
        #test relationships
        self.assertAlmostEqual(0.75, self.queue.r)
        self.assertAlmostEqual(0.75, self.queue.ro)
        self.assertAlmostEqual(2.25 + 0.75, self.queue.l)
        self.assertAlmostEqual(0.2, self.queue.w)
        self.assertAlmostEqual(0.15, self.queue.wq)
        self.assertAlmostEqual(self.queue.ro, self.queue.utilization)

    def test_infeasible_values(self):
        #test for infeasible values
        self.queue.lamda = 20
        self.queue.mu = 20
        self.assertFalse(self.queue.is_feasible())
        self.assertTrue(math.isinf(self.queue.lq))
        self.assertTrue(math.isinf(self.queue.p0))

        self.queue.lamda = 30
        self.queue.mu = 20
        self.assertFalse(self.queue.is_feasible())
        self.assertTrue(math.isinf(self.queue.lq))
        self.assertTrue(math.isinf(self.queue.p0))

    def test_invalid_values(self):
        #Invalid mu
        self.queue.mu = 0
        #On access, _calc_metrics should set NaNs
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #Invalid lamda
        self.queue.lamda = 0
        self.queue.mu = 10
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #Non-numeric inputs
        self.queue.lamda = "5"
        self.queue.mu = 10
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

    def test_is_valid_and_is_feasible(self):
        #Valid, feasible inputs
        self.queue.lamda = 12
        self.queue.mu = 18
        self.assertTrue(self.queue.is_valid())
        self.assertTrue(self.queue.is_feasible())

        #Valid but infeasible
        self.queue.lamda = 18
        self.queue.mu = 18
        self.assertTrue(self.queue.is_valid())
        self.assertFalse(self.queue.is_feasible())

        #Invalid
        self.queue.mu = 0
        self.assertFalse(self.queue.is_valid())
        self.assertFalse(self.queue.is_feasible())

    def test_str_format(self):
        #__str__ should return a string
        s = str(self.queue)
        self.assertIsInstance(s, str)
        self.assertIn('MM1Queue instance', s)
        self.assertIn('lamda:', s)
        self.assertIn('mu:', s)
        self.assertIn('ro:', s)
        self.assertIn('lq:', s)
        self.assertIn('wq:', s)
        self.assertIn('w:', s)
