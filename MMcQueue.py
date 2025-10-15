import BaseQueue
import math
from numbers import Number

class MMcQueue(BaseQueue.BaseQueue):
    """
    MMC queue class is a Base Queue class that implements a new argument c, or number of servers.
    Contains the values that result from Little's Laws calculations with consideration for the value of c.
    Checks for validity and feasibility of inputs.
    """

    def __init__(self, lamda, mu, c):
        """
        Constructor for MMC queue class. Uses the same arguments as parent class with the addition of c.
        Args:
            c (number): number of servers in the queue
        """
        super().__init__(lamda, mu)
        self.c = c
        self._calc_metrics()
        self._recalc_needed = False

    def __str__(self):
        """
        Method that returns a string representation of a queue's object state.
        Returns: String

        """
        print(f'MMcQueue instance at {id(self)}'
              f'\n\t lamda: {self.lamda}'
              f'\n\t mu: {self.mu}'
              f'\n\t P0: {self.p0}'
              f'\n\t lq: {self.lq}'
              f'\n\t l: {self.l}'
              f'\n\t wq: {self.wq}'
              f'\n\t w: {self.w}'
              f'\n\t c: {self.c}')


    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, c):
        self._recalc_needed = True
        if isinstance(c, Number) and c > 0:
            self._c = c
        else:
            self._c = math.nan

    @property
    def ro(self):
        return self.r / self.c

    def is_valid(self) -> bool:
        """
        Checks to see if lamda, mu, and c are not nan

        Returns: True if all arguments are valid, False if any argument is nan
        """
        if math.isnan(self._lamda) or math.isnan(self.mu) or math.isnan(self.c):
            return False

        return True

    def is_feasible(self) -> bool:
        """
        Checks to see if rho is within range of 0 < rho < 1

        Returns: True if rho is in range and False if rho is out of range
        """
        # Check to see if all values are valid
        if not self.is_valid():
            return False

        if self.ro >= 1:
            return False

        return True

    def _calc_metrics(self):
        """
        Calculates and stores lq, the average number of customers waiting,
        and p_0 , the probability of an empty system, for an MMC queue.
        This applies to MM1 Queues as well.
        This is called whenever lamda, mu, or c is set or changed.

        Returns: None
        """
        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
            return

        if not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf
            return

        #Set recalc_needed to false before calculations are made because the lq calculation calls the
        # getter for p0 and if recalc_needed is true until the end of the calculation, this will result in an infinite
        # loop of calls to calc_metrics. I was not sure if it was appropriate to use self._p0 in the lq calculation
        self._recalc_needed = False

        if self.c == 1:
            #Technically, MM1 should be used if c = 1, but putting this in here just in case since c can be an
            # integer greater than 0.
            self._p0 = 1 - self.ro
            self._lq = (self.lamda ** 2) / (self.mu * (self.mu - self.lamda))

        else:
            #Multiserver calculations separate from single server calculations since the formulas are different.
            #P0 calculated first so that lq calculation can use the calculated p0 metric.
            p0_term_1 = 0
            for i in range(0, self.c):
                p0_term_1 += (self.r ** i) / math.factorial(i)
            p0_term_2 = (self.r ** self.c) / (math.factorial(self.c) * (1 - self.ro))
            self._p0 = 1.0 / (p0_term_1 + p0_term_2)

            lq_numerator = (self.r ** self.c) * self.ro
            lq_denominator = math.factorial(self.c) * ((1 - self.ro) ** 2)
            self._lq = (lq_numerator / lq_denominator) * self.p0
