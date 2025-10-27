import BaseQueue
import math
from numbers import Number

class MG1Queue(BaseQueue.BaseQueue):
    """
    MG1 queue is singler server with
    Poisson arrivals (regardless of service time distribution type)
    """

    def __init__(self, lamda, mu, sigma):
        self._sigma = math.nan  #service-time std dev
        super().__init__(lamda, mu)
        self.sigma = sigma  #validate via setter

    def __str__(self):
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
        return self._sigma

    @sigma.setter
    def sigma(self, val):
        self._recalc_needed = True
        if isinstance(val, Number) and val >= 0:
            self._sigma = float(val)
        else:
            self._sigma = math.nan

    def is_valid(self) -> bool:
        if not super().is_valid():  #checks lamda and mu
            return False
        return not math.isnan(self._sigma)

    def is_feasible(self) -> bool:
        """
        Feasibility for MG1 depends only on lamda and mu (p < 1).
        Don't make feasibility check depend on sigma
        """
        #lamda, mu must be valid numbers
        if math.isnan(self._lamda) or math.isnan(self._mu):
            return False

        if self._mu == 0:
            return False
        rho = self._lamda / self._mu
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
        if denominator <= 0 or math.isnan(denominator):
            self._lq = math.nan
        else:
            self._lq = (rho ** 2 + (self.lamda ** 2) * (self.sigma ** 2)) / denominator

        self._p0 = 1 - rho
        self._recalc_needed = False
