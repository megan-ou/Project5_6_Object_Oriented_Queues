from unittest import TestCase
import MMcPriorityQueue as q
import math

class TestMMcPriorityQueue(TestCase):
    def setUp(self):
        #use class lamda so k is iterable
        self.queue = q.MMcPriorityQueue((6, 4, 5), 20, 2)

    def test_innit(self):
        #Test for init sets basic attributes right
        self.assertAlmostEqual(15, self.queue.lamda)
        self.assertAlmostEqual(20, self.queue.mu)
        self.assertTrue(self.queue._recalc_needed)

    def test_lamda(self):
        #feasible system
        self.assertAlmostEqual(15, self.queue.lamda)
        self.assertEqual((6, 4, 5), self.queue.lamda_k)

        #change lamda to new tuple, confirm sum and structure
        self.queue.lamda = (10, 5)
        self.assertAlmostEqual(15, self.queue.lamda)
        self.assertEqual((10, 5), self.queue.lamda_k)

        #invalid lamda
        self.queue.lamda = (-1.2,)
        self.assertTrue(math.isnan(self.queue.lamda))
        self.assertFalse(self.queue.is_valid())

    def test_lamda_k(self):
        #getter returns tuple
        self.assertEqual((6, 4, 5), self.queue.lamda_k)

        #setter updates lamda test
        self.queue.lamda_k = (7, 8)
        self.assertAlmostEqual(15, self.queue.lamda)
        self.assertEqual((7, 8), self.queue.lamda_k)

    def test_get_b_k(self):
        #valid k test
        self.assertAlmostEqual(1.0, self.queue.get_b_k(0))
        self.assertAlmostEqual(0.85, self.queue.get_b_k(1), places=7)
        self.assertAlmostEqual(0.75, self.queue.get_b_k(2), places=7)
        self.assertAlmostEqual(0.625, self.queue.get_b_k(3), places=7)

        #invalid k test
        self.assertTrue(math.isnan(self.queue.get_b_k(-1)))
        self.assertTrue(math.isnan(self.queue.get_b_k(4)))

    def test_get_l_k(self):
        # test valid k values
        w1 = self.queue.get_w_k(1)
        w2 = self.queue.get_w_k(2)
        w3 = self.queue.get_w_k(3)

        self.assertAlmostEqual(6 * w1, self.queue.get_l_k(1))
        self.assertAlmostEqual(4 * w2, self.queue.get_l_k(2))
        self.assertAlmostEqual(5 * w3, self.queue.get_l_k(3))

    def test_get_lamda_k(self):
        #test valid k values (starts at 1)
        self.assertAlmostEqual(6, self.queue.get_lamda_k(1))
        self.assertAlmostEqual(4, self.queue.get_lamda_k(2))
        self.assertAlmostEqual(5, self.queue.get_lamda_k(3))

        #test invalid k value (nan)
        self.assertEqual((6, 4, 5), self.queue.get_lamda_k(math.nan))

    def test_get_lq_k(self):
        # est valid k values
        wq1 = self.queue.get_wq_k(1)
        wq2 = self.queue.get_wq_k(2)
        wq3 = self.queue.get_wq_k(3)

        self.assertAlmostEqual(6 * wq1, self.queue.get_lq_k(1))
        self.assertAlmostEqual(4 * wq2, self.queue.get_lq_k(2))
        self.assertAlmostEqual(5 * wq3, self.queue.get_lq_k(3))

        #test invalid k values
        self.assertTrue(math.isnan(self.queue.get_lq_k(0)))
        self.assertTrue(math.isnan(self.queue.get_lq_k(4)))

    def test_get_ro_k(self):
        #test valid k values
        self.assertFalse(math.isnan(self.queue.get_ro_k(1)))
        self.assertFalse(math.isnan(self.queue.get_ro_k(2)))
        self.assertFalse(math.isnan(self.queue.get_ro_k(3)))

        #test invalid k values
        self.assertTrue(math.isnan(self.queue.get_ro_k(0)))
        self.assertTrue(math.isnan(self.queue.get_ro_k(4)))

    def test_get_w_k(self):
        #test valid k values
        wq1 = self.queue.get_wq_k(1)
        wq2 = self.queue.get_wq_k(2)
        wq3 = self.queue.get_wq_k(3)

        self.assertAlmostEqual(wq1 + 1 / 20, self.queue.get_w_k(1))
        self.assertAlmostEqual(wq2 + 1 / 20, self.queue.get_w_k(2))
        self.assertAlmostEqual(wq3 + 1 / 20, self.queue.get_w_k(3))

        #test invalid k values
        self.assertTrue(math.isnan(self.queue.get_w_k(0)))
        self.assertTrue(math.isnan(self.queue.get_w_k(4)))

    def test_get_wq_k(self):
        #test valid values
        self.assertFalse(math.isnan(self.queue.get_wq_k(1)))
        self.assertFalse(math.isnan(self.queue.get_wq_k(2)))
        self.assertFalse(math.isnan(self.queue.get_wq_k(3)))

        #test invalid values
        self.assertTrue(math.isnan(self.queue.get_wq_k(0)))
        self.assertTrue(math.isnan(self.queue.get_wq_k(4)))