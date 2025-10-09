import math

from tenacity import retry_unless_exception_type
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
        #TODO: Should there be error checking both in here and in the setters?
        # and should I change any of the is_valid and is_feasible code?
        #TODO: Google docstrings?
        #TODO: Unit testing?
        #TODO: Difference between ro and utilization
        #TODO: Is it okay to set attributes to none?
        #TODO: What is recalc_needed? It is different from the other properties in the UML diagram
        self._lamda = lamda
        self._mu = mu
        self._lq = None
        self._p0 = None
        #TODO: no underscore?
        self.recalc_needed = False
        self._l = None
        self._r = None
        self._ro = None
        self._w = None
        self._wq = None
        self._utilization = None

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
        if self.is_valid(lamda, self.mu):
            self._lamda = lamda
        else:
            self._lamda = math.nan

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, mu):
        self.recalc_needed = True
        if self.is_valid(self.lamda, mu):
            self._mu = mu
        else:
            self._mu = math.nan

    @property
    def lq(self):
        if self.recalc_needed == True:
            self.calc_metrics()
            self.recalc_needed = False

        if self.is_feasible(self.lamda, self.mu):
            return self._lq
        else:
            return math.inf

    @property
    def p0(self):
        if self.recalc_needed == True:
            self.calc_metrics()
            self.recalc_needed = False

        if self.is_feasible(self.lamda, self.mu):
            return self._p0
        else:
            return math.inf

    #TODO: does order of declaration matter here?
    @property
    def l(self):
        return self.lq + self.r

    @property
    def r(self):
        return self.lamda / self.mu

    @property
    def ro(self):
        #TODO: is this appropriate? would I have to do this for every setter
        # that uses lamda
        wlamda = self.simplify_lamda(self.lamda)
        #TODO: since BaseQueue assumes c = 1, then the "c" attribute wouldn't be present here?
        return wlamda / self.mu

    @property
    def w(self):
        return self.l / self.lamda

    @property
    def wq(self):
        return self.lq / self.lamda

    @property
    def utilization(self):
        return self.lamda / self.mu

    def is_valid(self, lamda, mu, c=1) -> bool:
        """
        Checks to see if all arguments are numerical.
        Checks to see if value of arguments are within the valid range for queue calculations.
        Streamlined version of is_valid that is used was given to us as feedback by Dr. Mitchell.

        Args:
            lamda (number): arrival rate of customers per time interval (scalar or multivalued)
            mu (number): service rate per time interval (scalar)
            c (number): number of servers in the system (scalar)

        Returns: True if all arguments are valid, False if any argument is invalid
        """
        # Check to see is lamda is iterable. If lamda is a single value, bundle it into a single
        # value tuple so that we can treat all cases of lamda the same
        # If lamda is an iterable, coerce it into a tuple as well so we can bundle it with
        # the other arguments
        #TODO: simplify lamda?
        if isiterable(lamda):
            wlamda = tuple(lamda)
        else:
            wlamda = (lamda,)

        # Combine args into a single tuple so that we can check to see if all arguments are
        # numbers and greater than 0 once.
        args = (mu, c, *wlamda)

        if all([isinstance(a, Number) and a > 0 for a in args]):
            return True

        else:
            return False

    def is_feasible(self, lamda, mu, c=1) -> bool:
        """
        Calculates rho (ρ) and checks to see if the value of rho is feasible.
        rho must be a value between 0 and 1.
        rho = lamda / mu * c

        Args:
            lamda (number): arrival rate of customers per time interval (scalar or multivalued)
            mu (number): service rate per time interval (scalar)
            c (number): number of servers in the system (scalar)

        Returns: True if rho is feasible False if rho is not feasible
        """
        # Check to see if all values are valid
        if not self.is_valid(lamda, mu, c):
            return False

        # Check to see if 0 < rho < 1 because rho is a percentage of time a server is busy
        # Since is_valid() already ensures that lamda, mu, and c are non-negative values, we only need to check
        # to see if rho is less than 1.
        if self.ro < 1:
            return False

        return True

    def simplify_lamda(self, lamda) -> float:
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

    def calc_metrics(self):
        """
        Calculates and stores  , the average number of customers waiting,
        and p_0 , the probability of an empty system, for the queue.
        This is called whenever lamda or mu is set or changed.

        Returns: None

        """
        #TODO