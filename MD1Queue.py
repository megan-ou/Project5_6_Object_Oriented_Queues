import BaseQueue
import math

class MD1Queue(BaseQueue.BaseQueue):
    """
    MD1Queue implements an MM1 queue with Poisson arrivals and deterministic service times.
    Contains the values that result from Little's Laws calculations.
    Checks validity and feasibility of inputs.
    """
    def __init__(self, lamda, mu):
        """
        Constructor for MD1 Priority queue class.
        Uses the same arguments as MM1 queue with no additional parameters.
        Args:
            lamda (number): average rate of arrival (scalar or iterable)
            mu (number): average rate of service completion
        Returns: None
        """
        super().__init__(lamda, mu)

    def __str__(self):
        """
        Method that prints a string representation of an MD1 queue's object state.
        Returns: None
        """
        return (
            f'MD1Queue instance at {id(self)}'
            f'\n\t lamda: {self.lamda}'
            f'\n\t mu: {self.mu}'
            f'\n\t p: {self.ro}'
            f'\n\t P0: {self.p0}'
            f'\n\t Lq: {self.lq}'
            f'\n\t l: {self.l}'
            f'\n\t Wq: {self.wq}'
            f'\n\t w: {self.w}'
        )

    def _calc_metrics(self):
        """
        Calculates Lq and P0 of MD1 queue
        Returns: None
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

        #MD1 formula
        denominator = 2 * self.mu * (self.mu - self.lamda)
        self._lq = (self.lamda ** 2) / denominator

        #p0 calculation based on single server queue
        self._p0 = 1 - self.ro
        self._recalc_needed = False




