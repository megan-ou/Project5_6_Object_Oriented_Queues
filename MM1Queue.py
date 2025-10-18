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
            c (number): number of servers in the queue (c = 1 for MM1)
        """
        self.c = 1  # single server
        super().__init__(lamda, mu)
        self._calc_metrics()

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
            f'\n\t c: {self.c}'
        )

    @property
    def ro(self):
        return self.lamda / (self.mu * self.c)

    def is_valid(self) -> bool:
        """
        Checks to see if lamda, mu, and c are not nan

        Returns: True if all arguments are valid, False if any argument is nan
        """
        if math.isnan(self._lamda) or math.isnan(self.mu) or math.isnan(self.c):
            return False
        if self.lamda <= 0 or self.mu <= 0:
            return False
        return True

    def is_feasible(self) -> bool:
        """
        Checks to see if rho is within range of 0 < rho < 1

        Returns: True if rho is in range and False if rho is out of range
        """
        if not self.is_valid():
            return False
        return self.ro < 1

    def _calc_metrics(self):
        """
        Calculates Lq and P0 for M/M/1 queue
        """
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

        lamda = self.lamda
        mu = self.mu

        denominator = mu * (mu - lamda)
        if denominator == 0:
            self._lq = math.nan
        else:
            self._lq = lamda ** 2 / denominator

        self._p0 = 1 - lamda / mu
        self._recalc_needed = False