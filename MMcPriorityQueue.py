from toolz.functoolz import is_valid_args

import MMcQueue
import math
from toolz import isiterable
from numbers import Number

class MMcPriorityQueue(MMcQueue.MMcQueue):
    """
    MMcPriority Queue implements an MMC Queue with a class system for customers. It will calculate
    queue metrics for each individual class based on what percentage of the calling population is
    in each class.
    Contains the values that result from Little's Laws calculations.
    Checks for validity and feasibility of inputs.
    """
    def __init__(self, lamda, mu,c):
        """
        Constructor for MMC Priority queue class.
        Uses the same arguments as MMC queue with no additional parameters.
        Args:
            lamda (number): average rate of arrival (scalar or iterable)
            mu (number): average rate of service completion
            c (number): number of servers in the queue
        """
        super().__init__(lamda,mu,c)

    def __str__(self):
        """
        Method that prints a string representation of a queue's object state.
        Returns: None
        """
        print(f'MMcPriorityQueue instance at {id(self)}'
              f'\n\t lamda: {self.lamda}'
              f'\n\t lamda_k: {self.lamda_k}'
              f'\n\t mu: {self.mu}'
              f'\n\t P0: {self.p0}'
              f'\n\t lq: {self.lq}'
              f'\n\t l: {self.l}'
              f'\n\t wq: {self.wq}'
              f'\n\t w: {self.w}'
              f'\n\t c: {self.c}')

    @property
    def lamda(self):

        return self._lamda

    @lamda.setter
    def lamda(self,lamda_k):
        """
        Setter method for lamda property; does error checking on the argument. Overridden method
        to include lamda_k
        Args:
            lamda_k (number): interarrival rate of customers to the queue
        Returns: None
        """
        if isiterable(lamda_k):
            wlamda = lamda_k
        else:
            # If there is a single lamda, bundle it into a single value tuple so it works with the
            # code for iterable lamdas.
            wlamda = (lamda_k,)

        if all([isinstance(l, Number) and l > 0 for l in wlamda]):
            self._lamda = self._simplify_lamda(lamda_k)
            self._lamda_k = lamda_k
        else:
            self._lamda = math.nan
            # instead of assigning the entire lamda_k to math.nan, go in and assign each index to math.nan
            # to keep lamda_k iterable
            self._lamda_k = [math.nan for _ in wlamda]


    @property
    def lamda_k(self):
        """
        Getter method for lamda_k; from what I understand of the instructions,
        lamda_k is a tuple containing all lamdas that can then be called on separately
        through get_lamda_k(). lamda_k is NOT an aggregate lamda.

        Returns: tuple of average interarrival rates for each class k
        """
        return self._lamda_k

    @lamda_k.setter
    def lamda_k(self, lamda_k):
        """
        Setter method for lamda_k; just calls the lamda setter that has been overridden to handle
        lamda_k

        Returns: None
        """
        self.lamda = lamda_k

    def get_b_k(self, k):
        """
        Calculates Bk factor for class k in MMC Priority Queue. Bk represents the amount of capacity remaining
        for service classes greater than k (lower priority classes). Primarily used to calculate a factor used
        in the Wq,k calculation.
        Args:
            k (number): priority class number

        Returns: double, the remaining capacity for lower priority classes
        """
        if not self.is_valid():
            return math.nan

        elif not self.is_feasible():
            return math.inf

        if not isinstance(k, Number) or k < 0 or k > len(self.lamda_k):
            # k cannot be longer than lamda because it will reference indexes that do not exist
            return math.nan

        if k == 0:
            # B0 = 1 as described by the formula
            return 1

        # variable is named rho aggregate because the formula sums up lamda_j / (mu * c) which is rho for each
        # lamda_k; I am not sure if there is a better name for this, this is just what made the most sense to me
        rho_agg = sum([self.lamda_k[j] / (self.c * self.mu) for j in range(k)])
        bk = 1 - rho_agg
        return bk

    def get_l_k(self, k):
        """
        Calculates the average number of priority class k customers in the system.
        Args:
            k (number): priority class number
        Returns: average number of priority class k customers in the system
        """
        if not isinstance(k, Number) or k <= 0 or k > len(self.lamda_k):
            # k cannot be longer than lamda because it will reference indexes that do not exist
            return math.nan

        if not self.is_valid():
            return math.nan

        elif not self.is_feasible():
            return math.inf

        return self.get_lamda_k(k) * self.get_w_k(k)

    def get_lamda_k(self, k):
        """
        Getter method for lamda of specific class k.
        Args:
            k (number): priority class number
        Returns: interarrival rate of class k, or, if k is not specified, tuple of all lamda_k
        """
        if math.isnan(k):
            #return lamda_k because lamda_k is already a tuple with all lamda_k values
            return self.lamda_k
        else:
            #use k-1 because indexing starts at 0
            return  self.lamda_k[k-1]

    def get_lq_k(self, k):
        """
        Calculates the average number of priority class k customers waiting in the queue
        Args:
            k (number): priority class number
        Returns: average number of priority class k customers waiting in the queue
        """
        if not isinstance(k, Number) or k <= 0 or k > len(self.lamda_k):
            # k cannot be greater than the length of lamda because then we would be referencing indexes that
            # do not exist
            return math.nan

        if not self.is_valid():
            return math.nan

        elif not self.is_feasible():
            return math.inf

        # if all arguments valid and feasible, calculate lqk based on little's laws
        return self.get_lamda_k(k) * self.get_wq_k(k)

    def get_ro_k(self, k):
        """
        Calculate utilization for all priority class k customers and higher customers waiting in queue
        Args:
            k (number): priority class number
        Returns: utilization for all priority class k customers and higher
        """
        if not isinstance(k, Number) or k <= 0 or k > len(self.lamda_k):
            # k cannot be greater than the length of lamda because then we would be referencing indexes that
            # do not exist
            return math.nan

        if not self.is_valid():
            return math.nan

        elif not self.is_feasible():
            return math.inf

        #Use k-1 because indexing starts at 0.
        ro_k = sum(self.get_lamda_k(i) / (self.mu * self.c) for i in range(1, k + 1))
        return ro_k

    def get_w_k(self, k):
        """
        Calculates average time in spent in the system for a customer in priority class k.
        Args:
            k (number): priority class number
        Returns: average time in spent in the system for a customer in priority class k

        """
        if not isinstance(k, Number) or k <= 0 or k > len(self.lamda_k):
            # k cannot be greater than the length of lamda because then we would be referencing indexes that
            # do not exist
            return math.nan

        if not self.is_valid():
            return math.nan

        elif not self.is_feasible():
            return math.inf

        return self.get_wq_k(k) + (1/self.mu)

    def get_wq_k(self, k):
        """
        Calculates the average time spent waiting in queue for customer priority class k
        Args:
            k (number): priority class number
        Returns: average time spent waiting in queue for customer priority class k
        """
        if not isinstance(k, Number) or k <= 0 or k > len(self.lamda_k):
            # k cannot be greater than the length of lamda because then we would be referencing indexes that
            # do not exist
            return math.nan

        if not self.is_valid():
            return math.nan

        elif not self.is_feasible():
            return math.inf

        wqk = (1 - self.ro) * self.lq / (self.lamda * self.get_b_k(k-1) * self.get_b_k(k))
        return wqk