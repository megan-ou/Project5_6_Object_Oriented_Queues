from unittest import TestCase
import math
import MMcQueue as q


class TestMMcQueue(TestCase):
    def setUp(self):
        #Feasible multi-server system
        self.queue = q.MMcQueue(15, 20, 2)

    def test_init(self):
        #Test init and metrics
        self.assertAlmostEqual(15, self.queue._lamda)
        self.assertAlmostEqual(20, self.queue._mu)
        self.assertAlmostEqual(2, self.queue._c)

        expected_p0 = 1.0 / (1.0 + 0.75 + (0.75**2) / (2 * (1 - 0.375)))
        expected_lq = ((0.75**2) * 0.375) / (2 * (1 - 0.375) ** 2) * expected_p0

        self.assertAlmostEqual(expected_p0, self.queue._p0)
        self.assertAlmostEqual(expected_lq, self.queue._lq)
        self.assertFalse(self.queue._recalc_needed)

    def test_c_property(self):
        #getter
        self.assertAlmostEqual(2, self.queue.c)

        #valid set
        self.queue.c = 3
        self.assertAlmostEqual(3, self.queue.c)
        self.assertTrue(self.queue._recalc_needed)

        #invalid sets of c
        self.queue.c = 0
        self.assertTrue(math.isnan(self.queue.c))
        self.assertFalse(self.queue.is_valid())

        self.queue.c = -2
        self.assertTrue(math.isnan(self.queue.c))
        self.assertFalse(self.queue.is_valid())

        self.queue.c = "2"
        self.assertTrue(math.isnan(self.queue.c))
        self.assertFalse(self.queue.is_valid())

    def test_ro_uses_c(self):
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue.c = 2
        self.assertAlmostEqual(0.75, self.queue.r)
        self.assertAlmostEqual(0.375, self.queue.ro)

        #Change in c to confirm ro updates
        self.queue.c = 3
        self.assertAlmostEqual(0.75 / 3, self.queue.ro)

    def test_c_equals_1(self):
        #When c=1, formulates in M/M/1
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue.c = 1

        self.assertAlmostEqual(2.25, self.queue.lq)
        self.assertAlmostEqual(0.25, self.queue.p0)

        #Little's Law relationships
        self.assertAlmostEqual(0.75, self.queue.r)
        self.assertAlmostEqual(2.25 + 0.75, self.queue.l)
        self.assertAlmostEqual((2.25 + 0.75) / 15, self.queue.w)
        self.assertAlmostEqual(2.25 / 15, self.queue.wq)

    def test_multiserver_metrics(self):
        #c=2, lamda=15, mu=20
        self.queue.lamda = 15
        self.queue.mu = 20
        self.queue.c = 2

        #expectations
        r = 15 / 20
        ro = r / 2
        expected_p0 = 1.0 / (1 + r + (r**2) / (2 * (1 - ro)))
        expected_lq = ((r**2) * ro) / (2 * (1 - ro) ** 2) * expected_p0
        expected_L = expected_lq + r
        expected_W = expected_L / 15
        expected_Wq = expected_lq / 15

        self.assertAlmostEqual(expected_p0, self.queue.p0)
        self.assertAlmostEqual(expected_lq, self.queue.lq)
        self.assertAlmostEqual(expected_L, self.queue.l)
        self.assertAlmostEqual(expected_W, self.queue.w)
        self.assertAlmostEqual(expected_Wq, self.queue.wq)

    def test_recalc_on_change(self):
        #Change lamda, mu, c separately and ensure recompute
        self.queue.lamda = 10
        self.assertFalse(math.isnan(self.queue.lamda))
        self.assertTrue(self.queue._recalc_needed)
        self.queue.lq
        self.assertFalse(self.queue._recalc_needed)

        self.queue.mu = 25
        self.assertFalse(math.isnan(self.queue.mu))
        self.assertTrue(self.queue._recalc_needed)
        self.queue.p0
        self.assertFalse(self.queue._recalc_needed)

        self.queue.c = 3
        self.assertFalse(math.isnan(self.queue.c))
        self.assertTrue(self.queue._recalc_needed)
        self.queue.lq
        self.assertFalse(self.queue._recalc_needed)

    def test_infeasible_values(self):
        #Test infeasible values
        self.queue.lamda = 40
        self.queue.mu = 20
        self.queue.c = 2
        self.assertFalse(self.queue.is_feasible())
        self.assertTrue(math.isinf(self.queue.lq))
        self.assertTrue(math.isinf(self.queue.p0))

        self.queue.lamda = 100
        self.queue.mu = 20
        self.queue.c = 3
        self.assertFalse(self.queue.is_feasible())
        self.assertTrue(math.isinf(self.queue.lq))
        self.assertTrue(math.isinf(self.queue.p0))

    def test_invalid_values(self):
        #Invalid mu
        self.queue.mu = 0
        self.assertFalse(self.queue.is_valid())
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #Negative mu
        self.queue.mu = -20
        self.assertFalse(self.queue.is_valid())
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #Invalid lamda
        self.queue.lamda = 0
        self.queue.mu = 10
        self.assertFalse(self.queue.is_valid())
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #Negative lamda
        self.queue.lamda = -10
        self.queue.mu = 10
        self.assertFalse(self.queue.is_valid())
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #Invalid c
        self.queue.c = 0
        self.assertFalse(self.queue.is_valid())
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

        #Negative c
        self.queue.c = -2
        self.assertFalse(self.queue.is_valid())
        self.assertTrue(math.isnan(self.queue.lq))
        self.assertTrue(math.isnan(self.queue.p0))

    def test_is_valid_and_is_feasible(self):
        #Valid and feasible
        self.queue.lamda = 12
        self.queue.mu = 18
        self.queue.c = 2
        self.assertTrue(self.queue.is_valid())
        self.assertTrue(self.queue.is_feasible())
