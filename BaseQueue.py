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
        #TODO: Should there be error checking both in here and in the setters?
        # and should I change any of the is_valid and is_feasible code?
        self._lamda = lamda
        self._mu = mu

    @property
    def lamda(self):
        return self._lamda

    @lamda.setter
    def lamda(self, lamda):
        if self.is_valid(lamda, self.mu) and self.is_feasible(lamda, self.mu):
            self._lamda = lamda
        else:
            self._lamda = math.nan

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, mu):
        if self.is_valid(self.lamda, mu) and self.is_feasible(self.lamda, mu):
            self._mu = mu
        else:
            self._mu = math.nan

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

        # Check to see if lamda is iterable and sum lamda up if it is
        if isiterable(lamda):
            lamda = sum(lamda)

        # Calculate rho using Little's Laws
        rho = lamda / (c * mu)

        # Check to see if 0 < rho < 1 because rho is a percentage of time a server is busy
        # Since is_valid() already ensures that lamda, mu, and c are non-negative values, we only need to check
        # to see if rho is less than 1.
        if rho >= 1:
            return False

        return True