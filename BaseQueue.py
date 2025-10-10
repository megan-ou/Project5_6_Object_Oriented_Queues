import math
from toolz import isiterable
from numbers import Number

class BaseQueue:
    """
    Base queue class that holds all the attributes of a M/M/1 Queue.
    Contains the values that result from Little's Laws calculations.
    Checks for validity and feasibility of inputs.
    This is the inheritable class.
    """
    def __init__(self, lamda, mu):
        """
        Constructor for BaseQueue class.
        Args:
            lamda (number): average rate of arrival (scalar or iterable)
            mu (number): average rate of service completion
        """
        self.lamda = lamda
        self.mu = mu
        self._lq = None
        self._p0 = None
        self._recalc_needed = False

    def __str__(self):
        """
        Method that returns a string representation of a queue's object state.
        Returns: String

        """
        #TODO


    @property
    def lamda(self):
        return self._lamda

    @lamda.setter
    def lamda(self, lamda):
        self.recalc_needed = True

        if isiterable(lamda):
            wlamda = tuple(lamda)
        else:
            wlamda = (lamda,)

        if all([isinstance(a, Number) and a > 0 for a in wlamda]):
            self._lamda = self._simplify_lamda(lamda)
        else:
            self._lamda = math.nan

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, mu):
        self.recalc_needed = True
        if isinstance(mu, Number) and mu > 0:
            self._mu = mu
        else:
            self._mu = math.nan

    @property
    def lq(self):
        if self._recalc_needed:
            self._calc_metrics()
            self._recalc_needed = False
        return self._lq

    @property
    def p0(self):
        if self._recalc_needed:
            self._calc_metrics()
            self._recalc_needed = False
        return self._p0

    @property
    def l(self):
        return self.lq + self.r

    @property
    def r(self):
        return self.lamda / self.mu

    @property
    def ro(self):
        return self.r

    @property
    def w(self):
        return self.l / self.lamda

    @property
    def wq(self):
        return self.lq / self.lamda

    @property
    def utilization(self):
        return self.ro

    def is_valid(self) -> bool:
        """
        Checks to see if lamda and mu are not nan

        Returns: True if all arguments are valid, False if any argument is nan
        """
        if math.isnan(self._lamda) or math.isnan(self.mu):
            return False

        return True

    def is_feasible(self) -> bool:
        """
        Checks to see if rho is not inf

        Returns: True if rho is not inf and False if rho is inf
        """
        # Check to see if all values are valid
        if not self.is_valid():
            return False

        if self.ro > 1:
            return False

        return True

    def _simplify_lamda(self, lamda) -> float:
        """
        Helper function that checks to see if lamda is iterable and aggregates it.
        Args:
            lamda (number): arrival rate of customers per time interval (scalar or multivalued)

        Returns: Sum of lamda if lamda is iterable and lamda if lamda is not iterable

        """
        if isiterable(lamda):
            return sum(lamda)
        else:
            return lamda

    def _calc_metrics(self):
        """
        Calculates and stores the average number of customers waiting,
        and p_0 , the probability of an empty system, for the queue.
        This is called whenever lamda or mu is set or changed.

        Returns: None

        """
        if not self.is_valid():
            self._lamda = math.nan
            self._p0 = math.nan

        if not self.is_feasible():
            self._lamda = math.inf
            self._p0 = math.inf

        self._lamda = math.nan
        self._p0 = math.nan
        self._recalc_needed = False
