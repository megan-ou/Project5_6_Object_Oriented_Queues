import math
from toolz import isiterable
from numbers import Number

class BaseQueue:
    """
    Base queue class that holds all the attributes of a standard queue.
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
        self._recalc_needed = False
        self.lamda = lamda
        self.mu = mu
        #self._lq = math.nan
        #self._p0 = math.nan

    def __str__(self):
        """
        Method that returns a string representation of a queue's object state.
        Returns: String
        """
        print(f'BaseQueue instance at {id(self)}'
              f'\n\t lamda: {self.lamda}'
              f'\n\t mu: {self.mu}'
              f'\n\t P0: {self.p0}'
              f'\n\t lq: {self.lq}'
              f'\n\t l: {self.l}'
              f'\n\t wq: {self.wq}'
              f'\n\t w: {self.w}')

    @property
    def lamda(self):
        """
        Getter method for lamda property
        Returns: interarrival rate of customers
        """
        return self._lamda

    @lamda.setter
    def lamda(self, lamda):
        """
        Setter method for lamda property; does error checking on the argument
        Args:
            lamda (number): interarrival rate of customers to the queue
        Returns: None
        """
        self._recalc_needed = True

        if isiterable(lamda):
            #Force lamda into a tuple so we can iterate through it when checking the values
            # if it is already iterable
            wlamda = lamda
        else:
            #If there is a single lamda, bundle it into a single value tuple so it works with the
            # code for iterable lamdas.
            wlamda = (lamda,)

        if all([isinstance(l, Number) and l > 0 for l in wlamda]):
            self._lamda = self._simplify_lamda(lamda)
        else:
            self._lamda = math.nan

    @property
    def mu(self):
        """
        Getter method for mu property
        Returns: average rate of service time
        """
        return self._mu

    @mu.setter
    def mu(self, mu):
        """
        Setter method for mu property; does error checking
        Args:
            mu (number): average rate of service time
        Returns: None
        """
        self._recalc_needed = True
        if isinstance(mu, Number) and mu > 0:
            self._mu = mu
        else:
            self._mu = math.nan

    @property
    def lq(self):
        """
        Getter method for lq property. Values for lq are set in calc_metrics.
        Returns: the average number of people waiting in the queue
        """
        if self._recalc_needed:
            self._calc_metrics()
            self._recalc_needed = False
        return self._lq

    @property
    def p0(self):
        """
        Getter method for p0 property. Values for p0 are set in calc_metrics.
        Returns: the probability of an empty queue
        """
        if self._recalc_needed:
            self._calc_metrics()
            self._recalc_needed = False
        return self._p0

    @property
    def l(self):
        """
        Getter method for l property calculated using Little's Laws
        Returns: average number of people in the system
        """
        return self.lq + self.r

    @property
    def r(self):
        """
        Getter method for r property calculated using Little's Laws
        Returns: expected number of customers in service
        """
        return self.lamda / self.mu

    @property
    def ro(self):
        """
        Getter method for ro property calculated using Little's Laws
        Returns: traffic intensity of the queue
        """
        return self.r

    @property
    def w(self):
        """
        Getter method for w property calculated using Little's Laws
        Returns: time spent in the system
        """
        return self.l / self.lamda

    @property
    def wq(self):
        """
        Getter method for wq property calculated using Little's Laws
        Returns: time spent waiting in the queue
        """
        return self.lq / self.lamda

    @property
    def utilization(self):
        """
        Getter method for utilization property; another word for ro.
        Returns: the value of ro, or the system utilization
        """
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
        Checks to see if rho is within range of 0 < rho < 1

        Returns: True if rho is in range and False if rho is out of range
        """
        # Check to see if all values are valid
        if not self.is_valid():
            return False

        if self.ro >= 1:
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
            self._lq = math.nan
            self._p0 = math.nan
            return

        if not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf
            return

        #This is in place of an abstract class. Sets the value of lq and p0 to math.nan since a base queue
        # does not have an lq or p0 formula.
        self._lq = math.nan
        self._p0 = math.nan

        self._recalc_needed = False
