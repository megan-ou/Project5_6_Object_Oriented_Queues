import math
from math import isnan
import BaseQueue


class MM1Queue(BaseQueue.BaseQueue):
    """
    MM1 queue class is a Base Queue class that implements single server queue (c = 1).
    Checks for validity and feasibility of inputs.
    """

    def __init__(self, lamda, mu):
        """
        Constructor for MMC queue class. Uses the same arguments as parent class with the addition of c = 1.
        Args:
            lamda (number): average rate of arrival (scalar or iterable)
            mu (number): average rate of service completion
        """
        super().__init__(lamda, mu)

    def __str__(self):
        """
        Method that returns a string representation of a queue's object state.
        Returns: String

        """
        return (
            f'MM1Queue instance at {id(self)}'
            f'\n\t lamda: {self.lamda}'
            f'\n\t mu: {self.mu}'
            f'\n\t ro: {self.ro}'
            f'\n\t lq: {self.lq}'
            f'\n\t l: {self.l}'
            f'\n\t wq: {self.wq}'
            f'\n\t w: {self.w}'
        )

    def _calc_metrics(self):
        """
        Calculates Lq and P0 for M/M/1 queue
        """
        #If any of the arguments are invalid, set lq and p0 to math.nan and if the queue is
        # valid but infeasible, set lq and p0 to math.inf. This way, no calculations will be made if
        # any arguments are not an actual number.
        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
            self._recalc_needed = False
            return

        if not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf
            self._recalc_needed = False
            return

        #lq calculation based on single server queue
        denominator = self.mu * (self.mu - self.lamda)
        if denominator == 0:
            self._lq = math.nan
        else:
            self._lq = self.lamda ** 2 / denominator

        #p0 calculation based on single server queue
        #can also use self.ro here instead of self.lamda / self.mu (megan)
        self._p0 = 1 - self.lamda / self.mu
        self._recalc_needed = False