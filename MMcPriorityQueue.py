import MMcQueue
import math

class MMcPriorityQueue(MMcQueue.MMcQueue):
    """
    MMcPriority Queue implements an MMC Queue with a class system for customers. It will calculate
    queue metrics for each individual class based on what percentage of the calling population is
    in each class.
    Contains the values that result from Little's Laws calculations.
    Checks for validity and feasibility of inputs.
    """