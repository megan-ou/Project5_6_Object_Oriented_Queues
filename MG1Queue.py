import BaseQueue
import math
from numbers import Number

class MG1Queue(BaseQueue.BaseQueue):
    """
    MG1 queue applies to any single server queue with Poisson arrivals (regardless of service time distribution type).
    Contains the values that result from Little's Laws calculations.
    Calculates metrics using the Checks validity and feasibility of inputs.
    """
    def __init__(self, lamda, mu, sigma = 0.0):
        super().__init__(lamda, mu)
        self.sigma = sigma  #validate via setter

    def __str__(self):
        """
        Method that prints a string representation of a queue's object state.
        Returns: None
        """
        return (
            f"MG1Queue instance at {id(self)}"
            f"\n\t lamda: {self.lamda}"
            f"\n\t mu: {self.mu}"
            f"\n\t sigma: {self.sigma}"
            f"\n\t ro: {self.ro}"
            f"\n\t P0: {self.p0}"
            f"\n\t Lq: {self.lq}"
            f"\n\t l: {self.l}"
            f"\n\t Wq: {self.wq}"
            f"\n\t w: {self.w}"
        )

    #service time variance property
    @property
    def sigma(self):
        """
        Getter method for sigma property
        Returns: service tive variance
        """
        return self._sigma

    @sigma.setter
    def sigma(self, val):
        self._recalc_needed = True
        if isinstance(val, Number) and val >= 0:
            #TODO: I do not believe you need to force val into a float
            self._sigma = float(val)
        else:
            self._sigma = math.nan

    def is_valid(self) -> bool:
        if not super().is_valid():  #checks lamda and mu
            return False
        return not math.isnan(self.sigma)

    def is_feasible(self) -> bool:
        """
        Checks whether the MG1 queue system is feasible.
        Returns: True if lamda / mu < 1. False otherwise.
        """
        #lamda, mu must be valid numbers
        if math.isnan(self.lamda) or math.isnan(self.mu):
            return False

        if self.mu <= 0:
            return False
        rho = self.lamda / self.mu
        return rho < 1

    def _calc_metrics(self):
        #Compute Lq and P0 for MG1
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

        rho = self.ro
        denominator = 2 * (1 - rho)

        self._lq = (rho ** 2 + (self.lamda ** 2) * (self.sigma ** 2)) / denominator

        self._p0 = 1 - rho
        self._recalc_needed = False
